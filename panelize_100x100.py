import os
import wx
import pcbnew

ROOT = os.path.dirname(os.path.abspath(__file__))
IU = pcbnew.FromMM

app = wx.App(False)
panel = pcbnew.BOARD()
panel.SetCopperLayerCount(2)
panel.GetDesignSettings().m_MinClearance = IU(0.15)
panel.GetDesignSettings().m_SilkClearance = IU(0.15)
panel.GetAllNetClasses()["Default"].SetClearance(IU(0.15))

sources = [
    # Final assembly uses the 3-key ESP32 carrier with the controller socket
    # on the same PCB.  This avoids the external interposer and keeps the
    # switches clear of the module footprint.
    ("GigaPad3_ESP32_Onboard.kicad_pcb", 5, 5, 0, ""),
    ("N12_TJA1103_KONG_KETI_EDUv2.kicad_pcb", 65.5, 5, 0, ""),
    ("MATEnet_2Wire_Dongle_A.kicad_pcb", 5, 75.5, 0, ""),
    ("MATEnet_2Wire_Dongle_B.kicad_pcb", 48, 75.5, 0, ""),
]

def net_map(src, prefix):
    mapping = {0: 0}
    for code, net in src.GetNetInfo().NetsByNetcode().items():
        name = prefix + net.GetNetname()
        if not name:
            continue
        names = panel.GetNetsByName()
        if name not in names:
            panel.Add(pcbnew.NETINFO_ITEM(panel, name))
        existing = panel.GetNetsByName()[name]
        mapping[code] = existing.GetNetCode()
    return mapping

def remap(item, src, mapping):
    if hasattr(item, "GetNetCode") and hasattr(item, "SetNetCode"):
        code = item.GetNetCode()
        if code in mapping:
            item.SetNetCode(mapping[code])
    if isinstance(item, pcbnew.FOOTPRINT):
        for pad in item.Pads():
            code = pad.GetNetCode()
            if code in mapping:
                pad.SetNetCode(mapping[code])

def copy_source(rel, tx, ty, rotation, prefix):
    src = pcbnew.LoadBoard(os.path.join(ROOT, rel))
    mapping = net_map(src, prefix)
    items = []
    items.extend(list(src.GetFootprints()))
    items.extend(list(src.GetTracks()))
    items.extend(list(src.GetDrawings()))
    items.extend(list(src.Zones()))
    source_box = src.GetBoardEdgesBoundingBox()
    source_center = source_box.Centre()
    if rotation % 180:
        rotated_w, rotated_h = source_box.GetHeight(), source_box.GetWidth()
    else:
        rotated_w, rotated_h = source_box.GetWidth(), source_box.GetHeight()
    rotated_min = pcbnew.VECTOR2I(source_center.x - rotated_w // 2,
                                  source_center.y - rotated_h // 2)
    shift = pcbnew.VECTOR2I(IU(tx), IU(ty)) - rotated_min
    for original in items:
        # Edge.Cuts from child boards are intentionally omitted; panel has one 100x100 outline.
        if hasattr(original, "GetLayerName") and original.GetLayerName() == "Edge.Cuts":
            continue
        original_net = original.GetNetCode() if hasattr(original, "GetNetCode") else 0
        original_pads = list(original.Pads()) if isinstance(original, pcbnew.FOOTPRINT) else []
        try:
            copied = original.Duplicate(False)
        except TypeError:
            copied = original.Duplicate()
        if rotation:
            copied.Rotate(source_center, pcbnew.EDA_ANGLE(rotation, pcbnew.DEGREES_T))
        copied.Move(shift)
        panel.Add(copied)
        if isinstance(copied, pcbnew.FOOTPRINT):
            for source_pad, copied_pad in zip(original_pads, copied.Pads()):
                copied_pad.SetNetCode(mapping.get(source_pad.GetNetCode(), 0))
        elif hasattr(copied, "SetNetCode"):
            try:
                copied.SetNetCode(mapping.get(original_net, 0))
            except (RuntimeError, SystemError):
                pass

for source in sources:
    copy_source(*source)

def silk_rect(x1, y1, x2, y2):
    for a, b in [((x1, y1), (x2, y1)), ((x2, y1), (x2, y2)),
                 ((x2, y2), (x1, y2)), ((x1, y2), (x1, y1))]:
        shape = pcbnew.PCB_SHAPE(panel, pcbnew.SHAPE_T_SEGMENT)
        shape.SetLayer(pcbnew.F_SilkS)
        shape.SetStart(pcbnew.VECTOR2I(IU(a[0]), IU(a[1])))
        shape.SetEnd(pcbnew.VECTOR2I(IU(b[0]), IU(b[1])))
        shape.SetWidth(IU(0.18))
        panel.Add(shape)

def silk_text(value, x, y, size=1.0, rotation=0):
    label = pcbnew.PCB_TEXT(panel)
    label.SetText(value)
    label.SetPosition(pcbnew.VECTOR2I(IU(x), IU(y)))
    label.SetLayer(pcbnew.F_SilkS)
    label.SetTextSize(pcbnew.VECTOR2I(IU(size), IU(size)))
    label.SetTextThickness(IU(0.16))
    label.SetTextAngle(pcbnew.EDA_ANGLE(rotation, pcbnew.DEGREES_T))
    panel.Add(label)

# Assembly-zone separators and readable identifiers. These are silkscreen
# guides only; the single 100 x 100 mm Edge.Cuts outline remains unchanged.
silk_rect(4.5, 4.5, 64.5, 75.2)
silk_rect(65.0, 4.5, 99.0, 62.5)
silk_rect(4.5, 75.0, 44.5, 99.5)
silk_rect(47.5, 75.0, 87.5, 99.5)
silk_text("KETI / TJA1103 / 100BASE-T1", 82.0, 63.6, 0.72)
silk_text("A", 6.5, 76.4, 0.8)
silk_text("B", 49.5, 76.4, 0.8)

panel.SetTitleBlock(pcbnew.TITLE_BLOCK())
panel.GetTitleBlock().SetTitle("100x100 Mixed KETI + GigaPad + MATEnet Panel")
panel.GetTitleBlock().SetComment(1, "4-up panel: KETI Ethernet, onboard ESP32 GigaPad, 2 passive 2-wire dongles")
for start, end in [((0, 0), (100, 0)), ((100, 0), (100, 100)),
                   ((100, 100), (0, 100)), ((0, 100), (0, 0))]:
    outline = pcbnew.PCB_SHAPE(panel, pcbnew.SHAPE_T_SEGMENT)
    outline.SetLayer(pcbnew.Edge_Cuts)
    outline.SetStart(pcbnew.VECTOR2I(IU(start[0]), IU(start[1])))
    outline.SetEnd(pcbnew.VECTOR2I(IU(end[0]), IU(end[1])))
    outline.SetWidth(IU(0.1))
    panel.Add(outline)

out = os.path.join(ROOT, "N12_Mixed_100x100_Panel.kicad_pcb")
pcbnew.SaveBoard(out, panel)
print(out)
