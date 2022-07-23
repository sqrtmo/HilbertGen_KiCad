# https://jeffmcbride.net/kicad-track-layout/
# spaces problem https://stackoverflow.com/questions/5685406/inconsistent-use-of-tabs-and-spaces-in-indentation

import pcbnew
import wx
import os

from . import gui

class patternGen(pcbnew.ActionPlugin):
    """Draw hilbert curve"""
    def defaults( self ):
        self.name = "Hilber Gen"
        self.category = "Modify PCB"
        self.description = "generates a hilber curve pattern"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'h_ico.png')

    def Run( self ):
        board = pcbnew.GetBoard()

        # gui.msg("Info", "track length: " + str(whole_len) + " mm" + "\n" + "track width: " + str(track_widht) + " mm\n" + "trace resistance: " + str(resistance) )

        # sg = InitSimpleGui(pcbnew.GetBoard())

        # h = hilbert.hilbert(board)
        # h.order = 4
        # h.trace_width = 0.2
        # h.trace_thickness_oz = 1
        # h.T_ambient = 25
        # h.size = 100

        # h.calculate()
        # h.putLabel()
        # h.generate()
        # gui.msg("Info", str(board) )
        # gui.msg("Info", pcbnew.GetWizardsBackTrace() )
        sg = gui.SimpleGui( None, board )
        b  = sg.ShowModal()
        # sg.Destroy()

        # gui.msg("Info", str(b) )

        # pcbnew.Refresh()
patternGen().register()