def test_import_app():
    # Simple smoke test to ensure the app module imports without syntax errors
    import importlib
    importlib.import_module('app')

def test_import_utils():
    import importlib
    importlib.import_module('utils')
