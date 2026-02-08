import os
import importlib.util
import pytest

# Path to your modules folder
MODULES_DIR = "modules"

@pytest.mark.core
def get_all_modules():
    """Searches for all .py files in the modules folder automatically.."""
    modules = []
    if os.path.exists(MODULES_DIR):
        for filename in os.listdir(MODULES_DIR):
            if filename.endswith(".py") and filename != "__init__.py":
                modules.append(filename)
    return modules

@pytest.mark.security
@pytest.mark.parametrize("module_file", get_all_modules())
def test_module_load(module_file):
    """
    This test will try to load each module. 
    If there is a contributor whose code has typos/errors, this test will be RED.
    """
    module_path = os.path.join(MODULES_DIR, module_file)
    module_name = module_file[:-3]
    
    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        # If you get here without any errors, it means the code is 'healthy' (can be imported)
        assert True
    except Exception as e:
        pytest.fail(f"Module {module_file} ERROR: {e}")
      
