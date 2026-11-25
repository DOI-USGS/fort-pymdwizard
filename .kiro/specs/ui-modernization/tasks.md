# Tasks: Metadata Wizard UI modernization

Requirements: `requirements.md`. Design: `design.md`. Status and decisions: `status.md`.

## Conventions for every task

- Each numbered phase is one or more merge requests into `feature/ui-modernization`. Branch each from `feature/ui-modernization` with a name such as `feature/ui-<topic>`.
- Before a merge request: run the full test suite (it must still show 224 passed or more, 0 failed), add tests for new behavior in the existing `tests/test_<module>.py` for that module, update `CHANGES.txt`, and add before and after screenshots to the description for visual changes (Windows, plus macOS where noted).
- The XML a record produces must not change. The invariance test from phase 0 runs in every merge request.
- Commit messages are shown to the user for approval before committing. Stage files by name.
- A commit that touches `UI_Taxonomy.py` / `UI_taxonomy.py` follows the two-index-entry procedure in the workspace workflow rule.
- Requirement numbers in brackets show what each task satisfies.

## Phase 0: Preparation

- [ ] 0.1 Save the baseline: record the 224 passed / 11 skipped result and the 36-of-69 pyuic comparison in `status.md` (done 2026-11-25).
- [ ] 0.2 Add a test that loads every record in `tests/data/` that the app can open, and compares `to_xml()` output with a stored snapshot (stored under `tests/data/`). It is the guard for the "XML must not change" rule. [R6.4 intent, design principle 1]
- [ ] 0.3 Measure `to_xml()` time on the sample records, and record it in `status.md`. It decides how unsaved-changes tracking works in phase 7. [R10.1]
- [ ] 0.4 Add `.github/workflows/tests.yml`: Windows and Linux hosted runners, environment built from `environment.yml`, environment cache keyed on `environment.yml`, `pytest tests --no-network -q` with `QT_QPA_PLATFORM=offscreen`. Leave `build-macos-installer.yml` unchanged. First run on Linux may need `QTWEBENGINE_CHROMIUM_FLAGS=--no-sandbox`. [R12, R2.4]
- [ ] 0.5 Compare the package versions in `environment.yml` with the installer environment, and note any mismatch in `status.md`. [R2]
- [ ] 0.6 Take baseline screenshots of each section with `widget.grab()` at 1300×700, and store them outside the repo (a screenshots folder the user chooses).
- [ ] 0.7 Fix the shortcut conflict: in `PyMdWizardMainForm.build_ui`, set Save as to Ctrl+Shift+S and remove the About shortcut after `setupUi`. Add a test that no two actions share a shortcut. (The `.ui` file is changed in phase 4.)

## Phase 1: Prototype (throwaway, not merged)

- [ ] 1.1 On `feature/ui-prototype`, build a standalone script with real widgets and dummy data: sidebar, card page, jump bar, toolbar, Problems panel, status bar, in the proposed colors.
- [ ] 1.2 Check rendering on Windows and on a Mac under Fusion, at 100% and 150% scaling.
- [ ] 1.3 Check that the colors meet the contrast targets, and settle the token values.
- [ ] 1.4 Show the prototype to a few regular users and record their feedback in `status.md`.
- [ ] 1.5 Decide go or no-go on Fusion for macOS. Delete the prototype branch afterwards.

## Phase 2: Settings migration [R3]

- [ ] 2.1 Add `get_settings()` and `migrate_settings()` to `core/utils.py`, using `QSettings("USGS", "pymdwizard")`. Migration order: 2.2.1, 2.2.0, 2.1.1, 2.1.0, 2.0.8, from the first non-empty store, once, without overwriting existing keys, leaving the old store untouched.
- [ ] 2.2 Replace the five `QSettings("USGS_" + __version__, ...)` constructions (`core/utils.py`, `MainWindow.py`, `settings.py`, `detailed.py`, `spatial_tab.py`) with `get_settings()`. Call `migrate_settings()` once in `launch_main` before the main window is built.
- [ ] 2.3 Update tests that construct `QSettings("USGS_2.2.0", "pymdwizard_2.2.0")` directly (`test_mainwindow.py`).
- [ ] 2.4 Tests: values copied; runs once; existing values not overwritten; old store unchanged; a one-item `recentFileList` stays a list. Manual check: install state from 2.2.1, start the branch, confirm recent files, template and font carry over.

## Phase 3: Styling infrastructure

