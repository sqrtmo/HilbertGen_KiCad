# HilbertGen_KiCad
Hilbert curve generator plugin for KiCad

The plugin aims to make the PCB heaters easier and faster to develop.
At this point it is able to make only square shaped patterns. 
Code is based on: https://www.youtube.com/watch?v=dSK-MW-zuAc

# Warning!
Current KiCad version 6.0.6
This plugin is in working stage and is not fully tested!

# Installation
MacOS - download, unzip and copy the folder to /Users/your name/Documents/KiCad/6.0/scripting/plugins

# Error handling
The startup error handler is taken from: https://github.com/MitjaNemec/Kicad_action_plugins/blob/master/replicate_layout/__init__.py
Startup script will generate a log file containing the error message in the plugin source folder.

# todo
Add pattern edge fillets

