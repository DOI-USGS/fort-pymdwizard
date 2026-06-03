# Fort-pymdwizard Ruff Code Quality Report (UPDATED)

**Generated:** 2026-06-03 (Updated after fixes)
**Ruff Version:** Latest  
**Total Issues Remaining:** ~90-105

## Summary of Fixes Completed

✅ **Commit 1 (7a21512):** Auto-fixed 87 safe issues
- Removed unused imports (F401)
- Fixed 'not in' syntax (E713)
- Removed unnecessary f-string prefixes (F541)
- 44 files changed, net -38 lines

✅ **Commit 2 (e18c55e):** Fixed 3 bare except statements
- mdattr.py: XPath operations → `except (IndexError, AttributeError)`
- doi_utils.py: API calls → `except (requests.RequestException, KeyError, ValueError)`
- ContactInfo.py: Network ops → `except (ConnectionError, TimeoutError, Exception)`

✅ **Commit 3 (2e660b9):** Removed 177 unused variables (F841)
- spatial_utils.py: 101 fixes
- GUI files: 60+ fixes
- Core files: 16 fixes
- 26 files changed, net -5 lines

**Total Fixed:** 267 issues (72% of original 372)

---

## Remaining Issues by Category

### 1. Bare Except Statements (E722) - 54 remaining ⚠️
**Priority:** HIGH  
**Effort:** Medium (4-6 hours total)

These catch ALL exceptions including system exits and keyboard interrupts, which is problematic.

**Files Requiring Attention:**
- `pymdwizard/gui/spdom.py` - 8 instances
- `pymdwizard/gui/MainWindow.py` - 5 instances
- `pymdwizard/gui/sb_locator.py` - 5 instances
- `pymdwizard/gui/spatial_tab.py` - 3 instances
- `pymdwizard/core/spatial_utils.py` - 3 instances
- `pymdwizard/core/org_cert_setup.py` - 2 instances
- `pymdwizard/core/review_utils.py` - 2 instances
- `pymdwizard/core/taxonomy.py` - 2 instances
- Others - 1-2 each (~20 more across various files)

**Fix Patterns by Context:**

**Network/API Operations:**
```python
# BAD
try:
    response = requests.get(url)
except:
    return None

# GOOD
try:
    response = requests.get(url)
except (requests.RequestException, ConnectionError, TimeoutError):
    return None
```

**XPath/XML Operations:**
```python
# BAD
try:
    element = node.xpath("path/to/element")[0]
except:
    pass

# GOOD
try:
    element = node.xpath("path/to/element")[0]
except (IndexError, AttributeError, KeyError):
    pass
```

**File Operations:**
```python
# BAD
try:
    with open(filename) as f:
        data = f.read()
except:
    data = None

# GOOD
try:
    with open(filename) as f:
        data = f.read()
except (FileNotFoundError, IOError, OSError):
    data = None
```

**Type Conversions:**
```python
# BAD
try:
    maxrows = int(self.ui.maxrows.text())
except:
    maxrows = -9999

# GOOD
try:
    maxrows = int(self.ui.maxrows.text())
except (ValueError, TypeError):
    maxrows = -9999
```

**When You Don't Know Exactly:**
```python
# ACCEPTABLE - Still better than bare except
except Exception:
    pass
```

This catches most exceptions but still allows KeyboardInterrupt and SystemExit to work.

---

### 2. Type Comparison Issues (E721) - 4 instances
**Priority:** LOW  
**Effort:** 5 minutes

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

### 3. None Comparison Issues (E711) - 2 instances
**Priority:** LOW  
**Effort:** 2 minutes

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

### 4. Boolean Comparison (E712) - 1 instance
**Priority:** LOW  
**Effort:** 1 minute

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

### 5. Module Import Not at Top (E402) - 17 instances
**Priority:** LOW  
**Effort:** Low OR ignore

**Files:**
- All in `pymdwizard/gui/ui_files/UI_*.py` (auto-generated from Qt Designer)