### 3a Styles package [R1.1 to R1.4, R11.1, R11.2]
- [ ] 3a.1 Create `pymdwizard/gui/styles/` with `tokens.py`, `light.qss` (template), and `apply_theme(app)`. Set Fusion, build the stylesheet from tokens, apply the font from the user's settings (with `platform_font_pt`), set the application font.
- [ ] 3a.2 Include transitional `font-family` and `font-size` rules for the selectors that `NORMAL_STYLE` covers, so pinned fonts still follow the Settings dialog.
- [ ] 3a.3 Handle a missing or unreadable stylesheet: log a warning, keep Fusion defaults, do not crash.
- [ ] 3a.4 Call `apply_theme` from `launch_main`. Add a `themed_app` fixture to `conftest.py` for tests that need it.
- [ ] 3a.5 Add `*:focus` and `QGroupBox:hover` rules.
- [ ] 3a.6 Make the Settings dialog call `apply_theme` instead of `metadata_root.set_stylesheet(recursive=True)`.
- [ ] 3a.7 Tests in `tests/test_styles.py`: missing stylesheet does not raise; token contrast pairs meet 4.5:1 and 3:1; the font setting reaches widgets.

### 3b Remove per-widget stylesheet swapping [R1.5, R1.6]
- [ ] 3b.1 Make `WizardWidget.set_stylesheet()` stop calling `setStyleSheet`, keeping the method for callers. Delete the `enterEvent`/`leaveEvent` style swap and the `in_context` dependence on it.
- [ ] 3b.2 Convert `jupyterstarter.py` (applies `NORMAL_STYLE` directly), then delete `NORMAL_STYLE`, `FOCUS_STYLE`, `ERROR_STYLE`, `ERROR_FOCUS_STYLE` and the macOS button workaround.
- [ ] 3b.3 Compare before and after screenshots for every section (Windows and macOS). Fix anything that lost its look.

### 3c Validation through widget properties [R4]
- [ ] 3c.1 Add `styles/validation.py` with `set_validation(widget, state)` (property plus unpolish and polish). Add the `validation` rules to `light.qss`, including an accent bar so state is not color only.
- [ ] 3c.2 Change `highlight_error`, `highlight_attr`, `highlight_tab` and `clear_validation` in `MainWindow.py` to use it. Remove the opacity effect.
- [ ] 3c.3 Change `spdom.py` (north/south cue) and `theme.py` (unknown keyword) to use it.
- [ ] 3c.4 Update `tests/test_spdom.py` to check the property instead of the stylesheet string. Add tests: set, clear, no `setStyleSheet` left in the highlight functions, state survives a mouse enter.
- [ ] 3c.5 Review how the new highlighting looks and adjust the tokens.

### 3d Remaining colors [R1.3]
- [ ] 3d.1 Move the remaining hard-coded colors in `gui/*.py` into tokens.
- [ ] 3d.2 Add a script (kept outside the repo or in `tools/` if you want it kept) that lists every remaining `setStyleSheet` in `gui/*.py` and in `UI_*.py`, so phase 4 knows what is left.

## Phase 4: `.ui` cleanup [R1.7, R13]

### 4a Regeneration script
- [ ] 4a.1 Add a regeneration script that runs pyuic5 from `ui_files/`. Commit it on its own.
- [ ] 4a.2 For each differing file, move the hand edit into the `.ui` file or into the widget's Python class, then regenerate. Order: `UI_Preview.py` (move the `QWebView` fallback into `Preview.py`), `UI_taxoncl.py`, `UI_ThesaurusSearch.py`, `UI_useconst.py`, `UI_citeinfo.py`, `UI_Taxonomy.py`, `UI_spref.py`, `UI_MainWindow.py` (also remove the Ctrl+A shortcuts here and drop the override from 0.7), then the rest.
- [ ] 4a.3 Decide on the four `.ui` files with no generated file (`Citation.ui`, `ThemeKeywords2.ui`, `date_widget.ui`, `keyword_repeater.ui`): delete them or generate them.
- [ ] 4a.4 Each regeneration commit contains regeneration only. Run the full suite after each batch.

### 4b Remove font pins
- [ ] 4b.1 Remove `Arial` and `MS Shell Dlg 2` fonts and per-widget font stylesheets from the `.ui` files, and regenerate. Express bold or italic as a `class` property styled by the theme.
- [ ] 4b.2 Delete the transitional `font-family` rules from `light.qss`.
- [ ] 4b.3 Test: change the font in Settings and check labels, inputs and group boxes in every section follow it.

### 4c Size constraints (one section per merge request) [R7.7]
- [ ] 4c.1 Identification
- [ ] 4c.2 Metadata Reference
- [ ] 4c.3 Distribution
- [ ] 4c.4 Data Quality
- [ ] 4c.5 Spatial
- [ ] 4c.6 Entity and Attribute

Each one removes fixed minimum and maximum sizes that block resizing, then checks the page at 1300×700 and at 150% scaling.

## Phase 5: Sidebar [R5, R6]

