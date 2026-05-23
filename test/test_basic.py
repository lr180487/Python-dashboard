# =========================================================
# 🧪 BASIC TESTS
# =========================================================


def test_project_runs():
    """Verify pytest is working correctly."""
    assert True


def test_python_version():
    """Verify Python runtime."""
    import sys

    assert sys.version_info.major == 3


def test_import_app():
    """Verify main modules can be imported."""
    try:
        import app  # noqa: F401

        assert True
    except Exception as error:
        raise AssertionError(f"Import failed: {error}")


def test_database_module():
    """Verify database module loads."""
    try:
        from database import models  # noqa: F401

        assert True
    except Exception as error:
        raise AssertionError(f"Database import failed: {error}")
