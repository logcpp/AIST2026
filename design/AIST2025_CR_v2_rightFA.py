# AIST 2025 design script
# created on: 2026/01/18
# last change: 2026/01/18

import gdstk
import numpy as np
import lib_v2 as lib

top_cell = gdstk.Cell("top_cell")

#---------- total chip area ----------#
CHIP_WIDTH = 5000
CHIP_HEIGHT = 10000
JIANG_HEIGHT = 3500
SHERRY_HEIGHT = 1500
chip_area_JIANG = gdstk.rectangle([0, 0], [CHIP_WIDTH, JIANG_HEIGHT], layer=0, datatype=0)
chip_area_SHERRY_REN = gdstk.rectangle([0, JIANG_HEIGHT], [CHIP_WIDTH, JIANG_HEIGHT+SHERRY_HEIGHT], layer=0, datatype=0)
chip_area_SUGANUMA_LEFT = gdstk.rectangle([0, JIANG_HEIGHT+SHERRY_HEIGHT], [CHIP_WIDTH/2, CHIP_HEIGHT], layer=0, datatype=0)
chip_area_SUGANUMA_RIGHT = gdstk.rectangle([CHIP_WIDTH/2, JIANG_HEIGHT+SHERRY_HEIGHT], [CHIP_WIDTH, CHIP_HEIGHT], layer=0, datatype=0)
top_cell.add(
	chip_area_JIANG,
	chip_area_SHERRY_REN,
	chip_area_SUGANUMA_LEFT,
	chip_area_SUGANUMA_RIGHT,
)

#---------- GC test patterns ----------#
GC_pitch = 120 # <-- based on simulation
GC_io_distance = 500 # distance between array **centers**
GC_input_origin = [
	500,
	CHIP_HEIGHT - 500 - GC_io_distance - GC_pitch*1.5,
]
GC_output_origin = [
	GC_input_origin[0],
	GC_input_origin[1] + GC_io_distance - GC_pitch*1.5,
]
GC_grating_num = 20
GC_grating_pitch = 0.6
GC_grating_angle_deg = 35
GC_taper_length = 10
GC_T20P0_6A35L10 = lib.new_GC_cell(GC_grating_num, GC_grating_pitch, GC_grating_angle_deg, GC_taper_length, "GC_T20P0.6A35L10")
top_cell.add(
	# input 1x4 GC array
	gdstk.Reference(
		GC_T20P0_6A35L10,
		# rotation=np.pi/2,
		origin=GC_input_origin,
		columns=4,
		rows=1,
		spacing=(GC_pitch, GC_pitch)
	),
	# output 4x4 GC array
	gdstk.Reference(
		GC_T20P0_6A35L10,
		# rotation=-np.pi/2,
		origin=GC_output_origin,
		columns=4,
		rows=4,
		spacing=(GC_pitch, GC_pitch)
	)
)

#---------- MZM test patterns ----------#
o = [400, JIANG_HEIGHT]
PINL200_01_origin = [o[0]+500, o[1]+ 950]
PINL200_02_origin = [o[0],     o[1]+ 950]
PINL500_01_origin = [o[0]+500, o[1]+  80]
PINL500_02_origin = [o[0],     o[1]+  80]
pin_mzm_L200, pin_mzm_L200_end_o = lib.new_PIN_MZM_cell(200, "CR_PINL200MZ")
pin_mzm_L500, pin_mzm_L500_end_o = lib.new_PIN_MZM_cell(500, "CR_PINL500MZ")
top_cell.add(gdstk.Reference(pin_mzm_L200, origin=PINL200_01_origin))
top_cell.add(gdstk.Reference(pin_mzm_L200, origin=PINL200_02_origin))
top_cell.add(gdstk.Reference(pin_mzm_L500, origin=PINL500_01_origin))
top_cell.add(gdstk.Reference(pin_mzm_L500, origin=PINL500_02_origin))

#---------- right ssc region ----------#
ssc_bot_origin = [5000, JIANG_HEIGHT+50]
ssc_right = lib.new_ssc_cell(lib.LAYER_SiWG, "ssc_right", position='right')
top_cell.add(
	# ssc for MZM
	gdstk.Reference(
		ssc_right,
		origin=[ssc_bot_origin[0], ssc_bot_origin[1]],
		columns=1,
		rows=16,
		spacing=(0, lib.ssc_pitch)
	),
	# ssc for GC array
	gdstk.Reference(
		ssc_right,
		origin=[ssc_bot_origin[0], ssc_bot_origin[1]-18*lib.ssc_pitch],
		columns=1,
		rows=18,
		spacing=(0, lib.ssc_pitch)
	)
)
loop_straight_length = 5 # um
loop_right = lib.new_loopback_cell(loop_straight_length, lib.LAYER_SiWG, "loopback_right")
top_cell.add(
	# loopbacks of ssc for MZM
	gdstk.Reference(
		loop_right, rotation=np.pi, x_reflection=True,
		origin=[
			ssc_bot_origin[0] - lib.ssc_length - lib.dicing_length,
			ssc_bot_origin[1]
		]
	),
	gdstk.Reference(
		loop_right, rotation=np.pi, x_reflection=True,
		origin=[
			ssc_bot_origin[0] - lib.ssc_length - lib.dicing_length,
			ssc_bot_origin[1] + lib.ssc_pitch*14
		]
	),
	# loopbacks of ssc for GC array
	gdstk.Reference(
		loop_right, rotation=np.pi, x_reflection=True,
		origin=[
			ssc_bot_origin[0] - lib.ssc_length - lib.dicing_length,
			ssc_bot_origin[1] - lib.ssc_pitch*18
		]
	),
)

#---------- PINL200_01 (top right) routing ----------#
end_point = [
	ssc_bot_origin[0] - lib.ssc_length - lib.dicing_length,
	ssc_bot_origin[1] + 13 * lib.ssc_pitch
]
PINL200_01_route = lib.PINL200_01_route_cell(PINL200_01_origin, pin_mzm_L200_end_o, end_point, lib.LAYER_SiWG, "PINL200_01_route")
PINL500_01_route = lib.PINL500_01_route_cell(PINL500_01_origin, pin_mzm_L500_end_o, end_point, lib.LAYER_SiWG, "PINL500_01_route")
PINL200_02_route = lib.PINL200_02_route_cell(PINL200_02_origin, pin_mzm_L200_end_o, end_point, lib.LAYER_SiWG, "PINL200_02_route")
PINL500_02_route = lib.PINL500_02_route_cell(PINL500_02_origin, pin_mzm_L500_end_o, end_point, lib.LAYER_SiWG, "PINL500_02_route")
top_cell.add(gdstk.Reference(PINL200_01_route, origin=(0,0)))
top_cell.add(gdstk.Reference(PINL500_01_route, origin=(0,0)))
top_cell.add(gdstk.Reference(PINL200_02_route, origin=(0,0)))
top_cell.add(gdstk.Reference(PINL500_02_route, origin=(0,0)))

lib.LIB.add(top_cell, *top_cell.dependencies(True))
lib.LIB.write_gds("AIST2025_CR_v2_rightFA.gds")