**Options:**
1. Regenerate UI files properly
2. Add to `.ruff.toml` ignore list:
```toml
[tool.ruff.lint.per-file-ignores]
"pymdwizard/gui/ui_files/*.py" = ["E402"]
```

---

### 6. Star Imports (F403, F405) - 4 instances
**Priority:** LOW  
**Effort:** Medium

**File:**
- `pymdwizard/gui/ui_files/growingtextedit.py`

```python
# BAD
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# GOOD
from PyQt5.QtCore import Qt, QSize, pyqtSlot, QTimer
from PyQt5.QtGui import QTextDocument
from PyQt5.QtWidgets import QPlainTextEdit, QApplication
```

---

### 7. Function Redefinition (F811) - 1 instance
**Priority:** MEDIUM  
**Effort:** 5 minutes

**File:**
- `pymdwizard/gui/spref.py:429` - `has_content()` defined twice

**Fix:** Remove the duplicate definition or rename one.

---

### 8. Format String Issues (F523) - 1 instance
**Priority:** LOW  
**Effort:** 1 minute

**File:**
- `pymdwizard/core/xml_utils.py:634` - Format string has unused arguments

---

## Recommended Next Steps

### Phase 1: Quick Wins (30 minutes)
Fix all the trivial issues:
1. Type comparisons (E721) - 4 instances
2. None comparisons (E711) - 2 instances  
3. Boolean comparison (E712) - 1 instance
4. Format string (F523) - 1 instance
5. Function redefinition (F811) - 1 instance

**Total: 9 issues, ~30 minutes**

### Phase 2: Bare Except Statements (4-6 hours)
Tackle file by file, understanding context:

**Priority Order:**
1. `spdom.py` (8 instances) - Focus on JavaScript evaluation, map operations
2. `MainWindow.py` (5 instances) - UI operations, file handling
3. `sb_locator.py` (5 instances) - ScienceBase API, network operations
4. `spatial_tab.py` (3 instances) - File extraction operations
5. `spatial_utils.py` (3 instances) - GDAL/OGR operations
6. Others (26 instances across ~20 files) - 1-2 each

**Estimated time per file:**
- 8 instances: 1 hour
- 5 instances: 30-45 minutes
- 3 instances: 20-30 minutes
- 1-2 instances: 5-10 minutes each

### Phase 3: Clean Up (optional)
- Star imports in `growingtextedit.py`
- Add E402 ignore for auto-generated UI files

---

## Configuration Recommendation

Create `pyproject.toml` or `ruff.toml`:

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
"tests/test_*.py" = ["F811"]  # Allow redefined pytest fixtures
```

---

## Statistics

**Original Issues:** 372
**Fixed:** 267 (72%)
**Remaining:** ~90-105 (28%)

**Breakdown of Fixes:**
- ✅ Unused imports: 60+ fixed
- ✅ Unused variables: 177 fixed
- ✅ Syntax improvements: 25+ fixed
- ✅ Bare excepts: 3 fixed (54 remaining)

**Remaining Priority:**
- 🔴 HIGH: 54 bare except statements (major improvement needed)
- 🟡 MEDIUM: 1 function redefinition
- 🟢 LOW: 30+ trivial fixes (imports, comparisons, etc.)

---

## Next Session Commands

Check current status:
```bash
ruff check .
```

See only bare excepts:
```bash
ruff check . --select E722
```

See only quick wins:
```bash
ruff check . --select E721,E711,E712,F523,F811
```

Fix all remaining safe issues:
```bash
# This will fix type comparisons, None comparisons, etc.
ruff check . --fix
```

---

## Time Estimates

**To reach 90% fixed:**
- Quick wins: 30 minutes
- Top 5 files (26 bare excepts): 3-4 hours
- **Total: ~4.5 hours**

**To reach 95% fixed:**
- Above + remaining 28 bare excepts: 2-3 hours more
- **Total: ~7 hours**

**To reach 100% fixed:**
- Above + star imports + configuration: 1 hour more
- **Total: ~8 hours**

---

**Report generated by Claude Code**  
**Session:** 2026-06-03 (Updated)  
**Branch:** main-v2.2  
**Last Commit:** 2e660b9