- [ ] 5.1 Add `gui/sidebar.py`: a list of six entries in index order, with a badge area for status, arrow-key navigation, and accessible names.
- [ ] 5.2 In `MetadataRoot.build_ui`, add the sidebar to the left of the stacked widget, connect `section_requested` to `switch_section`, and make `switch_section` update the selection. Hide the old button frame.
- [ ] 5.3 Make `use_section` show or hide the matching sidebar entry.
- [ ] 5.4 Add Ctrl+1 to Ctrl+6 shortcuts.
- [ ] 5.5 Move the xpath-to-page mapping from `goto_error` into one function, `section_index_for_xpath`.
- [ ] 5.6 Add `set_status(index, errors, warnings)` (not yet fed by validation).
- [ ] 5.7 Delete the old button frame and its six `QToolButton`s once nothing references them.
- [ ] 5.8 Tests: selection stays in step with `switch_section`; hiding a section hides its entry; shortcuts; accessible names.

## Phase 6: Cards and jump bar [R7]

- [ ] 6.1 Add card styling to `light.qss` (surface, header from `QGroupBox::title`, no nested borders) and check it on Identification.
- [ ] 6.2 Add `gui/jump_bar.py` with scrolling and current-card highlighting. Tests for threshold (more than three visible entries), scrolling and highlight.
- [ ] 6.3 Roll out one section per merge request, in this order:
  - [ ] Identification (14 groups from `IDInfo.build_ui`)
  - [ ] Metadata Reference
  - [ ] Distribution
  - [ ] Data Quality
  - [ ] Spatial
  - [ ] Entity and Attribute (theme only, no jump bar)
- [ ] 6.4 Confirm the Yes/No sections (Point of Contact, Process Contact and others) behave exactly as before, including `has_content()`.

## Phase 7: Validation experience [R8, R10, R4.5]

- [ ] 7.1 Survey which layout types the validated fields use, to confirm the inline-message placement rules (box, form, fallback to the top of the card).
- [ ] 7.2 Add `show_message` and `clear_message` and the message label style. Wire into `highlight_error` and `clear_validation`.
- [ ] 7.3 Replace the error dialog with a dockable Problems panel at the bottom. Keep `ErrorList.add_error`, `clear_errors` and `errors`, and make `clear_errors` empty `errors` too. Drop the summary message box.
- [ ] 7.4 Update `goto_error` to switch page, scroll, focus the field and mark it `active-error`.
- [ ] 7.5 Feed `set_status` on the sidebar from the validation results.
- [ ] 7.6 Add Validate menu entry and status bar toggle for the panel.
- [ ] 7.7 Add unsaved-changes tracking (design 3.5), the save-state label, last-saved time and the error and warning counts in the status bar.
- [ ] 7.8 Tests: `test_validation` still passes; panel rows; clicking a row navigates and sets `active-error`; counts update on validate and clear; unsaved state toggles after an edit and clears after save.

## Phase 8: Toolbar [R9]

- [ ] 8.1 Add Lucide SVG icons for New, Open, Save, Validate, Preview and Review Report under `pymdwizard/resources/icons/`, with the license file.
- [ ] 8.2 Add `styles/icons.py` (`load_icon`) that recolors from tokens and provides normal and disabled states.
- [ ] 8.3 Add the toolbar using the existing menu `QAction`s, with tooltips that show the shortcut.
- [ ] 8.4 Tests: each toolbar action is the same object as the menu action; tooltip includes the shortcut; disabled Review Report when `python-docx` is missing; icons render at 1x and 2x.

## Phase 9: Accessibility check [R11]

- [ ] 9.1 Check every new control for an accessible name, a visible focus indicator and keyboard use (sidebar, jump bar, toolbar, Problems panel).
- [ ] 9.2 Run the contrast test and a manual pass with a screen reader on Windows (Narrator).

## Phase 10: Release [R14]

- [ ] 10.1 Set `__version__` to 2.3.0. Confirm phase 2 is already merged.
- [ ] 10.2 Write the `CHANGES.txt` entry for the user-visible changes.
- [ ] 10.3 Update `docs/usage/` text and screenshots to the new layout, then rebuild the HTML.
- [ ] 10.4 Note in the release notes that future installers must be built from a `main-v2.2` checkout.
- [ ] 10.5 Confirm CI passes on Windows and Linux, then merge `feature/ui-modernization` into `main-v2.2` (not into `master`).
- [ ] 10.6 Test the update path: from a 2.2.1 installation, run Help → Check for Updates and confirm the app starts without any package install.

## Phase 11: Later enhancements [R15]

- [ ] 11.1 Completeness ring in the sidebar header.
- [ ] 11.2 Removable chips for originators and keywords.
- [ ] 11.3 Ctrl+K field search.
- [ ] 11.4 Light, dark and system theme with a persisted choice.
