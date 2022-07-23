# pcbnew loads this folder as a package using import
# thus __init__.py (this file) is executed
# We import the plugin class here and register it to pcbnew

# from . import hilbertGen

try:
    # test for wxpython
    import wx
    # Note the relative import!
    from .hilbertGen import patternGen
    # Instantiate and register to Pcbnew
    patternGen().register()
except Exception as e:
    import os
    plugin_dir = os.path.dirname(os.path.realpath(__file__))
    log_file = os.path.join(plugin_dir, 'patternGen.log')
    with open(log_file, 'w') as f:
        f.write(repr(e))
    from .no_wxpython import NoWxpython as patternGen
    patternGen().register()