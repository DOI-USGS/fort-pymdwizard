# Requirements: Metadata Wizard UI modernization

## Introduction

This work modernizes the Metadata Wizard interface. It adds a left sidebar for navigation, a card-based layout for each section, inline validation messages, a Problems panel, a toolbar, and one central theme. The goal is to make the app easier to read and to move around in, without changing what metadata it produces.

Constraints:
- Development happens on `feature/ui-modernization` on GitLab (code.usgs.gov). Each phase is its own merge request into that branch. The finished work merges into `main-v2.2` as release v2.3.0.
- Users receive updates through the in-app updater, which runs `git merge` from the GitHub mirror into their installed checkout. **No change may require a Python package that the current installer environment lacks.**
- PyQt5 5.15.11 on Python 3.13, as pinned in `environment.yml`.

## Glossary

- **Wizard:** the Metadata Wizard desktop application.
- **Section:** a top-level part of the record that currently has its own tab: Identification, Data Quality, Spatial, Entity and Attribute, Distribution, Metadata Reference.
- **Page:** what the sidebar shows when an entry is selected. Every section is one page, except Identification, which becomes two (Requirement 6).
- **Card:** a visually separated block on a page that holds one existing widget group, such as Citation or Point of Contact.
- **Jump bar:** a row of buttons at the top of a page that scrolls the page to a card. It does not hide or move content.
- **Theme:** the central stylesheet plus its color, spacing and font tokens.
- **Installer environment:** the conda environment shipped by the current Windows and macOS installers, defined by `environment.yml`.
- **Problem:** a validation error or warning reported for a specific field.

## Requirements

### Requirement 1: Central theme

**User story:** As a maintainer, I want all styling defined in one place, so that visual changes don't need edits across dozens of files.

**Acceptance criteria**
1. WHEN the Wizard starts, THE Wizard SHALL use the Qt Fusion style on every platform.
2. WHEN the Wizard starts, THE Wizard SHALL load one application-wide stylesheet from the `pymdwizard/gui/styles/` package.
3. THE Wizard SHALL define colors, spacing and corner radii as named tokens in one module, and the stylesheet SHALL be built from those tokens.
4. IF the stylesheet file is missing or unreadable, THEN THE Wizard SHALL start with Fusion defaults and log a warning, and SHALL NOT crash.
5. THE Wizard SHALL NOT replace a widget's stylesheet when the mouse enters or leaves it. Hover and focus appearance SHALL come from `:hover` and `:focus` rules in the central stylesheet.
6. WHEN the user changes the font family or size in Settings, THE Wizard SHALL apply it to every widget, including widgets defined in `.ui` files.
7. The `.ui` files SHALL NOT pin a font family. A bold or italic style SHALL be expressed as a stylesheet class, not a per-widget font.

### Requirement 2: No change to the installer environment

**User story:** As a user who installed v2.2, I want to receive v2.3.0 through Help → Check for Updates, so that I don't have to reinstall.

**Acceptance criteria**
1. THE Wizard SHALL import only packages present in the installer environment.
2. THE Wizard SHALL use committed SVG files for icons, rendered with QtSvg, and SHALL NOT depend on an icon package.
3. WHEN an installation on v2.2.x updates through the in-app updater, THE Wizard SHALL start and run without any package install step.
4. THE CI pipeline SHALL build its test environment from `environment.yml` as committed, so that a new import missing from that file fails CI.

### Requirement 3: Settings survive the version upgrade

**User story:** As a user, I want my recent files, template, fonts and window size kept when I update, so that an update doesn't reset my setup.

**Acceptance criteria**
1. THE Wizard SHALL store settings under a fixed organization name that doesn't include the version number.
2. WHEN the Wizard starts and the new settings location is empty, THE Wizard SHALL copy all values from the most recent version-specific settings location it finds, then use the new location.
3. THE migration SHALL run once, and SHALL NOT overwrite values already present in the new location.
4. THE migration SHALL be included in the same release as, or an earlier release than, the change of `__version__` to 2.3.0.
5. THE Wizard SHALL leave the old settings location in place, so that a v2.2.x installation on the same machine keeps working.

### Requirement 4: Validation highlighting through widget properties

