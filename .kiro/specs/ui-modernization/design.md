# Design: Metadata Wizard UI modernization

Requirements are in `requirements.md`. Status and phase order are in `status.md`. This document says how each requirement is met, based on how the code works today. File and line references were read on 2026-11-25 on `feature/ui-modernization` (from `main-v2.2` at `a7c09c9`).

## 1. How the code works today

These facts drive the design.

**Navigation.** `MetadataRoot` (`gui/MetadataRoot.py`) holds a frame of six checkable `QToolButton`s (`idinfo_button`, `dataquality_button`, `spatial_button`, `eainfo_button`, `distinfo_button`, `metainfo_button`) above a `QStackedWidget` (`fgdc_metadata`). It is not a `QTabWidget`. The button order and the stack index order are the same, 0 to 5. `switch_section(i)` is the only function that changes the page. It is called by the buttons (through `section_changed`) and by `PyMdWizardMainForm.goto_error`. Advanced → Include Sections has four checkable actions (Data Quality, Spatial, Entity and Attribute, Distribution). They call `MetadataRoot.use_section`, which hides the page widget but leaves its button visible.

**Page content.** Identification, Data Quality, Spatial, Distribution and Metadata Reference each have one `QScrollArea` and expose it as `.scroll_area`. Entity and Attribute (`EA.py`) is a `QTabWidget` with west-side tabs and no `.scroll_area`. Within a page, the cards are the existing `QGroupBox`es inside each child widget. A `QGroupBox` is often the FGDC element itself (`fgdc_keywords`, `fgdc_descript`), so its object name drives `to_xml`, `from_xml` and validation lookup. Identification builds 14 widget groups in `IDInfo.build_ui` with `insertWidget(0, ...)`. `IdInfo.children()` also returns `spatial_tab.spdom`, which lives on the Spatial page but belongs to `idinfo` in the XML.

**Styling.** Every `WizardWidget` calls `setStyleSheet` on itself with a copy of `NORMAL_STYLE` (`wiz_widget.py`) in `set_stylesheet()`, again in `setup_dragdrop`, and on every mouse enter (`FOCUS_STYLE`) and leave. The font family is applied by a text `replace("Arial", family)`. About 60 generated `UI_*.py` files also contain stylesheets and fonts of their own. Qt gives a widget's own stylesheet priority over the application stylesheet for properties that conflict, and the two merge for properties that don't. So a central stylesheet can be introduced gradually: unconverted widgets keep their look, converted ones follow the theme.

