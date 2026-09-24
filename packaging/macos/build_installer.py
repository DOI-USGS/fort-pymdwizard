#!/usr/bin/env python3
"""
Build a macOS installer (.pkg) for MetadataWizard from a fort-pymdwizard
git checkout.

STATUS: first draft / sketch. Has not been run end-to-end yet.

Layout this produces (mirrors the existing v2.0.7 install and the Windows
Inno Setup script's conventions):

    MetadataWizard.app/Contents/
        Info.plist
        MacOS/
            MetadataWizard   (launcher)
            pip              (pip wrapper)
        Resources/
            Ducky.icns
        Frameworks/
            pymdwizard/      (conda env, built --prefix directly here)
        fort-pymdwizard/     (git clone of main-v2.2, .git included so the
                               app's built-in "check for updates" feature
                               -- MainWindow.check_for_updates/
                               update_from_github, which merges from
                               origin/<active branch> -- works)
        docs/
        examples/

Known gaps / things to confirm before this is production-ready:
  - Not signed or notarized. Add `productsign --sign <identity>` on the
    .pkg and `xcrun notarytool submit` + `xcrun stapler staple` before
    distributing outside your own machine.
  - The jupyterlab kernel.json (see the Windows .iss CreateKernelFile
    step) isn't written here -- conda's jupyterlab package normally
    registers its own kernel pointing at itself, so this may not be
    needed on Mac, but hasn't been verified against the "Start Jupyter"
    button in the app.
  - No [Files]-equivalent exclusions have been tuned; fort-pymdwizard's
    tests/ and .github/ are cloned along with everything else.
"""

import argparse
import plistlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

APP_NAME = "MetadataWizard"
BUNDLE_ID = "gov.usgs.metadatawizard"  # matches the pkgutil receipt on this
                                        # machine; the existing Info.plist
                                        # uses "usgs.metadatawizard" instead
                                        # -- confirm which is canonical
ENV_DIRNAME = "pymdwizard"
REPO_URL = "https://github.com/DOI-USGS/fort-pymdwizard.git"
DEFAULT_BRANCH = "main-v2.2"

# Real system git, not the git bundled in the app's conda env (that copy is
# broken -- see fort-pymdwizard-default-branch session notes).
GIT = "/usr/bin/git"

LAUNCHER_SCRIPT = """#!/bin/bash

DIR=$(dirname "$0")

# LaunchServices passes the Carbon process identifier to the application with
# -psn parameter - we do not want it
if [[ "${1}" == -psn_* ]]; then
    shift 1
fi

# Disable user site packages
export PYTHONNOUSERSITE=1

cd "${DIR}"/..
# Put the cloned fort-pymdwizard checkout on PYTHONPATH so the `pymdwizard`
# package is importable. This is resolved at runtime from the app's actual
# location ($(pwd) is Contents/ after the cd above), so it works regardless
# of where the app is installed (staging, /Applications, etc.) -- no build-
# time path is baked in.
export PYTHONPATH="$(pwd)/fort-pymdwizard${PYTHONPATH:+:$PYTHONPATH}"
# Use an absolute path to the bundled interpreter so we can never silently
# fall through to a system python (e.g. Homebrew's) if something about the
# bundle is off.
exec "$(pwd)/Frameworks/pymdwizard/bin/python" -m pymdwizard.MetadataWizard "$@"
"""

PIP_WRAPPER_SCRIPT = """#!/bin/bash

DIR=$(dirname "$0")

# Disable user site packages
export PYTHONNOUSERSITE=1

# change directory into conda environment
cd "${DIR}"/..
exec -a "$0" "$(pwd)/Frameworks/pymdwizard/bin/python" -m pip "$@"
"""


def run(cmd, **kw):
    print("+", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True, **kw)


def preflight():
    """Fail early, with a clear message, if the OS or any required external
    tool is missing -- rather than crashing partway through the build with a
    raw subprocess traceback."""
    if sys.platform != "darwin":
        sys.exit(
            "This installer build must run on macOS -- it uses sips, "
            "iconutil, and pkgbuild, which only exist there."
        )

    # git is referenced by absolute path (GIT); the rest must be on PATH.
    required = {
        "conda": "Miniforge/conda (needed to build the bundled environment)",
        "sips": "Xcode Command Line Tools (icon conversion)",
        "iconutil": "Xcode Command Line Tools (icon conversion)",
        "pkgbuild": "Xcode Command Line Tools (installer packaging)",
    }
    missing = [
        f"  - {name}: {why}"
        for name, why in required.items()
        if shutil.which(name) is None
    ]
    if not Path(GIT).exists():
        missing.append(
            f"  - git: expected at {GIT} "
            f"(install the Xcode Command Line Tools)"
        )
    if missing:
        sys.exit(
            "Missing required tool(s):\n"
            + "\n".join(missing)
            + "\n\nInstall the Xcode Command Line Tools with "
            "`xcode-select --install` and make sure conda is on your PATH."
        )


def get_version(repo: Path) -> str:
    text = (repo / "pymdwizard" / "__init__.py").read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', text)
    if not match:
        raise ValueError("Could not find __version__ in pymdwizard/__init__.py")
    return match.group(1)


def clone_source(contents: Path, branch: str) -> Path:
    dest = contents / "fort-pymdwizard"
    if dest.exists():
        shutil.rmtree(dest)
    run([GIT, "clone", "--branch", branch, REPO_URL, str(dest)])
    return dest