**User story:** As a maintainer, I want validation state to be a widget property, not a replaced stylesheet, so that highlighting doesn't conflict with the theme.

**Acceptance criteria**
1. WHEN validation finds a problem in a field, THE Wizard SHALL set a `validation` property on that field (values: `error`, `warning`, `active-error`) and re-polish its style.
2. WHEN validation is cleared or the problem is fixed and validation is re-run, THE Wizard SHALL reset the property, and the field SHALL return to the theme's normal look.
3. THE appearance of each validation state SHALL be defined only in the central stylesheet.
4. THE Wizard SHALL NOT call `setStyleSheet` on a field to show validation state.
5. An error state SHALL be indicated by more than color alone: an accent bar plus an inline message (Requirement 8).

### Requirement 5: Sidebar navigation

**User story:** As a user, I want a list of sections down the left showing each section's status, so that I can see what needs work and go there directly.

**Acceptance criteria**
1. THE Wizard SHALL show a sidebar listing every section that currently has a tab, in the current tab order, with the same names.
2. WHEN the user selects a sidebar entry, THE Wizard SHALL show that page in the main area.
3. WHEN validation has run, each sidebar entry SHALL show the number of errors and warnings on its page. WHEN a page has no problems, its entry SHALL show a completed indicator.
4. Each status indicator SHALL combine an icon or count with color, and SHALL NOT rely on color alone.
5. THE user SHALL be able to move between entries with the arrow keys, and to open page *n* with Ctrl+*n*.
6. Each sidebar entry SHALL expose an accessible name that includes its status, for example "Identification, 1 error".
7. WHEN an optional section is enabled (Taxonomy, Cross reference, and the other entries in Advanced → Optional Sections), THE sidebar SHALL reflect it. The existing menu entries SHALL remain.
8. THE Wizard SHALL NOT provide a setting for the previous tab layout.

### Requirement 6: Identification split into two pages

**User story:** As a user, I want the long Identification section split into two pages grouped by purpose, so that each page is easier to work through.

**Acceptance criteria**
1. THE sidebar SHALL show Identification as a group heading with two pages under it:
   - **Description:** Citation, Abstract, Purpose, Supplemental Information, Keywords, Status, Time Period of Content.
   - **Access and Contact:** Point of Contact, Access Constraints, Use Constraints, Data Set Credit, Native Data Set Environment, Cross Reference.
2. Taxonomy, when enabled, SHALL appear on the Description page after Keywords.
3. THE split SHALL change only where widgets are displayed. The XML the Wizard reads and writes SHALL be identical to the output before the split, for the same input.
4. Every widget currently in Identification SHALL appear on exactly one of the two pages.

> **Undecided.** The split above is a draft. Whether to split Identification at all, and how, is still open. Keeping it as one page with a jump bar (Requirement 7) is an acceptable outcome. See `status.md`.

### Requirement 7: Card layout and jump bar

**User story:** As a user, I want each page organized into clear blocks with quick links, so that long pages are easier to scan.

**Acceptance criteria**
1. Each widget group that is currently a group box SHALL be shown as a card. A card has a background, a header, and no border nested inside another border.
2. THE pages SHALL keep their current content and order, apart from the Identification split in Requirement 6.
3. WHEN a page has more than three cards, THE Wizard SHALL show a jump bar listing those cards in page order.
4. WHEN the user activates a jump bar button, THE page SHALL scroll so that the card is at the top. The jump bar SHALL highlight the card currently in view.
5. Cards that already collapse (Point of Contact, Process Contact) SHALL keep that behavior and use one shared expand/collapse control.
6. THE layout SHALL remain usable at a window size of 1300×700 and at 100% and 150% display scaling, without content clipping.

### Requirement 8: Inline validation messages and Problems panel

**User story:** As a user, I want to see why a field is invalid next to the field, and a list of all problems I can click through, so that I can fix a record quickly.

**Acceptance criteria**
1. WHEN a field has a problem, THE Wizard SHALL show the message directly below the field, in addition to the tooltip.
2. THE Wizard SHALL replace the Error List dialog with a dockable Problems panel at the bottom of the main window.
3. WHEN the user selects a problem in the Problems panel, THE Wizard SHALL switch to the page containing the field, scroll to it, focus it, and mark it `active-error`.
4. THE Problems panel SHALL show each problem's severity, section and message, and SHALL update when validation runs or is cleared.
5. THE user SHALL be able to show or hide the Problems panel from the Validate menu and from the status bar.

