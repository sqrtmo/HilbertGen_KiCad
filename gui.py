import wx
import pcbnew

from . import hilbert

# https://kicad.mmccoo.com/2017/02/15/adding-gui-elements-in-pcbnew/

def msg( label, msg ):
    msg = wx.MessageDialog(None, msg, label, wx.OK | wx.ICON_WARNING)
    msg.ShowModal()


class SimpleGui(wx.Dialog):
    def __init__(self, parent, board):
        wx.Dialog.__init__(self, parent, title="hilbert gen test", size = (200, 300))
        self.panel = wx.Panel(self)

        # msg("Info", pcbnew.GetWizardsBackTrace() )

        self.board = board
        self.pattern = hilbert.hilbert(self.board)

        # msg("Info", str(self.board) )

        # inputs menu
        self.ord_label = wx.StaticText(self.panel, label = "order", pos=(10 , 10))
        self.ord_textbox = wx.TextCtrl(self.panel, value = "2"    , pos=(120, 10), size = (50, 20))

        self.width_label = wx.StaticText(self.panel, label = "width(mm)", pos=(10 , 30))
        self.width_textbox = wx.TextCtrl(self.panel, value = "0.2"      , pos=(120, 30), size = (50, 20))

        self.t_amb_label = wx.StaticText(self.panel, label = "T amb(C)", pos=(10 , 50))
        self.t_amb_textbox = wx.TextCtrl(self.panel, value = "25.0"    , pos=(120, 50), size = (50, 20))

        self.square_size_label = wx.StaticText(self.panel, label = "square sz", pos=(10 , 70))
        self.square_size_textbox = wx.TextCtrl(self.panel, value = "100"      , pos=(120, 70), size = (50, 20))

        self.track_thickness_label = wx.StaticText(self.panel, label = "thickness(oz)", pos=(10 , 90))
        self.track_thickness_textbox = wx.TextCtrl(self.panel, value = "1"            , pos=(120, 90), size = (50, 20))

        self.working_voltage_label = wx.StaticText(self.panel, label = "working voltage", pos=(10 , 110))
        self.working_voltage_textbox = wx.TextCtrl(self.panel, value = "12"             , pos=(120, 110), size = (50, 20))

        # drop down
        net = self.board.GetNetsByName()
        self.netList = []
        for n in net.items():
            self.netList.append(str(n[0]))

        self.netList_label = wx.StaticText(self.panel, label = "net name", pos=(10 , 130))        
        self.netsList = wx.ComboBox( self.panel, pos=(120, 130), size = (75, 25), choices=self.netList )
        self.netsList.Bind( wx.EVT_COMBOBOX, self.OnCombo ) 


        # buttons
        self.calc_button = wx.Button(self.panel, label="Calculate", pos=(10 , 240), size = (80, 20))
        self.gen_button  = wx.Button(self.panel, label="Generate" , pos=(100, 240), size = (80, 20))

        self.calc_button.Bind( wx.EVT_BUTTON, self.calculate )
        self.gen_button.Bind( wx.EVT_BUTTON, self.gener )

        # todo add functionality to assign net to the pattern
        # self.net = NETINFO_ITEM(self.board, "net_name") # https://forum.kicad.info/t/creating-a-net-in-python/2261/16

        # binds
        # self.ord_textbox.Bind( wx.EVT_TEXT, self.calculate )
        # self.width_textbox.Bind( wx.EVT_TEXT, self.calculate )
        # self.t_amb_textbox.Bind( wx.EVT_TEXT, self.calculate )
        # self.square_size_textbox.Bind( wx.EVT_TEXT, self.calculate )
        # self.track_thickness_textbox.Bind( wx.EVT_TEXT, self.calculate )
        # self.working_voltage_textbox.Bind( wx.EVT_TEXT, self.calculate )

        self.result = wx.StaticText(self.panel, label = self.pattern.info(), pos=(10, 150))        


    def _clamp( self, v, min, max ):
        if v < min:
            msg("Wrong value", "min: "+ str( min ) + ", max: " + str( max ) )
            return min
        elif v > max:
            msg("Wrong value", "min: "+ str( min ) + ", max: " + str( max ) )
            return max
        else:
            return v

    def OnCombo( self, event ):
        # msg( "comb", str( self.netList.index(self.netsList.GetValue()) ) )
        self.pattern.netIndex           = int( self.netList.index(self.netsList.GetValue()) )   # get index of selected net


    def calculate( self, event ):
        self.pattern.order              = int(self.ord_textbox.GetValue())
        self.pattern.trace_width        = float(self.width_textbox.GetValue())
        self.pattern.trace_thickness_oz = int(self.track_thickness_textbox.GetValue())
        self.pattern.T_ambient          = float(self.t_amb_textbox.GetValue())
        self.pattern.size               = float(self.square_size_textbox.GetValue())
        self.pattern.voltage            = float(self.working_voltage_textbox.GetValue())

        # msg("Info", self.pattern.info() )
        self.pattern.order              = self._clamp( self.pattern.order             , 1   , 10   )
        self.pattern.trace_width        = self._clamp( self.pattern.trace_width       , 0.01, 10   )
        self.pattern.trace_thickness_oz = self._clamp( self.pattern.trace_thickness_oz, 1   , 3    ) 
        self.pattern.T_ambient          = self._clamp( self.pattern.T_ambient         , 0   , 500  )
        self.pattern.size               = self._clamp( self.pattern.size              , 1   , 1000 )
        self.pattern.voltage            = self._clamp( self.pattern.voltage           , 0.1 , 500  )

        self.pattern.calculate()

        self.result.Destroy()
        self.result = wx.StaticText(self.panel, label = self.pattern.info(), pos=(10, 150))


    def gener( self, event ):
        # msg("Info", str(23434) )
        self.pattern.gen()
        self.pattern.putLabel()
        self.EndModal( wx.ID_OK )
        # self.OnQuit(None)
        # self.Destroy()
