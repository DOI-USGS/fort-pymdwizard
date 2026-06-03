# Fort-pymdwizard Ruff Code Quality Report

**Generated:** 2026-06-03  
**Ruff Version:** Latest  
**Total Issues Remaining:** 267

## Summary of Fixes Completed

✅ **Commit 1 (7a21512):** Auto-fixed 87 safe issues
- Removed unused imports (F401)
- Fixed 'not in' syntax (E713)
- Removed unnecessary f-string prefixes (F541)
- 44 files changed, net -38 lines

✅ **Commit 2 (e18c55e):** Fixed 3 bare except statements
- mdattr.py: XPath operations
- doi_utils.py: API calls with fallback
- ContactInfo.py: Network operations

---

## Remaining Issues by Category

### 1. Bare Except Statements (E722) - 54 remaining
**Priority:** HIGH  
**Effort:** Medium - Requires understanding context for each exception

These catch ALL exceptions including system exits and keyboard interrupts.

**Top Files to Fix:**
- `pymdwizard/gui/spdom.py` - 8 instances
- `pymdwizard/gui/MainWindow.py` - 5 instances
- `pymdwizard/gui/sb_locator.py` - 5 instances
- `pymdwizard/gui/spatial_tab.py` - 3 instances
- `pymdwizard/core/spatial_utils.py` - 3 instances

**Fix Pattern:**
```python
# BAD
except:
    pass

# GOOD - Specific exceptions
except (IndexError, KeyError, AttributeError):
    pass

# ACCEPTABLE - When you truly need to catch most things
except Exception:
    pass
```

**Common Exception Types to Use:**
- **Network/API calls:** `requests.RequestException, ConnectionError, TimeoutError`
- **Dictionary/List access:** `KeyError, IndexError, AttributeError`
- **XML/Parsing:** `etree.XMLSyntaxError, AttributeError`
- **File operations:** `FileNotFoundError, IOError, OSError`
- **Type conversions:** `ValueError, TypeError`

---

### 2. Unused Variables (F841) - ~150 instances
**Priority:** MEDIUM  
**Effort:** Low - Mostly just remove the variable assignment

Variables are assigned but never used.

**Top Files:**
- `pymdwizard/core/spatial_utils.py` - 80+ instances
- `pymdwizard/core/doi_utils.py` - 6 instances
- `pymdwizard/gui` files - scattered throughout

**Common Pattern:**
```python
# BAD - Variable assigned but never used
title = xml_node("title", text="...", parent_node=citeinfo)

# GOOD - xml_node already adds to parent, don't need variable
xml_node("title", text="...", parent_node=citeinfo)
```

**Note:** Many of these are in XML node creation where the function has a side effect (adds to parent), so the return value isn't needed.

---

### 3. Type Comparison Issues (E721) - 4 instances
**Priority:** LOW  
**Effort:** Trivial

Using `type(x) == str` instead of `isinstance(x, str)`.

**Files:**
- `pymdwizard/core/fgdc_utils.py:269`
- `pymdwizard/core/xml_utils.py:602, 636`
- `tests/test_version.py:17, 18`

**Fix:**
```python
# BAD
if type(date_input) == str:

# GOOD
if isinstance(date_input, str):
```

---

### 4. None Comparison Issues (E711) - 2 instances
**Priority:** LOW  
**Effort:** Trivial

**Files:**
- `pymdwizard/core/spatial_utils.py:587, 595`

**Fix:**
```python
# BAD
if params["mapprojn"] != None:

# GOOD
if params["mapprojn"] is not None:
```

---

### 5. Boolean Comparison (E712) - 1 instance
**Priority:** LOW  
**Effort:** Trivial

**File:**
- `pymdwizard/gui/sb_locator.py:296`

**Fix:**
```python
# BAD
if permissions["write"]["inherited"] == True:

# GOOD
if permissions["write"]["inherited"]:
```

---

### 6. Module Import Not at Top (E402) - 17 instances
**Priority:** LOW  
**Effort:** Low - Move imports to top of file

**Files:**
- All in `pymdwizard/gui/ui_files/UI_*.py` (auto-generated)

**Note:** These are auto-generated UI files from Qt Designer. Consider:
- Regenerating them properly
- Adding them to Ruff ignore list if they're always auto-generated

---

### 7. Star Imports (F403, F405) - 4 instances
**Priority:** LOW  
**Effort:** Medium

**File:**
- `pymdwizard/gui/ui_files/growingtextedit.py`

```python
# BAD
from PyQt5.QtCore import *

# GOOD
from PyQt5.QtCore import Qt, QSize, QPoint
```

---

### 8. Redefined Function (F811) - 1 instance
**Priority:** MEDIUM  
**Effort:** Low

**File:**
- `pymdwizard/gui/spref.py:429` - `has_content` defined twice

**Fix:** Remove or rename one of the definitions.

---

### 9. Format String Issues (F523) - 1 instance
**Priority:** LOW  
**Effort:** Trivial

**File:**
- `pymdwizard/core/xml_utils.py:634` - Unused format arguments

---

## Recommended Fix Priority

### Phase 1: Quick Wins (1-2 hours)
1. ✅ Auto-fix safe issues (DONE)
2. Type comparisons (E721) - 4 instances
3. None comparisons (E711) - 2 instances  
4. Boolean comparison (E712) - 1 instance
5. Format string (F523) - 1 instance
6. Function redefinition (F811) - 1 instance

### Phase 2: Unused Variables (2-3 hours)
Focus on `spatial_utils.py` first (80+ instances). Most can be removed by changing:
```python
variable = xml_node(...)
```
to:
```python
xml_node(...)
```

### Phase 3: Bare Except Statements (4-6 hours)
Work file by file, understanding context:
1. `spdom.py` (8 instances)
2. `MainWindow.py` (5 instances)
3. `sb_locator.py` (5 instances)
4. Others (3 or fewer each)

### Phase 4: Clean Up (optional)
- Star imports in `growingtextedit.py`
- Module import locations in auto-generated files

---

## Configuration Recommendation

Create a `ruff.toml` or add to `pyproject.toml`:

```toml
[tool.ruff]
line-length = 88
target-version = "py313"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "W",   # pycodestyle warnings
]

# Ignore auto-generated files
[tool.ruff.lint.per-file-ignores]
"pymdwizard/gui/ui_files/*.py" = ["E402", "F403", "F405"]
"tests/test_*.py" = ["F811"]  # Allow redefined fixtures
```

---

## Statistics

**Files with Issues:** ~50 files
**Issues Fixed:** 90 (25% of original 372)
**Issues Remaining:** 267 (75%)

**By Category:**
- Unused variables: ~150 (56%)
- Bare excepts: 54 (20%)
- Import issues: 17 (6%)
- Other: 46 (18%)

---

## How to Continue

Run Ruff to see current state:
```bash
ruff check .
```

Fix specific issue types:
```bash
# See only bare excepts
ruff check . --select E722

# See only unused variables
ruff check . --select F841

# Auto-fix unsafe issues (includes removing unused variables)
ruff check . --fix --unsafe-fixes
```

Generate updated report:
```bash
ruff check . --output-format=json > ruff_issues_detailed.json
```

---

**Report generated by Claude Code**
**Session:** 2026-06-03
