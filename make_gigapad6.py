# DEPRECATED: this legacy generator uses KiCad's in-process pcbnew Python API
# and must not be run while the KiCad GUI is open. The validated board is
# routed by the external Java-free KiCadRoutingTools CLI instead.
import os
import wx
import pcbnew

ROOT = os.path.dirname(os.path.abspath(__file__))
IU = pcbnew.FromMM
app = wx.App(False)

def add_net(board, name):
    if name not in board.GetNetsByName():
        board.Add(pcbnew.NETINFO_ITEM(board, name))
    return board.GetNetsByName()[name].GetNetCode()

def seg(board, a, b, layer, net):
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(pcbnew.VECTOR2I(IU(a[0]), IU(a[1])))
    t.SetEnd(pcbnew.VECTOR2I(IU(b[0]), IU(b[1])))
    t.SetLayer(layer)
    t.SetWidth(IU(0.25))
    t.SetNetCode(net)
    board.Add(t)

src = pcbnew.LoadBoard(os.path.join(ROOT, "third_party/GigaPad/giga_pad_pcb/giga_pad.kicad_pcb"))
board = pcbnew.BOARD()
board.SetCopperLayerCount(2)
board.GetDesignSettings().m_MinClearance = IU(0.20)
board.GetDesignSettings().m_SilkClearance = IU(0.15)
board.GetAllNetClasses()["Default"].SetClearance(IU(0.20))

gnd = add_net(board, "GND")
sw_nets = [add_net(board, f"SW_{i}") for i in range(1, 7)]

sw_source = next(f for f in src.GetFootprints() if f.GetReference() == "SW2")
xiao_source = next(f for f in src.GetFootprints() if f.GetReference() == "U1")

switch_xy = [(82, 49), (102, 49), (122, 49), (82, 68), (102, 68), (122, 68)]
switches = []
for i, (x, y) in enumerate(switch_xy, 1):
    f = pcbnew.Cast_to_FOOTPRINT(sw_source.Duplicate(False))
    board.Add(f)
    f.SetReference(f"SW{i}")
    f.SetPosition(pcbnew.VECTOR2I(IU(x), IU(y)))
    # Cherry MX footprints contain NPTH mounting holes before the two
    # electrical pads in the pad list. Select by pad number, never by index.
    pad1 = next(p for p in f.Pads() if p.GetNumber() == "1")
    pad2 = next(p for p in f.Pads() if p.GetNumber() == "2")
    pad1.SetNetCode(sw_nets[i-1])
    pad2.SetNetCode(gnd)
    switches.append(f)

xiao = pcbnew.Cast_to_FOOTPRINT(xiao_source.Duplicate(False))
board.Add(xiao)
xiao.SetPosition(pcbnew.VECTOR2I(IU(104), IU(84)))
xiao.SetReference("U1")
for p in xiao.Pads():
    p.SetNetCode(0)
for idx, p in enumerate(xiao.Pads()):
    if idx < 6:
        p.SetNetCode(sw_nets[idx])
    elif idx == 12:
        p.SetNetCode(gnd)

# Fan-out to the XIAO D0-D5 row. Alternate copper layers so the six short
# connections do not need to cross one another.
routes = [
    [((82,49),(82,45)),((82,45),(96.38,76.38))],
    [((102,49),(102,45)),((102,45),(98.92,76.38))],
    [((122,49),(122,45)),((122,45),(101.46,76.38))],
    [((82,68),(82,64)),((82,64),(104,76.38))],
    [((102,68),(102,64)),((102,64),(106.54,76.38))],
    [((122,68),(122,64)),((122,64),(109.08,76.38))],
]
route_layers = [pcbnew.B_Cu, pcbnew.F_Cu, pcbnew.B_Cu,
                pcbnew.F_Cu, pcbnew.B_Cu, pcbnew.F_Cu]
for i, route in enumerate(routes):
    for a, b in route:
        seg(board, a, b, route_layers[i], sw_nets[i])

# Filled ground plane connects all switch ground pads and the XIAO ground pad
# while automatically clearing signal pads and the unused XIAO pads.
ground_points = [(75.65,51.54),(95.65,51.54),(115.65,51.54),(75.65,70.54),(95.65,70.54),(115.65,70.54)]
zone = pcbnew.ZONE(board)
zone.SetLayer(pcbnew.F_Cu)
zone.SetNetCode(gnd)
zone.SetIsRuleArea(False)
zone.SetMinThickness(IU(0.25))
poly = zone.Outline()
poly.NewOutline()
poly.Append(IU(69), IU(38))
poly.Append(IU(136), IU(38))
poly.Append(IU(136), IU(92.5))
poly.Append(IU(69), IU(92.5))
board.Add(zone)
pcbnew.ZONE_FILLER(board).Fill(board.Zones())

for a, b in [((67.945,40.005),(67.945,90.805)),((67.945,90.805),(71.12,93.98)),
             ((71.12,93.98),(134.62,93.98)),((134.62,93.98),(137.795,90.805)),
             ((137.795,90.805),(137.795,40.005)),((137.795,40.005),(134.62,36.83)),
             ((134.62,36.83),(71.12,36.83)),((71.12,36.83),(67.945,40.005))]:
    s = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_SEGMENT)
    s.SetLayer(pcbnew.Edge_Cuts)
    s.SetStart(pcbnew.VECTOR2I(IU(a[0]), IU(a[1])))
    s.SetEnd(pcbnew.VECTOR2I(IU(b[0]), IU(b[1])))
    s.SetWidth(IU(0.1))
    board.Add(s)

text = pcbnew.PCB_TEXT(board)
text.SetText("GIGAPAD 6 MX / USB + BLE")
text.SetPosition(pcbnew.VECTOR2I(IU(102), IU(39)))
text.SetLayer(pcbnew.F_SilkS)
text.SetTextSize(pcbnew.VECTOR2I(IU(1.2), IU(1.2)))
text.SetTextThickness(IU(0.2))
board.Add(text)

board.GetTitleBlock().SetTitle("GigaPad 6 MX USB + BLE")
board.GetTitleBlock().SetComment(1, "Six Cherry MX keys; XIAO nRF52840 or XIAO Sense optional")
pcbnew.SaveBoard(os.path.join(ROOT, "GigaPad6_MX.kicad_pcb"), board)
print("created GigaPad6_MX.kicad_pcb")