### Requirement 9: Toolbar

**User story:** As a user, I want the common actions one click away, so that I don't need the menus for routine work.

**Acceptance criteria**
1. THE Wizard SHALL show a toolbar with New, Open, Save, Validate, Preview and Review Report.
2. Each toolbar action SHALL trigger the same code as its existing menu item, and SHALL show the menu item's keyboard shortcut in its tooltip.
3. Toolbar icons SHALL be SVG files recolored at load time from theme tokens, including a disabled state.
4. THE icon set's license file SHALL be committed next to the icons.

### Requirement 10: Status bar

**User story:** As a user, I want save state and problem counts always visible.

**Acceptance criteria**
1. THE status bar SHALL show whether the record has unsaved changes, and the time of the last save.
2. WHEN validation has run, THE status bar SHALL show error and warning counts. Clicking them SHALL toggle the Problems panel.
3. Existing temporary status messages SHALL continue to appear.

### Requirement 11: Accessibility (Section 508)

**User story:** As a user of assistive technology, I want the new interface to work with a keyboard and screen reader, and to have readable contrast.

**Acceptance criteria**
1. Text and its background SHALL meet WCAG 2.1 AA contrast: 4.5:1 for normal text, and 3:1 for large text and for borders that identify a control.
2. Every interactive control SHALL show a visible focus indicator.
3. Every new control (sidebar entries, jump bar buttons, toolbar buttons, Problems panel rows) SHALL have an accessible name.
4. Every new feature SHALL be usable without a mouse.

### Requirement 12: Continuous integration

**User story:** As a maintainer, I want tests to run automatically on every push, so that regressions are caught before merge.

**Acceptance criteria**
1. A GitHub Actions workflow SHALL run the test suite on Windows and Linux hosted runners for every push to the GitHub mirror.
2. THE workflow SHALL build the environment from `environment.yml` and run pytest with Qt in offscreen mode.
3. THE workflow SHALL cache the conda environment, keyed on the contents of `environment.yml`.
4. THE workflow SHALL be independent of the existing macOS installer workflow, and SHALL NOT change that workflow.

### Requirement 13: Reproducible generated UI code

**User story:** As a maintainer, I want the `UI_*.py` files regenerated by a script, so that `.ui` edits never conflict with hand edits.

**Acceptance criteria**
1. Before any `UI_*.py` file is regenerated, the hand edits in the committed files SHALL be identified, and moved into the `.ui` file or into Python code.
2. A script SHALL regenerate every `UI_*.py` file from its `.ui` file with the pyuic5 in the installer environment.
3. Regeneration SHALL be committed separately from any `.ui` content change.

### Requirement 14: Release

**User story:** As the release manager, I want v2.3.0 delivered through the existing update channel, documented, and buildable into future installers.

**Acceptance criteria**
1. THE release SHALL set `__version__` to 2.3.0 and merge `feature/ui-modernization` into `main-v2.2`.
2. `CHANGES.txt` SHALL describe the user-visible changes.
3. THE user documentation in `docs/usage/` SHALL be updated, including screenshots, to match the new layout.
4. THE release notes SHALL state that future installers must be built from a `main-v2.2` checkout, because installed copies follow the branch that was checked out at build time.
5. THE full test suite SHALL pass in CI on Windows and Linux before the merge into `main-v2.2`.

### Requirement 15: Later enhancements (lower priority, after Requirements 1–14)

**User story:** As a user, I want extra aids for finding and completing fields.

**Acceptance criteria**
1. THE sidebar header SHALL show the share of required fields that are complete, as a ring and a percentage.
2. Originators and keywords SHALL be shown as removable chips in a wrapping layout.
3. WHEN the user presses Ctrl+K, THE Wizard SHALL open a search box that lists matching field and card names, and SHALL go to the selected field.
4. THE user SHALL be able to choose a light theme, a dark theme, or following the system setting. The choice SHALL persist across updates.
