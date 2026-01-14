# AIST 2025 design script
# created on: 2026/01/09
# last change: 2026/01/09

import gdstk
import numpy as np
import lib

top_cell = gdstk.Cell("top_cell")

PINL100_01_origin = [650, 1000]
PINL100_02_origin = [250, 1000]
PINL250_01_origin = [650,   50]
PINL500_01_origin = [250,   50]

top_cell.add(gdstk.Reference(lib.AIST_PDK["AIST_SwPINL100MZ22HT"], origin=PINL100_01_origin))
top_cell.add(gdstk.Reference(lib.AIST_PDK["AIST_SwPINL100MZ22HT"], origin=PINL100_02_origin))
top_cell.add(gdstk.Reference(lib.AIST_PDK["AIST_SwPINL250MZ22HT"], origin=PINL250_01_origin))
top_cell.add(gdstk.Reference(lib.AIST_PDK["AIST_SwPINL500MZ22HT"], origin=PINL500_01_origin))

ssc_top_origin = [1100, 1500]
ssc_right = lib.new_ssc_cell(lib.LAYER_SiWG, "ssc_right", position='right')
top_cell.add(gdstk.Reference(
	ssc_right,
	origin=[ssc_top_origin[0], ssc_top_origin[1] - 21*lib.ssc_pitch],
	columns=1,
	rows=22,
	spacing=(0, lib.ssc_pitch)
	)
)

loop_straight_length = 5 # um
loop_right = lib.new_loopback_cell(loop_straight_length, lib.LAYER_SiWG, "loopback_right")
top_cell.add(gdstk.Reference(
	loop_right,
	rotation=np.pi,
	x_reflection=True,
	origin=[
		ssc_top_origin[0] - lib.ssc_length - lib.dicing_length,
		ssc_top_origin[1] - 21*lib.ssc_pitch
	],
	columns=1,
	rows=5,
	spacing=(0, 5*lib.ssc_pitch),
	)
)

# PINL100_01 routing
end_point = [
	ssc_top_origin[0] - lib.ssc_length - lib.dicing_length,
	ssc_top_origin[1] - 2 * lib.ssc_pitch
]
PINL100_01_route = lib.PINL100_01_route_cell(PINL100_01_origin, end_point, lib.LAYER_SiWG, "PINL100_01_route")
top_cell.add(gdstk.Reference(PINL100_01_route, origin=(0,0)))

lib.LIB.add(top_cell, *top_cell.dependencies(True))
lib.LIB.write_gds("AIST2025_CR_v1.gds")