**Validation.** `MainWindow.validate()` runs the XSD, calls `clear_validation()`, maps each error xpath to a widget with `make_tree().xpath_march()`, and calls `highlight_error`, which sets an object-name-scoped stylesheet on the widget. Two special cases: `highlight_attr` (attribute frame `fgdc_attr`, 16 object names) and `highlight_tab` (parent `QTabWidget`'s tab bar, 7 object names). `goto_error` maps the xpath's first segment to a section index (`idinfo/spdom` → 2) and calls `scroll_area.ensureWidgetVisible`. Three different reds are used (`MainWindow.py`, `theme.py`, `spdom.py`). Hovering a highlighted `WizardWidget` replaces its stylesheet and removes the highlight. `ErrorList.clear_errors()` clears the list widget but not `self.errors`.

**Settings.** `QSettings("USGS_" + __version__, "pymdwizard_" + __version__)` is built in five places: `core/utils.py:900` (`get_setting`, a new object per call), `gui/MainWindow.py:191`, `gui/settings.py:132`, `gui/detailed.py:162`, `gui/spatial_tab.py:163`.

**Other facts.**
- There is no unsaved-changes flag. `check_for_changes` compares the form's XML with the file only when closing.
- Status bar: a plain `QStatusBar`, used only for `showMessage`.
- `actionSave_as` and `actionAbout` are both bound to Ctrl+A, which Qt treats as ambiguous. Neither works. This is existing behavior and is not part of this work unless you decide otherwise (open decision 6).
- The Preview and Help dialogs are modal.
- Tests that pin current styling: `tests/test_spdom.py` (exact `styleSheet()` strings on the north/south fields). `test_mainwindow.py::test_validation` asserts `len(widget.error_list.errors) == 1`.
- The 224 existing tests pass today (baseline, 2026-11-25). Many tests find widgets by `fgdc_*` object name or `widget.ui.<name>`, so renaming or reparenting widgets is off limits.

## 2. Design principles

1. **Widgets keep their identity.** No `fgdc_*` object name, `ui.*` attribute, `to_xml` or `from_xml` changes. Layout and style change only. The XML output for any input must stay byte-identical, and a test checks this on the committed sample records.
2. **One navigation entry point.** `MetadataRoot.switch_section(i)` stays. The sidebar, `goto_error` and keyboard shortcuts all call it, so nothing else has to learn about the new navigation.
3. **Gradual migration through the cascade.** Introduce the central stylesheet first, then remove the old per-widget sheets one source at a time. Every merge request leaves a working app.
4. **No new imports.** Only PyQt5 modules already in the installer: `QtCore`, `QtGui`, `QtWidgets`, `QtSvg`, `QtWebEngineWidgets`. A CI job built from `environment.yml` enforces this.

## 3. Components

### 3.1 Styles package (Requirements 1, 4, 11)

New package `pymdwizard/gui/styles/` (not `theme`, which is the keyword widget).

| File | Contents |
|---|---|
| `tokens.py` | Named colors, spacing, radii, as module constants or a frozen dataclass. One source of truth. Includes the validation colors that are now duplicated. |
| `light.qss` | A `string.Template` file with `$name` placeholders for tokens. |
| `__init__.py` | `apply_theme(app)`: sets the Fusion style, builds the stylesheet from tokens and the user's font settings, calls `app.setStyleSheet`, and sets the application font. Calling it again re-applies everything. |
| `validation.py` | `set_validation(widget, state)`: sets the `validation` property (`error`, `warning`, `active-error`, or `None`) and unpolishes and polishes the widget. Also used by the inline messages (3.5). |
| `icons.py` | `load_icon(name)`: reads an SVG from `resources/icons/`, recolors it from tokens, and returns a `QIcon` with normal and disabled pixmaps (3.7). |

**Failure handling (1.4).** `apply_theme` catches a missing or unreadable `light.qss`, logs a warning, and returns after setting Fusion only.

**Fonts (1.6, 1.7).** `apply_theme` reads `fontfamily` and `fontsize` through the settings helper (3.2), applies `platform_font_pt` for macOS, and calls `QApplication.setFont`. During the transition the generated stylesheet also contains `font-family` and `font-size` rules for the selectors that `NORMAL_STYLE` covers today (QLabel, QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QRadioButton, QPushButton, QGroupBox). A stylesheet font rule beats a `setFont` call baked into a generated UI file, so widgets with a pinned `Arial` still follow the user's setting until phase 4b removes the pins. After 4b the `font-family` rules are deleted. The stylesheet uses `font-size` and `font-weight`, never the `font:` shorthand, so it doesn't reset the family.

**Settings dialog.** `Settings.save_settings` calls `apply_theme(QApplication.instance())` in place of `metadata_root.set_stylesheet(recursive=True)`.

**Hover and focus (1.5).** `QGroupBox:hover` and `*:focus` rules replace `enterEvent`/`leaveEvent`. `WizardWidget.set_stylesheet()` stays as a method that no longer sets a stylesheet, so subclasses and tests that call it keep working. `NORMAL_STYLE` and `FOCUS_STYLE` remain defined until `jupyterstarter.py` (which applies `NORMAL_STYLE` directly) is converted, then are deleted.

**macOS.** The macOS-only removal of `QPushButton` padding (`BUTTON_PADDING`) exists because native buttons turn flat when a box property is set. Fusion draws every button itself, so the workaround is no longer needed. Fusion will change the look of Mac controls from native Aqua to Fusion. Phase 1 (prototype) checks this on a Mac before it's committed to.

**Contrast (11.1).** `tests/test_styles.py` computes WCAG contrast for each text/background token pair and each border/background pair and fails below 4.5:1 or 3:1. Tokens are chosen to pass; the test keeps them passing.

**Focus indicator (11.2).** One `*:focus` rule gives every focusable control a visible outline.

### 3.2 Settings migration (Requirement 3)

A single helper in `core/utils.py`:

- `get_settings()` returns `QSettings("USGS", "pymdwizard")`. The org and app names have no version. The five existing constructions call it. `core/utils.py` already imports `QSettings`, so this adds no new dependency for `core/`.
- `migrate_settings()` runs once at startup, before the main window is built. If the new store has no `settings_migrated` key, it walks an ordered list of candidate old stores, newest first, and copies every key from the first one that is non-empty. It then writes `settings_migrated=True`. It never overwrites a key already present in the new store, and never touches the old store (3.5).
- Qt cannot list which organizations exist, so the candidate list is explicit, newest first: `2.2.1`, `2.2.0`, `2.1.1`, `2.1.0`, `2.0.8`. Each is tried as `QSettings("USGS_<v>", "pymdwizard_<v>")`. Git tags `v2.0.8`, `v2.1.0`, `v2.2.0` and `v2.2.1` all use this naming. 2.1.1 appears in `CHANGES.txt` but has no tag, so its naming is assumed and a missing store is simply skipped.
- Tests in `tests/test_mainwindow.py` that build `QSettings("USGS_2.2.0", "pymdwizard_2.2.0")` directly are updated to `get_settings()`.
- Lists such as `recentFileList` are copied as lists. Test that a one-item list stays a list after the copy.

This ships in the first release that uses the fixed name, which must not be later than the `__version__` change (3.4).

### 3.3 Sidebar (Requirement 5)

New widget `gui/sidebar.py`, `Sidebar(QListWidget-like)`. A custom widget on a `QListWidget` or a small `QListView` gives arrow-key navigation, selection, and accessibility for free. Each row shows an icon-or-count badge and the section name.

- `MetadataRoot.build_ui` builds a horizontal layout: sidebar on the left, the existing `QStackedWidget` on the right. The old button frame (`ui.frame` and its six buttons) is hidden in the first sidebar change and deleted in a later cleanup commit, so the objects `idinfo_button` etc. exist until nothing references them.
- Entries are in index order 0 to 5: Identification, Data Quality, Spatial, Entity and Attribute, Distribution, Metadata Reference. The names match the current button text.
- The sidebar emits `section_requested(int)`, connected to `MetadataRoot.switch_section`. `switch_section` updates the selected entry, so selection stays correct no matter who navigated.
- `use_section(which, value)` also calls `sidebar.set_entry_visible(index, value)`. This fixes the current behavior where a hidden section's button stays visible.
- Shortcuts: Ctrl+1 to Ctrl+6, defined as `QShortcut`s on the main window with `ApplicationShortcut` context. Ctrl+N is File → New and is not touched.
- Status per entry: `set_status(index, errors, warnings)`. A page with none shows a check icon; otherwise a count badge with an icon. Color is never the only signal (5.4).
- Accessible name: `"Identification, 1 error"`, set through `setAccessibleName` on each row's item data and updated by `set_status`.
- Page counts come from the Problems model (3.5). The xpath-to-page mapping that `goto_error` uses inline moves to one function, `section_index_for_xpath(xpath)`, used by both.

Identification stays one entry (Requirement 6). The sidebar takes its entries from a list, so a later split adds entries without changing the widget.

### 3.4 Cards and jump bar (Requirement 7)

**Card.** No new widget class. A card is the existing top-level `QGroupBox` of each child widget, styled by `light.qss`: surface background, a header drawn by `QGroupBox::title`, a thin border, and a rule that removes borders from group boxes nested inside another group box (`QGroupBox QGroupBox { border: none; }`). This avoids touching object names and layouts. Where a widget has an inner frame that draws its own border (`.QFrame` in `NORMAL_STYLE`), the rule moves into the theme and the border is dropped for nested frames.

**Jump bar.** New widget `gui/jump_bar.py`.
- `JumpBar(scroll_area, entries)` takes `(label, widget)` pairs. Each page class builds its list where it already builds its widgets (`IDInfo.build_ui` has the 14 groups). A button calls `scroll_area.ensureWidgetVisible(widget)` then `verticalScrollBar().setValue(widget.y() - margin)` so the card is at the top (7.4).
- Current-card highlight: on `verticalScrollBar().valueChanged`, pick the last entry whose widget's top (mapped to the scroll area's content) is at or above the viewport top plus a margin. Debounced with a 50 ms single-shot timer.
- Entries whose widget is hidden (`isVisible()` false, for example a hidden section) are skipped. A page shows a jump bar only when it has more than three visible entries (7.3).
- Entity and Attribute has no jump bar (7.6).
- Jump bar buttons are checkable `QToolButton`s with an accessible name (11.3) and keyboard focus.

