# bring PIN layers from AIST PDK
# created on: 2026/01/13
# last change: 2026/01/13

import gdstk
import numpy as np

AIST_PDK = gdstk.read_gds("../PDK_Device_Cells_20251112.gds")
for cell in AIST_PDK.cells:
	# Remove any polygons in layer 2
	# cell.filter([(30, 0)], paths=False, labels=False)
	cell.filter([(36, 0)], paths=False, labels=False)
	cell.filter([(38, 0)], paths=False, labels=False)
	cell.filter([(39, 0)], paths=False, labels=False)
	cell.filter([(41, 0)], paths=False, labels=False)
	# # Remove any paths in layer 10
	# cell.filter([(10, 0)], polygons=False, labels=False)

LIB = gdstk.Library()
top_cell = gdstk.Cell("top_cell")
top_cell.add(gdstk.Reference(AIST_PDK["AIST_SwPINL100MZ22HT"], origin=(0,0)))
LIB.add(top_cell, *top_cell.dependencies(True))
LIB.write_gds("pin_mzm_PIN_layer.gds")
