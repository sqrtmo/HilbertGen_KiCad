# https://www.programcreek.com/python/example/116915/pcbnew.GetBoard

import wx
import pcbnew
from pcbnew import NETINFO_ITEM


class hilbert(object):
    """docstring for hilbert"""
    order = 2
    trace_width = 0.2
    trace_thickness_oz = 1
    trace_thickness = trace_thickness_oz * 0.0347
    T_ambient = 25
    size = 100
    voltage = 12
    netIndex = 0

    N = 2**order
    edges = N*N

    segment_len = size / N
    whole_len = segment_len * (edges-1)

    side_real_size = segment_len * (N-1) # square size will be very close to the set one self.size


    def __init__(self, board):
        self.board = board
        self.group = pcbnew.PCB_GROUP(self.board)
        self.board.Add(self.group)
        self.netList = self.board.GetNetsByName()

    def _draw_segment( self, p_start, p_end ):

        track = pcbnew.PCB_TRACK(self.board) # PCB_TRACK FP_SHAPE
        track.SetStart( pcbnew.wxPointMM( float(p_start[0]), float(p_start[1]) ) )
        track.SetEnd  ( pcbnew.wxPointMM( float(p_end[0])  , float(p_end[1])   ) )

        # Size here is specified as integer nanometers, so multiply mm by 1e6
        track.SetWidth(int(self.trace_width * 1e6))
        track.SetLayer(pcbnew.F_Cu)

        # net = NETINFO_ITEM(self.board, "/heater")

        # self.board.AppendNet(net)
        # track.SetNetCode(net.GetNet())
        # nets = brd.GetNetsByName()
        # track.SetNetCode(0x7ff0a9a5c900)
        # print("fsdfgsgdfg")

        track.SetNet( self.netList.items()[self.netIndex][1] )
        self.board.Add(track)
        self.group.AddItem(track)
        
        # msg("Info", str( len(net.items()) ) )


    def _draw_frame_line( self, p_start, p_end, margin ):
        track = pcbnew.PCB_SHAPE(self.board)
        track.SetStart( pcbnew.wxPointMM( float(p_start[0]-margin), float(p_start[1]-margin) ) )
        track.SetEnd  ( pcbnew.wxPointMM( float(  p_end[0]-margin), float(  p_end[1]-margin) ) )

        # Size here is specified as integer nanometers, so multiply mm by 1e6
        track.SetWidth(int(0.1 * 1e6))
        track.SetLayer(pcbnew.Dwgs_User)
        self.board.Add(track)
        self.group.AddItem(track)


    def _pattern( self, p ):
        pattern = [ [0, 0],
                    [0, 1],
                    [1, 1],
                    [1, 0] ]

        index = p & 0b0011
        ptr = pattern[index]

        for x in range(1, self.order):
            p >>= 2
            index = p & 0b0011
            _len = pow(2, x)
            
            if index == 0:
                ptr[0], ptr[1] = ptr[1], ptr[0]
            elif index == 1:
                ptr[1] += _len
            elif index == 2:
                ptr[0] += _len
                ptr[1] += _len
            elif index == 3:
                ptr[0], ptr[1] = ptr[1], ptr[0]
                ptr[0] = _len - 1 - ptr[0]
                ptr[1] = _len - 1 - ptr[1]
                ptr[0]+=_len
        return ptr


    def calculate(self):
        self.trace_thickness = self.trace_thickness_oz * 0.0347
        self.N = 2 ** self.order
        self.edges = self.N * self.N

        self.segment_len = self.size / self.N
        self.whole_len = self.segment_len * (self.edges-1)
        self.side_real_size = self.segment_len * (self.N-1)


    def gen(self):
        # from . import gui

        fr_margin = (self.size - self.side_real_size) / 2

        # gui.msg("in put label", str(fr_margin) )

        # draw frame
        self._draw_frame_line( [0, 0]                , [0, self.size]        , fr_margin )
        self._draw_frame_line( [0, self.size]        , [self.size, self.size], fr_margin )
        self._draw_frame_line( [self.size, self.size], [self.size, 0]        , fr_margin )
        self._draw_frame_line( [self.size, 0]        , [0, 0]                , fr_margin )
        # draw cross
        self._draw_frame_line( [self.size/2, 0]       , [self.size/2, self.size], fr_margin )
        self._draw_frame_line( [0, self.size/2]       , [self.size, self.size/2], fr_margin )        
        # draw pattern
        for x in range(self.edges-1):
            start = self._pattern(x)
            start[0] *= self.segment_len
            start[1] *= self.segment_len
            end = self._pattern(x+1)
            end[0] *= self.segment_len
            end[1] *= self.segment_len
            self._draw_segment( start, end ) 


    def putLabel(self):
        # from . import gui
        legend = self.info()

        text = pcbnew.PCB_TEXT(self.board)
        text.SetText(legend)
        text.SetHorizJustify(pcbnew.GR_TEXT_HJUSTIFY_LEFT)
        text.SetPosition( pcbnew.wxPointMM( float(self.size+5), float(5) ) )
        text.SetLayer(pcbnew.Cmts_User)
        # track.SetEnd  ( pcbpoint( (p_end[0]  , p_end[1]  ) ) )
        self.board.Add(text)


    def info(self):
        # https://www.omnicalculator.com/other/pcb-trace-resistance
        resistance = (1.7e-5 * self.whole_len / (self.trace_thickness * self.trace_width)) * (1 + 3.9e-3 * (self.T_ambient-25)) 
        resistance = round( resistance, 5 )

        current = self.voltage / resistance
        current = round( current, 5 )

        wattage = self.voltage * current
        wattage = round( wattage, 5 )

        return ( 'segment len: '+ str(self.segment_len) + ' mm\n' + 
                 'whole len: '  + str(self.whole_len)   + ' mm\n' + 
                 'resistance: ' + str(resistance)       + ' ohm\n'+
                 'current: '      + str(current)          + ' A\n'  +
                 'power: '        + str(wattage)          + ' W' 
                )
