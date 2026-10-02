# MetadataWizard macOS installer build

Builds an unsigned macOS distributable for MetadataWizard from a
`fort-pymdwizard` branch (default `main-v2.2`), in one of two formats
(`--format`):

- **`pkg`** (default) — a `pkgbuild` installer that installs the app to
  `/Applications`.
- **`dmg`** — a laid-out ("pretty") drag-to-install disk image built with
  [`create-dmg`](https://github.com/create-dmg/create-dmg): the window shows
  the app icon and an `/Applications` drop target, compressed read-only
  (UDZO).

Both formats share the same `MetadataWizard.app` bundle; only the final
packaging step differs.

The build **must run on macOS** — `build_installer.py` shells out to `sips`,
`iconutil`, and `pkgbuild`/`hdiutil`, which only exist there (and, for `dmg`,
`create-dmg`). Since development happens on Windows, the intended path is to
run the build on a macOS CI runner.

These build files live on a dedicated `macos-build` branch (off `main-v2.2`),
not on `main-v2.2` itself, so they never land in users' installed apps via the
in-app "check for updates" feature.

## Files

- `build_installer.py` — the build script. `--format pkg|dmg` selects the
  output; `--output` defaults to `MetadataWizard.<format>`.
- `environment-pinned.yml` — the conda environment, with a few versions pinned
  to avoid known problems (see comments at the top of that file — notably
  `habanero`, where >= 2.9.2 breaks DOI import from DataCite).

## Running in CI

Two configs are provided at the repo root:

- `.github/workflows/build-macos-installer.yml` — GitHub Actions. Uses a
  GitHub-hosted `macos-14` runner (no Mac hardware needed). Run it from the
  Actions tab via "Run workflow", selecting the `macos-build` branch, then
  pick the fort-pymdwizard branch to package and the **Output format** (`pkg`
  or `dmg`) from the dropdowns. The result is uploaded as the
  `MetadataWizard-<format>` artifact (`MetadataWizard-pkg` or
  `MetadataWizard-dmg`). For `dmg` builds the workflow `brew install`s
  `create-dmg` first.
- `.gitlab-ci.yml` — GitLab CI. Requires a macOS runner (hosted macOS runners
  on gitlab.com are a paid opt-in tier; self-managed GitLab needs your own Mac
  runner). Run the manual `build-macos-installer` job; set the `BUILD_FORMAT`
  variable (`pkg` or `dmg`) under Run pipeline → Variables to choose the
  format. The result is published as the `MetadataWizard-<format>` job
  artifact.

Both install Miniforge on the runner (macOS runners don't ship conda) and then
invoke `build_installer.py`. The conda solve is the slow part.

> Note: the CI branch and the packaged branch are independent. CI runs the
> workflow from whatever branch you launch it on (`macos-build`), but
> `build_installer.py` clones a fresh copy of `fort-pymdwizard` from GitHub at
> `--branch` (default `main-v2.2`), so the installer contains the release
> code, not the build branch's code.

## Running locally on a Mac

A `pkg` (default):

```
python3 build_installer.py --env-yml environment-pinned.yml
```

Produces `MetadataWizard.pkg`. Install with
`sudo installer -pkg MetadataWizard.pkg -target /`, or double-click in Finder
(right-click → Open the first time, since it's unsigned).

A `dmg` (needs `create-dmg`: `brew install create-dmg`):

```
python3 build_installer.py --env-yml environment-pinned.yml --format dmg
```

Produces `MetadataWizard.dmg`. Open it in Finder, drag **MetadataWizard** onto
the **Applications** shortcut, then eject the disk image. Because it's
unsigned, the first launch needs right-click → Open to get past Gatekeeper.

## Not signed / not notarized

Gatekeeper will warn or block either format on other machines. For testing on
your own machine this is fine (right-click → Open). Before distributing beyond
your own machine you need an Apple Developer ID and must sign + notarize:

- **pkg**: `productsign --sign "Developer ID Installer: …"` on the `.pkg`,
  then `xcrun notarytool submit` / `xcrun stapler staple`.
- **dmg**: `codesign` the `.app` bundle (`Developer ID Application: …`) before
  building the dmg, then `notarytool submit` / `stapler staple` the dmg.

The exact commands are stubbed as TODO comments in `build_pkg()` /
`build_dmg()` in `build_installer.py`.