def build_conda_env(env_yml: Path, target: Path):
    if target.exists():
        shutil.rmtree(target)
    # Built directly at its final location so no paths need relocating
    # afterward (some installed console-script shebangs bake in the
    # build prefix).
    run(["conda", "env", "create", "-f", str(env_yml), "--prefix", str(target)])


def build_icon(repo: Path, resources: Path):
    ico = repo / "pymdwizard" / "resources" / "icons" / "Ducky.ico"
    iconset = resources / "Ducky.iconset"
    if iconset.exists():
        shutil.rmtree(iconset)
    iconset.mkdir(parents=True)

    # The .ico's largest embedded image is 256x256. Extract it to a PNG
    # once, then scale from that -- asking sips to convert straight from
    # .ico to a size above 256 (e.g. the 512 the iconset spec wants) fails
    # (sips error 13) even though scaling a PNG up works fine.
    base_png = iconset / "_source.png"
    run(["sips", "-s", "format", "png", str(ico), "--out", str(base_png)])

    for size in (16, 32, 128, 256, 512):
        run(["sips", "-z", str(size), str(size), str(base_png),
             "--out", str(iconset / f"icon_{size}x{size}.png")])
        run(["sips", "-z", str(size * 2), str(size * 2), str(base_png),
             "--out", str(iconset / f"icon_{size}x{size}@2x.png")])
    base_png.unlink()

    resources.mkdir(parents=True, exist_ok=True)
    run(["iconutil", "-c", "icns", str(iconset),
         "-o", str(resources / "Ducky.icns")])
    shutil.rmtree(iconset)


def write_info_plist(contents: Path, version: str):
    plist = {
        "CFBundleName": APP_NAME,
        "CFBundleExecutable": APP_NAME,
        "CFBundleIdentifier": BUNDLE_ID,
        "CFBundleGetInfoString": "MetadataWizard, FGDC metadata editor extraordinaire",
        "CFBundleVersion": version,
        "CFBundleShortVersionString": version,
        "CFBundleIconFile": "Ducky.icns",
        "CFBundlePackageType": "APPL",
        "CFBundleSignature": "mdwiz",
        "CFBundleInfoDictionaryVersion": "6.0",
        "NSPrincipalClass": "NSApplication",
        "NSHighResolutionCapable": True,
        "LSMinimumSystemVersion": "10.9.0",
    }
    with open(contents / "Info.plist", "wb") as f:
        plistlib.dump(plist, f)


def write_launchers(macos: Path):
    macos.mkdir(parents=True, exist_ok=True)

    launcher = macos / APP_NAME
    launcher.write_text(LAUNCHER_SCRIPT)
    launcher.chmod(0o755)

    pip_wrapper = macos / "pip"
    pip_wrapper.write_text(PIP_WRAPPER_SCRIPT)
    pip_wrapper.chmod(0o755)


def build_app_bundle(staging: Path, env_yml: Path, branch: str) -> tuple:
    app = staging / f"{APP_NAME}.app"
    if app.exists():
        shutil.rmtree(app)
    contents = app / "Contents"
    contents.mkdir(parents=True)

    fort_pymdwizard = clone_source(contents, branch)
    version = get_version(fort_pymdwizard)
    print(f"Building {APP_NAME} {version} ({branch}) at {app}")

    write_info_plist(contents, version)
    write_launchers(contents / "MacOS")
    build_icon(fort_pymdwizard, contents / "Resources")
    env_dir = contents / "Frameworks" / ENV_DIRNAME
    build_conda_env(env_yml, env_dir)
    # Note: the cloned fort-pymdwizard checkout is made importable at runtime
    # by the launcher (it puts Contents/fort-pymdwizard on PYTHONPATH), so no
    # .pth file is written here -- that avoids baking a build-time path that
    # would go stale once the app is relocated to /Applications.

    return app, version


def build_pkg(app: Path, output: Path, version: str):
    payload = app.parent / "pkg_payload"
    if payload.exists():
        shutil.rmtree(payload)
    apps_dir = payload / "Applications"
    apps_dir.mkdir(parents=True)
    shutil.copytree(app, apps_dir / app.name, symlinks=True)

    run([
        "pkgbuild",
        "--root", str(payload),
        "--identifier", BUNDLE_ID,
        "--version", version,
        "--install-location", "/",
        str(output),
    ])
    shutil.rmtree(payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument(
        "--env-yml", type=Path, required=True,
        help="Path to the pinned environment.yml "
             "(see environment-pinned.yml)",
    )
    parser.add_argument(
        "--staging", type=Path,
        default=Path(__file__).parent / "staging",
    )
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).parent / "MetadataWizard.pkg",
    )
    args = parser.parse_args()

    preflight()

    if not args.env_yml.exists():
        sys.exit(f"--env-yml file not found: {args.env_yml}")

    args.staging.mkdir(parents=True, exist_ok=True)
    app, version = build_app_bundle(args.staging, args.env_yml, args.branch)
    print(f"App bundle built: {app}")

    build_pkg(app, args.output, version)
    print(f"Installer built: {args.output}")
    print(
        "\nNOTE: this .pkg is unsigned and unnotarized. Before distributing "
        "it outside your own machine, add a `productsign --sign <identity>` "
        "step and notarize with `xcrun notarytool submit` / "
        "`xcrun stapler staple`."
    )


if __name__ == "__main__":
    main()
