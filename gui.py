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

        # triggers
        self.calc_button = wx.Button(self.panel, label="Calculate", pos=(10 , 240), size = (80, 20))
        self.gen_button  = wx.Button(self.panel, label="Generate" , pos=(100, 240), size = (80, 20))

        self.calc_button.Bind( wx.EVT_BUTTON, self.calculate )
        self.gen_button.Bind( wx.EVT_BUTTON, self.gener )
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

        

        # self.out = False

    def gener( self, event ):
        # msg("Info", str(23434) )
        self.pattern.gen()
        self.pattern.putLabel()
        self.EndModal( wx.ID_OK )
        self.OnQuit(None)
        # self.Destroy()



        # self.result = wx.StaticText(self.panel, label = order, id=1, pos=(50, 50))


        # nets = board.GetNetsByName()
        # self.netnames = []
        # for netname, net in nets.items():
        #     if (str(netname) == ""):
        #         continue
        #     self.netnames.append(str(netname))
        # netcb = wx.ComboBox(self.panel, choices=self.netnames)
        # netcb.SetSelection(0)
        # netsbox = wx.BoxSizer(wx.HORIZONTAL)
        # netsbox.Add(wx.StaticText(self.panel, label="Nets:"))
        # netsbox.Add(netcb, proportion=1)
        # modules = board.GetModules()
        # self.modulenames = []
        # for mod in modules:
        #     self.modulenames.append("{}({})".format(mod.GetReference(), mod.GetValue()))
        # modcb = wx.ComboBox(self.panel, choices=self.modulenames)
        # modcb.SetSelection(0)
        # modsbox = wx.BoxSizer(wx.HORIZONTAL)
        # modsbox.Add(wx.StaticText(self.panel, label="Modules:"))
        # modsbox.Add(modcb, proportion=1)
        # box = wx.BoxSizer(wx.VERTICAL)
        # box.Add(label,   proportion=0)
        # box.Add(button,  proportion=0)
        # box.Add(netsbox, proportion=0)
        # box.Add(modsbox, proportion=0)
        # self.panel.SetSizer(box)
        # self.Bind(wx.EVT_BUTTON, self.OnPress, id=1)
        # self.Bind(wx.EVT_COMBOBOX, self.OnSelectNet, id=netcb.GetId())
        # self.Bind(wx.EVT_COMBOBOX, self.OnSelectMod, id=modcb.GetId())
    # def OnPress(self, event):
    #     print("in OnPress")
    #     label = wx.StaticText(self.panel, label = "Hello World")
    # def OnSelectNet(self, event):
    #     item = event.GetSelection()
    #     print("Net {} was selected".format(self.netnames[item]))
    # def OnSelectMod(self, event):
    #     item = event.GetSelection()
        # print("Module {} was selected".format(self.modulenames[item]))