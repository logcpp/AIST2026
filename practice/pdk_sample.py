import gdstk
import numpy as np

lib = gdstk.Library()

AIST_PDK = gdstk.read_rawcells("../PDK_Device_Cells_20251112.gds")

top_cell = gdstk.Cell("top_cell")
top_cell.add(
	gdstk.Reference(AIST_PDK["AIST_SwPINL250MZ22HT"], origin=(0, 0), x_reflection=True, rotation=np.pi/2, columns=32, rows=1, spacing=(500, 0)),
	gdstk.Reference(AIST_PDK["AIST_MMI_2x2"], origin=(100, 0), columns=2, rows=1, spacing=(1000, 0)),
)

output_gds_path = "pdk_sample.gds"
lib.add(top_cell, *top_cell.dependencies(True))
lib.write_gds(output_gds_path)
