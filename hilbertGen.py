# https://jeffmcbride.net/kicad-track-layout/
# spaces problem https://stackoverflow.com/questions/5685406/inconsistent-use-of-tabs-and-spaces-in-indentation

import pcbnew
import wx

from . import gui
# from . import hilbert

# track_widht = 0.3

# hilb_order = 5
# hilb_N = 2**hilb_order
# hilb_edges = hilb_N*hilb_N

# hilb_size = 100.0 # square size
# segment_len = hilb_size / hilb_N
# whole_len = segment_len*(hilb_edges-1)
# track_thickness = 0.0347 # 1 oz
# Tamb = 25

# resistance = (1.7e-5 * whole_len / (track_thickness * track_widht)) * (1 + 3.9e-3 * (Tamb-25)) # https://www.omnicalculator.com/other/pcb-trace-resistance

# fillet = 0.5

# hilb_segment_len = hilb_size[0] / hilb_N




    # fillet = pcbnew.PCB_ARC(board)
    # fillet.SetStart( pcbpoint( (p_start[0], p_start[1]) ) )
    # fillet.SetMid  ( pcbpoint( (p_start[0]-p_end[0], p_start[1]-p_end[1]) ) )
    # fillet.SetEnd  ( pcbpoint( (p_end[0]  , p_end[1]  ) ) )

    # fillet.SetLayer(pcbnew.F_Cu)
    # fillet.SetWidth(int(track_widht * 1e6))
    # group.AddItem(fillet)
    # board.Add(fillet)

# def InitSimpleGui(board):
#   sg = gui.SimpleGui(None, board)
#   sg.Show(True)
#   return sg



class patternGen(pcbnew.ActionPlugin):
    """Draw hilbert curve"""
    def defaults( self ):
        self.name = "Hilber Gen"
        self.category = "Modify PCB"
        self.description = "generates a hilber curve pattern"
        self.show_toolbar_button = True
        # self.icon_file_name = os.path.join(os.path.dirname(__file__), 'simple_plugin.png')

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