**Sizes (7.7).** Several widgets set fixed minimum sizes (`fgdc_citeinfo.setMinimumSize(1000, 360)`, `WIDGET_WIDTH`, `resize()` with `EXPANDED_HEIGHT`). Phase 4c relaxes those per section, with a screenshot check at 1300×700 and at 150% scaling (`QT_SCALE_FACTOR=1.5`).

**Yes/No sections (7.5).** Nothing changes in `PointOfContact`, `proccont`, `citeinfo` and similar. The radio still drives `show()`/`hide()` and `has_content()`.

### 3.5 Validation, inline messages and Problems panel (Requirements 4, 8, 10)

**Property-based highlighting (Req. 4).**
`highlight_error`, `highlight_attr`, `highlight_tab` and `clear_validation` call `set_validation(widget, state)` instead of `setStyleSheet`. The three stylesheet cases become theme rules:

```
QWidget[validation="error"]        { background: $error_bg; border: 2px solid $error_border; }
QWidget[validation="active-error"] { background: $error_bg_active; border: 4px solid $error_border_active; }
QFrame[validation="error"]         { ... }            /* fgdc_attr frame */
QTabWidget[validation="error"] QTabBar { background: $error_tab; }
```

The type-selector forms match only the widget that carries the property, not its descendants, so unlike `QWidget#name` there is no accidental cascade. `set_validation` calls `style().unpolish(w); style().polish(w)` because Qt does not re-evaluate property selectors on its own. The same function handles the north/south cue in `spdom.py` (`NS_ERROR_FIELD_STYLE`), which becomes `set_validation(field, "error")`, and the unknown-keyword highlight in `theme.py`. `tests/test_spdom.py` changes from comparing stylesheet strings to checking the `validation` property.

