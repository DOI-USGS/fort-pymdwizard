#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Shared pytest fixtures and configuration for the pymdwizard test suite.

The main job of this module is to make the Qt / QtWebEngine based GUI tests
shut down cleanly. Several widgets (spdom's Leaflet map, the doc Preview)
create a live ``QWebEngineView`` / ``QWebEnginePage``. If those pages are still
alive when Qt tears down the global ``QWebEngineProfile`` at interpreter exit,
Qt prints

    "Release of profile requested but WebEnginePage still not deleted.
     Expect troubles !"

and the process exits non-zero (and can hang) even though every test passed.
That non-zero exit would make CI report failure on a green suite, so we clean
the pages up deterministically at the end of the session instead.
"""

import gc
import socket

import pytest

try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QCoreApplication
except ImportError as err:  # pragma: no cover - environment guard
    raise ImportError(err, __file__)


# ---------------------------------------------------------------------------
# Network marker + offline auto-skip
# ---------------------------------------------------------------------------
#
# Tests that hit a live external service (ITIS, DataCite/Crossref, the USGS
# People Picker, arbitrary public URLs) are marked with @pytest.mark.network.
# They are integration checks: valuable, but flaky in CI and impossible to run
# offline. They are skipped automatically when there is no internet
# connectivity, and can be skipped unconditionally with --no-network.
#
# The offline-safe unit tests mock the network boundary and always run.


def pytest_addoption(parser):
    parser.addoption(
        "--no-network",
        action="store_true",
        default=False,
        help="Skip tests marked @pytest.mark.network (live external services).",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "network: test requires live internet access to an external service.",
    )


def _has_internet(host="8.8.8.8", port=53, timeout=3):
    """Best-effort connectivity probe (DNS port on a public resolver)."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


# Cache the probe so we do not open a socket per test.
_INTERNET_AVAILABLE = None


def pytest_collection_modifyitems(config, items):
    global _INTERNET_AVAILABLE

    force_skip = config.getoption("--no-network")
    if not force_skip and _INTERNET_AVAILABLE is None:
        _INTERNET_AVAILABLE = _has_internet()

    for item in items:
        if "network" not in item.keywords:
            continue
        if force_skip:
            item.add_marker(pytest.mark.skip(reason="--no-network specified"))
        elif not _INTERNET_AVAILABLE:
            item.add_marker(
                pytest.mark.skip(reason="no internet connectivity detected")
            )

# QWebEngine is optional at import time; guard so a non-WebEngine environment
# still collects the non-GUI tests.
try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

    _HAS_WEBENGINE = True
except ImportError:  # pragma: no cover - environment guard
    _HAS_WEBENGINE = False


def _process_events(app, iterations=5):
    """Pump the Qt event loop a few times so deferred deletions run."""
    if app is None:
        return
    for _ in range(iterations):
        app.processEvents()


def _delete_lingering_webengine_objects(app):
    """
    Explicitly delete any still-alive QWebEngineView / QWebEnginePage objects
    and let Qt process the deferred deletions.

    Widgets that own a web view are not always garbage collected before the
    QWebEngineProfile is torn down. Deleting the pages/views here, while the
    QApplication is still alive, avoids the "WebEnginePage still not deleted"
    teardown crash.
    """
    if not _HAS_WEBENGINE or app is None:
        return

    gc.collect()

    # Walk every object tracked by Python and schedule the web views/pages for
    # deletion. isinstance covers custom page subclasses (e.g.
    # SslTrustingWebEnginePage). Deleting them here, then pumping the event
    # loop, ensures the deferred deletes run before the profile is destroyed.
    for obj in list(gc.get_objects()):
        try:
            is_web = isinstance(obj, (QWebEngineView, QWebEnginePage))
        except (ReferenceError, TypeError):
            continue
        if is_web:
            try:
                obj.deleteLater()
            except (RuntimeError, ReferenceError):
                # Already deleted on the C++ side.
                continue

    _process_events(app)
    gc.collect()
    _process_events(app)


@pytest.fixture(scope="session")
def qapp_session():
    """
    A single session-wide QApplication.

    pytest-qt provides its own ``qapp``; this fixture just guarantees an
    instance exists for the session-scoped teardown below even if no test
    requested ``qtbot`` yet.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture(scope="session", autouse=True)
def _webengine_teardown():
    """
    Session-scoped, autouse cleanup that deletes lingering QtWebEngine pages
    and views before the interpreter (and the global QWebEngineProfile) tears
    down. Yields to let the whole session run first.
    """
    yield
    app = QApplication.instance() or QCoreApplication.instance()
    _delete_lingering_webengine_objects(app)
