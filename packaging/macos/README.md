# MetadataWizard macOS installer build

Builds an unsigned `.pkg` installer for MetadataWizard from a `fort-pymdwizard`
branch (default `main-v2.2`).

The build **must run on macOS** — `build_installer.py` shells out to `sips`,
`iconutil`, and `pkgbuild`, which only exist there. Since development happens
on Windows, the intended path is to run the build on a macOS CI runner.

These build files live on a dedicated `macos-build` branch (off `main-v2.2`),
not on `main-v2.2` itself, so they never land in users' installed apps via the
in-app "check for updates" feature.

## Files

- `build_installer.py` — the build script.
- `environment-pinned.yml` — the conda environment, with a few versions pinned
  to avoid known problems (see comments at the top of that file — notably
  `habanero`, where >= 2.9.2 breaks DOI import from DataCite).

## Running in CI

Two configs are provided at the repo root:

- `.github/workflows/build-macos-installer.yml` — GitHub Actions. Uses a
  GitHub-hosted `macos-14` runner (no Mac hardware needed). Run it from the
  Actions tab via "Run workflow", selecting the `macos-build` branch, and pick
  the fort-pymdwizard branch to package. The `.pkg` is uploaded as the
  `MetadataWizard-pkg` artifact.
- `.gitlab-ci.yml` — GitLab CI. Requires a macOS runner (hosted macOS runners
  on gitlab.com are a paid opt-in tier; self-managed GitLab needs your own Mac
  runner). Run the manual `build-macos-installer` job; the `.pkg` is published
  as a job artifact.

Both install Miniforge on the runner (macOS runners don't ship conda) and then
invoke `build_installer.py`. The conda solve is the slow part.

> Note: the CI branch and the packaged branch are independent. CI runs the
> workflow from whatever branch you launch it on (`macos-build`), but
> `build_installer.py` clones a fresh copy of `fort-pymdwizard` from GitHub at
> `--branch` (default `main-v2.2`), so the installer contains the release
> code, not the build branch's code.

## Running locally on a Mac

```
python3 build_installer.py --env-yml environment-pinned.yml
```

Produces `MetadataWizard.pkg`. Install with
`sudo installer -pkg MetadataWizard.pkg -target /`, or double-click in Finder
(right-click → Open the first time, since it's unsigned).

## Not signed / not notarized

Gatekeeper will warn or block this on other machines. Before distributing
beyond your own machine, add a `productsign --sign <identity>` step on the
`.pkg` and notarize with `xcrun notarytool submit` / `xcrun stapler staple`
— needs an Apple Developer ID.