Because the theme sheet is no longer swapped on hover (3.1), the highlight survives hovering. `apply_opacity_effect(line_edit, 0.95)` in `highlight_error` is not undone by `clear_validation` today; it is removed, because the accent bar and message replace it. How the new highlighting looks is reviewed once it exists (open decision 4).

**Accent bar (4.5).** For `error` and `active-error`, the stylesheet adds a thick left edge in the error color in addition to the tint, so state is not color-only.

**Inline messages (8.1).** `styles/validation.py` also provides `show_message(widget, text)` and `clear_message(widget)`. A small `QLabel` (object name `validation_message`, role-styled) is inserted directly after the widget in its parent layout:
- `QBoxLayout`: `insertWidget(index + 1, label)`.
- `QFormLayout`: inserted as a new row after the field's row.
- `QGridLayout` or no layout match: the label goes at the top of the nearest enclosing card (`QGroupBox`) instead of directly below the field.

Labels are created lazily, kept in a dict on the form for cleanup, and deleted by `clear_validation`. They are also set as the field's `accessibleDescription`. **Risk:** FGDC fields live in about 70 different generated layouts. Phase 7 starts with a survey of which layout types the validated fields use, and the fallback is a deliberate design choice, not a failure (open decision 5).

**Problems panel (8.2 to 8.5).**
- A `Problem` record: `severity`, `section` (page index and name), `message`, `xpath`, and a weak reference to the widget.
- `ErrorList` keeps its public names (`add_error`, `clear_errors`, `errors`) so `test_validation` and `goto_error` keep working. Its `clear_errors` also empties `self.errors`. It becomes the panel's content: a `QTreeWidget` or `QTableWidget` with Severity, Section and Message columns, grouped by section.
- `PyMdWizardMainForm.build_ui` replaces `error_list_dialog` with a `QDockWidget` at the bottom. The existing `QMessageBox` summary after validation is dropped in favor of the panel opening, since the panel states the count. Closing and reopening: Validate menu entry "Show Problems Panel" (checkable) and the status bar counts (8.5).
- Selecting a row calls `goto_error`, which now: switches the page through `switch_section`, scrolls with `ensureWidgetVisible`, focuses the widget, and sets `active-error` through `set_validation`. Restoring the previous active field uses `set_validation(prev, "error")`.
- Today the XSD validator produces only errors. Warnings appear in the model so the panel and sidebar can show them, and the thesaurus check (`feature/thesaurus-controlled-vocab-validation`) is the natural first source. No warning source is added in this work.

**Status bar (Requirement 10).** Three permanent widgets added with `addPermanentWidget`: a save-state label, a problems-count button (toggles the panel), and the last-saved time. `showMessage` calls keep working.

**Unsaved-changes tracking (10.1).** A `RecordState` object on the main window stores the serialized XML at load and at save (`xml_utils.node_to_string(metadata_root.to_xml())`). A debounced single-shot timer (800 ms) recomputes after key and mouse release events caught by one event filter on `metadata_root`, and compares with the stored snapshot. If `to_xml()` on a full record is too slow, the fallback is to compare on focus change only. Phase 0 measures `to_xml()` time on the sample records. The existing `check_for_changes` on exit stays as it is.

### 3.6 Toolbar (Requirement 9)

A `QToolBar` added in `PyMdWizardMainForm.build_ui`. It uses the existing `QAction` objects (`actionNew`, `actionOpen`, `actionSave`, `actionRun_Validation`, `actionPreview`, `generate_review`), so the slots, shortcuts and enabled state (for example `generate_review` disabled when `python-docx` is missing) are shared with the menu automatically. Each action gets an icon via `load_icon` and a tooltip of the form `"Save (Ctrl+S)"` built from `action.shortcut()`.

**Icons.** A committed set of SVGs under `pymdwizard/resources/icons/` (the folder exists), with the license file beside them. `load_icon` reads the SVG text, substitutes `currentColor` with a token color, renders with `QtSvg.QSvgRenderer` into a `QPixmap` at 1x and 2x, and registers `QIcon.Normal` and `QIcon.Disabled` pixmaps. Candidate set: Lucide (ISC), Tabler (MIT), Material Symbols (Apache 2.0). Proposal: Lucide, for consistent stroke style and the simplest license (open decision 3).

### 3.7 `.ui` cleanup and regeneration (Requirement 13)

Baseline findings (2026-11-25), 69 `UI_*.py` files checked by AST comparison with pyuic 5.15.11:
- 36 are identical after normalization.
- 33 differ. Most are version noise (pyuic 5.6 `setContentsMargins(0,0,0,0)` lines, the `__main__` block). These files regenerate safely.
- These differ in ways that matter and need a decision per file before regeneration: `UI_Preview.py` (hand-written `QWebView` → `QWebEngineView` fallback), `UI_taxoncl.py` (different class name and structure from its `.ui`), `UI_ThesaurusSearch.py`, `UI_useconst.py`, `UI_citeinfo.py` (a label text differs), `UI_Taxonomy.py`, `UI_spref.py`.
- Four `.ui` files have no `UI_` file and no references: `Citation.ui`, `ThemeKeywords2.ui`, `date_widget.ui`, `keyword_repeater.ui`.

Plan:
- Phase 4a adds a regeneration script (location to be chosen, for example next to the `.ui` files) that runs from `ui_files/` so icon paths stay relative. For each differing file, the hand edit is either moved into the `.ui` file or into the Python widget class (for example, the `QWebView` fallback goes into `Preview.py`), then regenerated. Regeneration commits contain only regeneration.
- `UI_Taxonomy.py` and `UI_taxonomy.py` are one file on Windows. The workspace rule applies: both index entries must carry the same blob after any change.
- Phase 4b removes `QFont("Arial")` pins and per-widget font stylesheets from `.ui` files, and replaces bold or italic with a `class` property styled by the theme.
- Phase 4c adjusts size constraints, one section per merge request.

### 3.8 Continuous integration (Requirement 12)

New `.github/workflows/tests.yml`, separate from `build-macos-installer.yml`.
- Matrix: `windows-latest`, `ubuntu-latest`.
- Steps: check out, set up conda (`conda-incubator/setup-miniconda`) with `environment-file: environment.yml`, cache keyed on `hashFiles('environment.yml')`, run `pytest tests --no-network -q` with `QT_QPA_PLATFORM=offscreen`.
- Tests marked `network` are skipped (`--no-network`).
- On Linux, Qt WebEngine may need `QTWEBENGINE_CHROMIUM_FLAGS=--no-sandbox`. This is checked on the first run.
- Because the build starts from `environment.yml`, a missing dependency or an import outside that file fails there (2.4). CI uses the conda environment, while the local development Python is the installer's. A mismatch between them would show up as a CI-only failure and is worth finding early.

## 4. Order and dependencies

The order in `status.md` stands, with these dependencies recorded:
- Phase 3b (remove the per-widget stylesheet and hover swap) needs phase 3a first. It does not need 4b, because the transitional font rules in the stylesheet (3.1) keep the family and size setting working for widgets that still pin `Arial`.
- Phase 3c (property-based validation) needs 3b first, or hovering still wipes highlights on widgets that keep their own sheet.
- Phase 7 (Problems panel, inline messages, status bar) needs the sidebar (phase 5) for page counts, and 3c for the property mechanism.
- Phase 6 (cards, jump bar) needs 3a and 3b so the card look comes from the theme.
- `UI_Taxonomy.py` / `UI_taxonomy.py` changes need the two-index-entry procedure.

## 5. Testing

- **Regression.** The existing 224 tests must pass at every merge request. `test_spdom.py` is updated in phase 3c.
- **XML invariance.** A test loads each record in `tests/data/`, writes `to_xml()` before the redesign branch and after, and compares serialization. Run in CI at every merge request.
- **Theme.** `test_styles.py`: `apply_theme` with a missing QSS logs a warning and doesn't raise (1.4); token contrast (11.1); after `apply_theme`, a widget's `font().family()` or stylesheet rule reflects the setting (1.6).
- **Validation.** `set_validation` sets the property and repolishes (a styled widget changes its reported palette or `styleSheet`-resolved color); `clear_validation` resets it; no `setStyleSheet` calls remain in `highlight_*` (4.4), checked with a grep-style test.
- **Settings.** In a temporary `QSettings` location: migration copies values, runs once, doesn't overwrite, leaves the old store alone (Requirement 3).
- **Sidebar.** Selection and `switch_section` stay in sync; hiding an optional section hides its entry; Ctrl+1..6; accessible names include counts.
- **Jump bar.** Builds only above three entries; scrolls; highlights the current card.
- **Accessibility.** Every new control has a non-empty accessible name.
- **Manual.** Windows and macOS screenshots before and after each visual merge request (see `status.md`), including 1300×700 and 150% scaling.

## 6. Risks

| Risk | Effect | Mitigation |
|---|---|---|
| Fusion changes the Mac look | Users on macOS see non-native controls | Prototype on a Mac in phase 1 before committing |
| Remaining widget-level stylesheets in generated UI files override the theme | Part of a page looks old | Phase 3d audit script lists remaining `setStyleSheet` calls; fixed in `.ui` files |
| Inline message cannot be inserted below some fields | Message appears at card level, not beside the field | Fallback defined in 3.5; survey in phase 7 |
| Unsaved-changes check is slow on large records | UI stutter | Measure in phase 0, fall back to focus-change checks |
| A `UI_*.py` regeneration drops a hand edit | Runtime failure (for example the Preview) | Phase 4a resolves each differing file before regenerating; tests |
| Settings migration misses an old version | A user's preferences reset | Explicit candidate list from the release history; manual test with a 2.2.0 and 2.2.1 store |
| CI environment differs from the installer environment | Passes locally, fails in CI, or the reverse | Compare package versions in phase 0 |
| Settings keys are written as `str` instead of `list` | `recentFileList` breaks after migration | Test for a one-item list |

## 7. Open decisions

1. **Identification:** one page for now (decided). The split is deferred.
2. **Released versions that stored settings:** resolved from the release tags (see 3.2).
3. **Icon set:** Lucide (decided 2026-11-25).
4. **`apply_opacity_effect` in `highlight_error`:** removed (decided 2026-11-25). The new highlighting is new visual design, so its appearance is reviewed after it is built and adjusted then.
5. **Inline message fallback:** when a field has no insertable position, show the message at the top of its card (decided 2026-11-25).
6. **Duplicate Ctrl+A on Save as and About:** fix in an early merge request (decided 2026-11-25). Save as becomes Ctrl+Shift+S, the standard shortcut. About gets no shortcut, because Ctrl+A is "select all" in every text field and About is rarely used. The docs don't mention either shortcut. `UI_MainWindow.py` is one of the files that can't be regenerated blindly (3.7), so the early fix sets the two shortcuts in `PyMdWizardMainForm.build_ui` after `setupUi`. Phase 4 changes them in `MainWindow.ui` too and removes the override.
7. **Settings names:** `QSettings("USGS", "pymdwizard")` (decided 2026-11-25).
