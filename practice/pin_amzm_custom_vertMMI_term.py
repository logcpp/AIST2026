# AIST 2025 design library
# created on: 2026/01/13
# last change: 2026/01/24

import gdstk
import numpy as np

AIST_PDK = gdstk.read_rawcells("../PDK_Device_Cells_20251112.gds")
LIB = gdstk.Library()

# design rule
LAYER_SiWG   = 30
LAYER_RIB    = 40
LAYER_NP     = 31 # N+
LAYER_PP     = 32 # P+
LAYER_NPP    = 33 # N++
LAYER_PPP    = 34 # P++
LAYER_TIN    = 38
LAYER_CT2PN  = 35 # contact to P++/N++
LAYER_CT2TIN = 39 # contact to TiN
LAYER_MET    = 36 # AlCu contact and metal wire
LAYER_PW     = 41 # probe window
LAYER_DW     = 42 # deep window (trench)

# constants
wg_width = 0.44        # waveguide width (um)
radius = 10            # waveguide bending radius (um)
dr = 0.1               # straight part length of bent waveguide (um)
dicing_length = 50     # dicing area length, one-side (um)
ssc_width_small = 0.16 # ssc small width (um)
ssc_length = 100       # ssc length (um)
ssc_pitch = 50         # ssc pitch (um)

RF_PAD_PITCH = 125
SIG_width = 10
GND_width = 50
GAP_width = 9
RF_PAD_size = RF_PAD_PITCH - GAP_width
RF_PAD_taper_length = 45
RF_PAD_taper_end = 30.5

def horizontal(origin, length, layer, ret_cell):
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.horizontal(length, relative=True)
	origin_next = [
		origin[0] + length,
		origin[1],
	]
	ret_cell.add(path)
	return origin_next

def vertical(origin, length, layer, ret_cell):
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(length, relative=True)
	origin_next = [
		origin[0],
		origin[1] + length,
	]
	ret_cell.add(path)
	return origin_next

def arc_RU(origin, layer, ret_cell):
	theta_start, theta_end = -np.pi / 2, 0
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.horizontal(dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.vertical(dr, relative=True)
	origin_next = [
		origin[0] + radius + dr,
		origin[1] + radius + dr,
	]
	ret_cell.add(path)
	return origin_next

def arc_RD(origin, layer, ret_cell):
	theta_start, theta_end = np.pi / 2, 0
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.horizontal(dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.vertical(-dr, relative=True)
	origin_next = [
		origin[0] + radius + dr,
		origin[1] - radius - dr,
	]
	ret_cell.add(path)
	return origin_next

def arc_LU(origin, layer, ret_cell):
	theta_start, theta_end = -np.pi / 2, -np.pi
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.horizontal(-dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.vertical(dr, relative=True)
	origin_next = [
		origin[0] - radius - dr,
		origin[1] + radius + dr,
	]
	ret_cell.add(path)
	return origin_next

def arc_LD(origin, layer, ret_cell):
	theta_start, theta_end = np.pi / 2, np.pi
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.horizontal(-dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.vertical(-dr, relative=True)
	origin_next = [
		origin[0] - radius - dr,
		origin[1] - radius - dr,
	]
	ret_cell.add(path)
	return origin_next

def arc_UR(origin, layer, ret_cell):
	theta_start, theta_end = np.pi, np.pi / 2
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.horizontal(dr, relative=True)
	origin_next = [
		origin[0] + radius + dr,
		origin[1] + radius + dr,
	]
	ret_cell.add(path)
	return origin_next

def arc_DR(origin, layer, ret_cell):
	theta_start, theta_end = -np.pi, -np.pi / 2
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(-dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.horizontal(dr, relative=True)
	origin_next = [
		origin[0] + radius + dr,
		origin[1] - radius - dr,
	]
	ret_cell.add(path)
	return origin_next

def arc_UL(origin, layer, ret_cell):
	theta_start, theta_end = 0, np.pi / 2
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.horizontal(-dr, relative=True)
	origin_next = [
		origin[0] - radius - dr,
		origin[1] + radius + dr,
	]
	ret_cell.add(path)
	return origin_next

def arc_DL(origin, layer, ret_cell):
	theta_start, theta_end = 0, -np.pi / 2
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(-dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.horizontal(-dr, relative=True)
	origin_next = [
		origin[0] - radius - dr,
		origin[1] - radius - dr,
	]
	ret_cell.add(path)
	return origin_next

def new_RF_PAD_cell():
	ret_cell = gdstk.Cell("RF_PAD")
	origin=(0,0)
	# GSGSG pad
	for i in range(5):
		pad_offset = i - 2
		#----- LAYER_MET = 36 (AlCu contact and metal wire) -----#
		layer = LAYER_MET
		MET_MIDDLE_corner_botleft = [
			- pad_offset*RF_PAD_PITCH - RF_PAD_size/2,
			origin[1] - RF_PAD_taper_length - RF_PAD_size
		]
		MET_MIDDLE_corner_topright = [
			- pad_offset*RF_PAD_PITCH + RF_PAD_size/2,
			origin[1] - RF_PAD_taper_length
		]
		pad_metal = gdstk.rectangle(MET_MIDDLE_corner_botleft, MET_MIDDLE_corner_topright, layer=layer, datatype=0)
		ret_cell.add(pad_metal)
		#----- LAYER_PW = 41 (AlCu contact and metal wire) -----#
		layer = LAYER_PW
		PW_MIDDLE_corner_botleft = [
			MET_MIDDLE_corner_botleft[0] + 5,
			MET_MIDDLE_corner_botleft[1] + 5,
		]
		PW_MIDDLE_corner_topright = [
			MET_MIDDLE_corner_topright[0] - 5,
			MET_MIDDLE_corner_topright[1] - 5,
		]
		assert RF_PAD_PITCH - (PW_MIDDLE_corner_topright[0]-PW_MIDDLE_corner_botleft[0]) > 4 # design rule
		pad_window = gdstk.rectangle(PW_MIDDLE_corner_botleft, PW_MIDDLE_corner_topright, layer=layer, datatype=0)
		ret_cell.add(pad_window)
	# taper
	#----- LAYER_MET = 36 (AlCu contact and metal wire) -----#
	layer = LAYER_MET
	# middle GND
	taper_middle_GND_botleft  = [ -RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_middle_GND_botright  = [ +RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_middle_GND_topright = [ +RF_PAD_size/2, origin[1] ]
	taper_middle_GND_topleft = [ -RF_PAD_size/2, origin[1] ]
	taper_middle_GND = gdstk.rectangle(taper_middle_GND_botleft, taper_middle_GND_topright, layer=layer, datatype=0)
	ret_cell.add(taper_middle_GND)
	# left SIG
	taper_left_SIG_botleft  = [ -1*RF_PAD_PITCH - RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_left_SIG_botright = [ -1*RF_PAD_PITCH + RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_left_SIG_topright = [ -RF_PAD_PITCH/2 - 4 - 0.5, origin[1] ]
	taper_left_SIG_topleft  = [ -RF_PAD_PITCH/2 - 4 - 0.5 - SIG_width, origin[1] ]
	points = [taper_left_SIG_botleft, taper_left_SIG_botright, taper_left_SIG_topright, taper_left_SIG_topleft]
	taper_left_SIG = gdstk.Polygon(points, layer=layer, datatype=0)
	ret_cell.add(taper_left_SIG)
	# left GND
	taper_left_GND_botleft  = [ -2*RF_PAD_PITCH - RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_left_GND_botright = [ -2*RF_PAD_PITCH + RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_left_GND_topright = [ taper_left_SIG_topleft[0] - GAP_width, origin[1] ]
	taper_left_GND_topleft  = [ taper_left_SIG_topleft[0] - GAP_width - GND_width, origin[1] ]
	points = [taper_left_GND_botleft, taper_left_GND_botright, taper_left_GND_topright, taper_left_GND_topleft]
	taper_left_GND = gdstk.Polygon(points, layer=layer, datatype=0)
	ret_cell.add(taper_left_GND)
	# left SIG
	taper_right_SIG_botleft  = [ +1*RF_PAD_PITCH - RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_right_SIG_botright = [ +1*RF_PAD_PITCH + RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_right_SIG_topright = [ +RF_PAD_PITCH/2 + 4 + 0.5 + SIG_width, origin[1] ]
	taper_right_SIG_topleft  = [ +RF_PAD_PITCH/2 + 4 + 0.5, origin[1] ]
	points = [taper_right_SIG_botleft, taper_right_SIG_botright, taper_right_SIG_topright, taper_right_SIG_topleft]
	taper_right_SIG = gdstk.Polygon(points, layer=layer, datatype=0)
	ret_cell.add(taper_right_SIG)
	# left GND
	taper_right_GND_botleft  = [ +2*RF_PAD_PITCH - RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_right_GND_botright = [ +2*RF_PAD_PITCH + RF_PAD_size/2, origin[1] - RF_PAD_taper_length ]
	taper_right_GND_topright = [ taper_right_SIG_topright[0] + GAP_width + GND_width, origin[1] ]
	taper_right_GND_topleft  = [ taper_right_SIG_topright[0] + GAP_width, origin[1] ]
	points = [taper_right_GND_botleft, taper_right_GND_botright, taper_right_GND_topright, taper_right_GND_topleft]
	taper_right_GND = gdstk.Polygon(points, layer=layer, datatype=0)
	ret_cell.add(taper_right_GND)
	# return point
	ret_points = [
		taper_left_GND_topleft, taper_left_GND_topright,
		taper_left_SIG_topleft, taper_left_SIG_topright,
		taper_middle_GND_topleft, taper_middle_GND_topright,
		taper_right_SIG_topleft, taper_right_SIG_topright,
		taper_right_GND_topleft, taper_right_GND_topright,
	]
	return ret_cell, ret_points
RF_PAD_cell, RF_PAD_cell_points = new_RF_PAD_cell()

# => 30.375 Ω based on sheet resistance = 27 Ω/sq
def new_TIN_SERIES_TERM_cell(TIN_width=80, TIN_length=90):
	# top pads
	ret_cell = gdstk.Cell("TIN_SERIES_TERM_30Ohm")
	pad_origin = (0, 0)
	# GSGSG pad
	for i in range(5):
		pad_offset = i - 2
		#----- LAYER_MET = 36 (AlCu contact and metal wire) -----#
		layer = LAYER_MET
		MET_MIDDLE_corner_botleft = [
			pad_origin[0] - pad_offset*RF_PAD_PITCH - RF_PAD_size/2,
			pad_origin[1] - RF_PAD_taper_length - RF_PAD_size
		]
		MET_MIDDLE_corner_topright = [
			pad_origin[0] - pad_offset*RF_PAD_PITCH + RF_PAD_size/2,
			pad_origin[1] - RF_PAD_taper_length
		]
		pad_metal = gdstk.rectangle(MET_MIDDLE_corner_botleft, MET_MIDDLE_corner_topright, layer=layer, datatype=0)
		ret_cell.add(pad_metal)
		#----- LAYER_PW = 41 (AlCu contact and metal wire) -----#
		layer = LAYER_PW
		PW_MIDDLE_corner_botleft = [
			MET_MIDDLE_corner_botleft[0] + 5,
			MET_MIDDLE_corner_botleft[1] + 5,
		]
		PW_MIDDLE_corner_topright = [
			MET_MIDDLE_corner_topright[0] - 5,
			MET_MIDDLE_corner_topright[1] - 5,
		]
		assert RF_PAD_PITCH - (PW_MIDDLE_corner_topright[0]-PW_MIDDLE_corner_botleft[0]) > 4 # design rule
		pad_window = gdstk.rectangle(PW_MIDDLE_corner_botleft, PW_MIDDLE_corner_topright, layer=layer, datatype=0)
		ret_cell.add(pad_window)
	#----- LAYER_CT2TIN = 39 # contact to TiN -----#
	layer = LAYER_CT2TIN
	contact_width = TIN_width - 3 * 2
	contact_length = 10
	# left
	contact_bot_left_botleft = [
		pad_origin[0] - 1*RF_PAD_PITCH - contact_width/2 + 3,
		pad_origin[1] - RF_PAD_taper_length - 3 - contact_length
	]
	contact_bot_left_topright = [
		pad_origin[0] - 1*RF_PAD_PITCH + contact_width/2 - 3,
		pad_origin[1] - RF_PAD_taper_length - 3
	]
	contact_bot_left = gdstk.rectangle(contact_bot_left_botleft, contact_bot_left_topright, layer=layer, datatype=0)
	ret_cell.add(contact_bot_left)
	# right
	contact_bot_right_botleft = [
		pad_origin[0] + 1*RF_PAD_PITCH - contact_width/2 + 3,
		pad_origin[1] - RF_PAD_taper_length - 3 - contact_length
	]
	contact_bot_right_topright = [
		pad_origin[0] + 1*RF_PAD_PITCH + contact_width/2 - 3,
		pad_origin[1] - RF_PAD_taper_length - 3
	]
	contact_bot_right = gdstk.rectangle(contact_bot_right_botleft, contact_bot_right_topright, layer=layer, datatype=0)
	ret_cell.add(contact_bot_right)
	#----- LAYER_TIN = 38 # contact to TiN -----#
	layer = LAYER_TIN
	# left
	TIN_left_botleft = [
		pad_origin[0] - 1*RF_PAD_PITCH - TIN_width/2 + 3,
		pad_origin[1] - RF_PAD_taper_length - 3 - contact_length - 3
	]
	TIN_left_topright = [
		pad_origin[0] - 1*RF_PAD_PITCH + TIN_width/2 - 3,
		pad_origin[1] - RF_PAD_taper_length - 3 - contact_length - 3 + TIN_length
	]
	TIN_left = gdstk.rectangle(TIN_left_botleft, TIN_left_topright, layer=layer, datatype=0)
	ret_cell.add(TIN_left)
	# right
	TIN_right_botleft = [
		pad_origin[0] + 1*RF_PAD_PITCH - TIN_width/2 + 3,
		pad_origin[1] - RF_PAD_taper_length - 3 - contact_length - 3
	]
	TIN_right_topright = [
		pad_origin[0] + 1*RF_PAD_PITCH + TIN_width/2 - 3,
		pad_origin[1] - RF_PAD_taper_length - 3 - contact_length - 3 + TIN_length
	]
	TIN_right = gdstk.rectangle(TIN_right_botleft, TIN_right_topright, layer=layer, datatype=0)
	ret_cell.add(TIN_right)
	#----- LAYER_CT2TIN = 39 # contact to TiN -----#
	layer = LAYER_CT2TIN
	contact_width = TIN_width - 3 * 2
	contact_length = 10
	# left
	contact_top_left_botleft = [
		contact_bot_left_botleft[0],
		contact_bot_left_botleft[1] + TIN_length - 3 -contact_length - 3
	]
	contact_top_left_topright = [
		contact_bot_left_topright[0],
		contact_bot_left_topright[1] + TIN_length - 3 -contact_length - 3
	]
	contact_top_left = gdstk.rectangle(contact_top_left_botleft, contact_top_left_topright, layer=layer, datatype=0)
	ret_cell.add(contact_top_left)
	# right
	contact_top_right_botleft = [
		contact_bot_right_botleft[0],
		contact_bot_right_botleft[1] + TIN_length - 3 -contact_length - 3
	]
	contact_top_right_topright = [
		contact_bot_right_topright[0],
		contact_bot_right_topright[1] + TIN_length - 3 -contact_length - 3
	]
	contact_top_right = gdstk.rectangle(contact_top_right_botleft, contact_top_right_topright, layer=layer, datatype=0)
	ret_cell.add(contact_top_right)
	#----- LAYER_MET = 36 (AlCu contact and metal wire) -----#
	layer = LAYER_MET
	# GND connection
	for i in range(5):
		pad_offset = i - 2
		if i%2 == 1:
			continue
		#----- LAYER_MET = 36 (AlCu contact and metal wire) -----#
		layer = LAYER_MET
		MET_MIDDLE_corner_botleft = [
			pad_origin[0] - pad_offset*RF_PAD_PITCH - RF_PAD_size/2,
			pad_origin[1] - RF_PAD_taper_length
		]
		MET_MIDDLE_corner_topright = [
			pad_origin[0] - pad_offset*RF_PAD_PITCH + RF_PAD_size/2,
			pad_origin[1] - RF_PAD_taper_length + TIN_length - 16*2
		]
		pad_metal = gdstk.rectangle(MET_MIDDLE_corner_botleft, MET_MIDDLE_corner_topright, layer=layer, datatype=0)
		ret_cell.add(pad_metal)
	return ret_cell
TIN_SERIES_TERM_30Ohm = new_TIN_SERIES_TERM_cell()

def new_PIN_AMZM_cell(PIN_length, cell_name):
	# connection points for use
	MZM_BOTLEFT_CENTER = [0.0, +0.55]
	MZM_BOTRIGHT_CENTER = [0.0, -0.55]
	# constants
	MMI2x2_BOTLEFT_CENTER  = [-0.55, 0.0]
	MMI2x2_BOTRIGHT_CENTER = [+0.55, 0.0]
	MMI2x2_TOPLEFT_CENTER  = [-0.55, 41.016]
	MMI2x2_TOPRIGHT_CENTER = [+0.55, 41.016]
	RF_PAD_PITCH = 125
	RF_PAD_GAP = 9
	AMZM_total_delay_length = 100 # um, total optical path difference
	AMZM_delayloop_length = AMZM_total_delay_length # delay on one side, total delay is doubled to match AMZM_total_delay_length
	assert AMZM_delayloop_length > 0
	routing_waveguide_pitch = 5
	# PIN cell
	PIN_cell, PIN_end_o = PIN_structure(PIN_length, [0,0], cell_name+"_PIN")
	ret_cell = gdstk.Cell(cell_name)
	# SiWG layer = 30
	layer = LAYER_SiWG
	## 2x2 MMI (bottom)
	o = [0, 0]
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_MMI_2x2"], origin=o, rotation=-np.pi/2)); o[0] += MMI2x2_TOPLEFT_CENTER[1]
	MMI_top_point = o.copy()
	## 2x2 MMI (bottom) left ports
	o = [MMI_top_point[0], -MMI2x2_BOTLEFT_CENTER[0]]
	o = arc_RU(o, layer, ret_cell)
	TAPER_BOT_LEFT = o.copy() # savepoint for taper (bottom left)
	ret_cell.add(gdstk.Reference(PIN_cell, origin=o))
	o[0] += PIN_end_o[0]
	o[1] += PIN_end_o[1]
	TAPER_TOP_LEFT = o.copy() # savepoint for taper (top left)
	## 2x2 MMI (bottom) right ports
	o = [MMI_top_point[0], -MMI2x2_BOTRIGHT_CENTER[0]]
	o = horizontal(o, RF_PAD_PITCH, layer, ret_cell) # go pad pitch first, then delay loop
	o = arc_RU(o, layer, ret_cell)
	v = np.abs(MMI2x2_BOTLEFT_CENTER[0] - MMI2x2_BOTRIGHT_CENTER[0])
	o = vertical(o, v, layer, ret_cell)
	TAPER_BOT_RIGHT = o.copy() # savepoint for taper (bottom right)
	ret_cell.add(gdstk.Reference(PIN_cell, origin=o))
	o[0] += PIN_end_o[0]
	o[1] += PIN_end_o[1]
	TAPER_TOP_RIGHT = o.copy() # savepoint for taper (top right)
	# connect to top MMI
	## 2x2 MMI (top) left ports
	o = TAPER_TOP_LEFT.copy()
	v = np.abs(MMI2x2_BOTLEFT_CENTER[0] - MMI2x2_BOTRIGHT_CENTER[0])
	o = vertical(o, v, layer, ret_cell)
	o = arc_UL(o, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	o = arc_DL(o, layer, ret_cell)
	h = -1 * AMZM_delayloop_length / 2
	o = horizontal(o, h, layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	o = vertical(o, routing_waveguide_pitch, layer, ret_cell) # spacing for top MMI and loops
	o = arc_UR(o, layer, ret_cell)
	h = AMZM_delayloop_length / 2
	o = horizontal(o, h, layer, ret_cell)
	o = horizontal(o, RF_PAD_PITCH, layer, ret_cell) # go pad pitch at last
	MMI_bot_point_left = o.copy() # savepoint for top MMI (left port)
	## 2x2 MMI (top) right ports
	o = TAPER_TOP_RIGHT.copy()
	o = arc_UL(o, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	o = arc_DL(o, layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	o = vertical(o, routing_waveguide_pitch, layer, ret_cell) # spacing for top MMI and loops
	o = arc_UR(o, layer, ret_cell)
	MMI_bot_point_right = o.copy() # savepoint for top MMI (right port)
	## 2x2 MMI (top)
	o = [
		MMI_bot_point_right[0],
		(MMI_bot_point_left[1] + MMI_bot_point_right[1]) / 2
	]
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_MMI_2x2"], origin=o, rotation=-np.pi/2)); o[0] += MMI2x2_TOPLEFT_CENTER[1]
	ret_o = o.copy()
	## PIN pad ##
	#----- LAYER_MET = 36 (AlCu contact and metal wire) -----#
	layer = LAYER_MET
	MET_MIDDLE_corner_botleft = [
		TAPER_BOT_LEFT[0] + RF_PAD_GAP/2,
		TAPER_BOT_LEFT[1] + 10 + 20
	]
	MET_MIDDLE_corner_topright = [
		TAPER_BOT_RIGHT[0] - RF_PAD_GAP/2,
		TAPER_BOT_RIGHT[1] + 10 + 20 + PIN_length + 2
	]
	pad_metal = gdstk.rectangle(MET_MIDDLE_corner_botleft, MET_MIDDLE_corner_topright, layer=layer, datatype=0)
	#----- LAYER_PW = 41 (AlCu contact and metal wire) -----#
	layer = LAYER_PW
	PW_MIDDLE_corner_botleft = [
		MET_MIDDLE_corner_botleft[0] + 5,
		MET_MIDDLE_corner_botleft[1] + 5,
	]
	PW_MIDDLE_corner_topright = [
		MET_MIDDLE_corner_topright[0] - 5,
		MET_MIDDLE_corner_topright[1] - 5,
	]
	assert RF_PAD_PITCH - (PW_MIDDLE_corner_topright[0]-PW_MIDDLE_corner_botleft[0]) > 4 # design rule
	pad_window = gdstk.rectangle(PW_MIDDLE_corner_botleft, PW_MIDDLE_corner_topright, layer=layer, datatype=0)
	### create pad cell
	pad_cell = gdstk.Cell(cell_name+"_PIN_PAD")
	pad_cell.add(pad_metal, pad_window)
	### add to ret_cell
	ret_cell.add(
		gdstk.Reference(pad_cell, origin=(-RF_PAD_PITCH*2, 0), columns=5, rows=1, spacing=(RF_PAD_PITCH, 0))
	)
	return ret_cell

def new_PIN_AMZM_TERM_cell(PIN_length, cell_name):
	# connection points for use
	MZM_BOTLEFT_CENTER = [0.0, +0.55]
	MZM_BOTRIGHT_CENTER = [0.0, -0.55]
	# constants
	MMI2x2_BOTLEFT_CENTER  = [-0.55, 0.0]
	MMI2x2_BOTRIGHT_CENTER = [+0.55, 0.0]
	MMI2x2_TOPLEFT_CENTER  = [-0.55, 41.016]
	MMI2x2_TOPRIGHT_CENTER = [+0.55, 41.016]
	AMZM_total_delay_length = 100 # um, total optical path difference
	AMZM_delayloop_length = AMZM_total_delay_length # delay on one side, total delay is doubled to match AMZM_total_delay_length
	assert AMZM_delayloop_length > 0
	routing_waveguide_pitch = 5
	# PIN cell
	PIN_cell, PIN_end_o = PIN_structure(PIN_length, [0,0], cell_name+"_PIN")
	ret_cell = gdstk.Cell(cell_name)
	# SiWG layer = 30
	layer = LAYER_SiWG
	## 2x2 MMI (bottom)
	o = [0, 0]
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_MMI_2x2"], origin=o, rotation=-np.pi/2)); o[0] += MMI2x2_TOPLEFT_CENTER[1]
	MMI_top_point = o.copy()
	## 2x2 MMI (bottom) left ports
	o = [MMI_top_point[0], -MMI2x2_BOTLEFT_CENTER[0]]
	o = arc_RU(o, layer, ret_cell)
	TAPER_BOT_LEFT = o.copy() # savepoint for taper (bottom left)
	ret_cell.add(gdstk.Reference(PIN_cell, origin=o))
	o[0] += PIN_end_o[0]
	o[1] += PIN_end_o[1]
	TAPER_TOP_LEFT = o.copy() # savepoint for taper (top left)
	## 2x2 MMI (bottom) right ports
	o = [MMI_top_point[0], -MMI2x2_BOTRIGHT_CENTER[0]]
	o = horizontal(o, RF_PAD_PITCH, layer, ret_cell) # go pad pitch first, then delay loop
	o = arc_RU(o, layer, ret_cell)
	v = np.abs(MMI2x2_BOTLEFT_CENTER[0] - MMI2x2_BOTRIGHT_CENTER[0])
	o = vertical(o, v, layer, ret_cell)
	TAPER_BOT_RIGHT = o.copy() # savepoint for taper (bottom right)
	ret_cell.add(gdstk.Reference(PIN_cell, origin=o))
	o[0] += PIN_end_o[0]
	o[1] += PIN_end_o[1]
	TAPER_TOP_RIGHT = o.copy() # savepoint for taper (top right)
	# connect to top MMI
	## 2x2 MMI (top) left ports
	o = TAPER_TOP_LEFT.copy()
	v = np.abs(MMI2x2_BOTLEFT_CENTER[0] - MMI2x2_BOTRIGHT_CENTER[0])
	o = vertical(o, v, layer, ret_cell)
	o = arc_UL(o, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	o = arc_DL(o, layer, ret_cell)
	h = -1 * AMZM_delayloop_length / 2
	o = horizontal(o, h, layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	o = vertical(o, routing_waveguide_pitch, layer, ret_cell) # spacing for top MMI and loops
	o = arc_UR(o, layer, ret_cell)
	h = AMZM_delayloop_length / 2
	o = horizontal(o, h, layer, ret_cell)
	o = horizontal(o, RF_PAD_PITCH, layer, ret_cell) # go pad pitch at last
	MMI_bot_point_left = o.copy() # savepoint for top MMI (left port)
	## 2x2 MMI (top) right ports
	o = TAPER_TOP_RIGHT.copy()
	o = arc_UL(o, layer, ret_cell)
	o = arc_LD(o, layer, ret_cell)
	o = arc_DL(o, layer, ret_cell)
	o = arc_LU(o, layer, ret_cell)
	o = vertical(o, routing_waveguide_pitch, layer, ret_cell) # spacing for top MMI and loops
	o = arc_UR(o, layer, ret_cell)
	MMI_bot_point_right = o.copy() # savepoint for top MMI (right port)
	## 2x2 MMI (top)
	o = [
		MMI_bot_point_right[0],
		(MMI_bot_point_left[1] + MMI_bot_point_right[1]) / 2
	]
	ret_cell.add(gdstk.Reference(AIST_PDK["AIST_MMI_2x2"], origin=o, rotation=-np.pi/2)); o[0] += MMI2x2_TOPLEFT_CENTER[1]
	ret_o = o.copy()
	## PAD cell
	SIG_GND_line_length = PIN_length + 1
	PAD_cell = PAD_structure(SIG_GND_line_length, RF_PAD_PITCH, [0,0], cell_name+"PAD")
	PAD_origin = [
		(TAPER_BOT_LEFT[0]+TAPER_BOT_RIGHT[0])/2,
		(TAPER_BOT_LEFT[1]+TAPER_BOT_RIGHT[1])/2 + RF_PAD_taper_end
	]
	ret_cell.add(gdstk.Reference(PAD_cell, origin=PAD_origin))
	## TIN TERM
	TIN_contact_length = 16 * 2
	TIN_length = 90
	TIN_TERM_origin = [
		PAD_origin[0],
		PAD_origin[1] - RF_PAD_size - TIN_length + TIN_contact_length
	]
	ret_cell.add(gdstk.Reference(TIN_SERIES_TERM_30Ohm, origin=TIN_TERM_origin))
	return ret_cell

def PIN_structure(PIN_length, start_point, cell_name):
	# LAYER_SiWG   = 30
	# LAYER_RIB    = 40
	# LAYER_NP     = 31 # N+
	# LAYER_PP     = 32 # P+
	# LAYER_NPP    = 33 # N++
	# LAYER_PPP    = 34 # P++
	# LAYER_TIN    = 38 <------ not used here
	# LAYER_CT2PN  = 35 # contact to P++/N++
	# LAYER_CT2TIN = 39 # contact to TiN <------ not used here
	# LAYER_MET    = 36 # AlCu contact and metal wire
	# LAYER_PW     = 41 # probe window
	# LAYER_DW     = 42 # deep window (trench) <------ not used here
	ret_cell = gdstk.Cell(cell_name)
	#----- LAYER_SiWG = 30 -----#
	layer = LAYER_SiWG
	o = start_point.copy()
	# taper (bottom)
	path = gdstk.FlexPath(o, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(10, 0.51, relative=True); o[1] += 10
	ret_cell.add(path)
	path = gdstk.FlexPath(o, 0.51, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(20, 2.00, relative=True); o[1] += 20
	ret_cell.add(path)
	# rectangle
	path = gdstk.FlexPath(o, 30, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(PIN_length + 2, relative=True); o[1] += PIN_length + 2
	ret_cell.add(path)
	# taper (top)
	path = gdstk.FlexPath(o, 2.00, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(20, 0.51, relative=True); o[1] += 20
	ret_cell.add(path)
	path = gdstk.FlexPath(o, 0.51, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(10, wg_width, relative=True); o[1] += 10
	ret_cell.add(path)
	ret_o = o.copy() # <--- return value of taper end of Si waveguide
	#----- LAYER_RIB = 40 -----#
	layer = LAYER_RIB
	o = start_point.copy()
	rib_start_point = o.copy()
	rib_paths = []
	# taper (rib): 2um wider than waveguide rib
	path = gdstk.FlexPath(o, 2.44, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(10, 2.51, relative=True); o[1] += 10
	path.vertical(19, 4.00, relative=True); o[1] += 19
	rib_paths.append(path)
	# rectangle (rib)
	path = gdstk.FlexPath(o, 32, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(PIN_length + 4, relative=True); o[1] += PIN_length + 4
	rib_paths.append(path)
	# taper (rib)
	path = gdstk.FlexPath(o, 4.00, layer=layer, datatype=0, tolerance=1e-3)
	path.vertical(19, 2.51, relative=True); o[1] += 19
	path.vertical(10, 2.44, relative=True); o[1] += 10
	rib_paths.append(path)
	rib_end_point = o.copy()
	# NOT region
	not_path = gdstk.FlexPath(rib_start_point, 0.51, layer=layer, datatype=0, tolerance=1e-3)
	not_path.vertical(np.abs(rib_end_point[1]-rib_start_point[1]), relative=True)
	# Boolean
	rib = gdstk.boolean(rib_paths, not_path, "not", precision=1e-3, layer=layer, datatype=0)
	ret_cell.add(*rib)
	# TODO: N+,N++ should be on the right, and P+,P++ should be on the left -> gdstk.Reference(x_reflection=True, rotation=np.pi)
	#----- LAYER_NP = 31 (N+) -----#
	layer = LAYER_NP
	o = start_point.copy()
	NP_corner_botright = [
		o[0] - 0.5,
		o[1] + 10 + 19 + 1.0 + 0.5
	]
	NP_corner_topleft = [
		NP_corner_botright[0] - 14,
		NP_corner_botright[1] + PIN_length + 1,
	]
	NP_rectangle = gdstk.rectangle(NP_corner_botright, NP_corner_topleft, layer=layer, datatype=0)
	ret_cell.add(NP_rectangle)
	#----- LAYER_PP = 32 (P+) -----#
	layer = LAYER_PP
	o = start_point.copy()
	PP_corner_botleft = [
		o[0] + 0.5,
		o[1] + 10 + 19 + 1.0 + 0.5
	]
	PP_corner_topright = [
		PP_corner_botleft[0] + 14,
		PP_corner_botleft[1] + PIN_length + 1,
	]
	PP_rectangle = gdstk.rectangle(PP_corner_botleft, PP_corner_topright, layer=layer, datatype=0)
	ret_cell.add(PP_rectangle)
	#----- LAYER_NPP = 33 (N++) -----#
	layer = LAYER_NPP
	o = start_point.copy()
	NPP_corner_botright = [
		NP_corner_botright[0] - 0.65,
		NP_corner_botright[1] + 0.5
	]
	NPP_corner_topleft = [
		NP_corner_topleft[0],
		NP_corner_topleft[1] - 0.5,
	]
	assert NPP_corner_topleft[1] - NPP_corner_botright[1] == PIN_length
	NPP_rectangle = gdstk.rectangle(NPP_corner_botright, NPP_corner_topleft, layer=layer, datatype=0)
	ret_cell.add(NPP_rectangle)
	#----- LAYER_PPP = 34 (P++) -----#
	layer = LAYER_PPP
	o = start_point.copy()
	PPP_corner_botleft = [
		PP_corner_botleft[0] + 0.65,
		PP_corner_botleft[1] + 0.5
	]
	PPP_corner_topright = [
		PP_corner_topright[0],
		PP_corner_topright[1] - 0.5,
	]
	assert PPP_corner_topright[1] - PPP_corner_botleft[1] == PIN_length
	PPP_rectangle = gdstk.rectangle(PPP_corner_botleft, PPP_corner_topright, layer=layer, datatype=0)
	ret_cell.add(PPP_rectangle)
	#----- LAYER_CT2PN = 35 (contact to P++/N++) -----#
	layer = LAYER_CT2PN
	o = start_point.copy()
	CT2PN_LEFT_corner_botright = [
		NP_corner_botright[0] - 5.5,
		NP_corner_botright[1] + 0.5 + 1
	]
	CT2PN_LEFT_corner_topleft = [
		NP_corner_topleft[0] + 1.5,
		NP_corner_topleft[1] - 0.5 - 1
	]
	assert np.abs(CT2PN_LEFT_corner_topleft[0] - CT2PN_LEFT_corner_botright[0]) == 7
	assert np.abs(CT2PN_LEFT_corner_topleft[1] - CT2PN_LEFT_corner_botright[1]) == PIN_length - 2
	CT2PN_LEFT_rectangle = gdstk.rectangle(CT2PN_LEFT_corner_botright, CT2PN_LEFT_corner_topleft, layer=layer, datatype=0)
	ret_cell.add(CT2PN_LEFT_rectangle)
	#----- LAYER_CT2PN = 35 (contact to P++/N++) -----#
	layer = LAYER_CT2PN
	o = start_point.copy()
	CT2PN_RIGHT_corner_botleft = [
		PP_corner_botleft[0] + 5.5,
		PP_corner_botleft[1] + 0.5 + 1
	]
	CT2PN_RIGHT_corner_topright = [
		PP_corner_topright[0] - 1.5,
		PP_corner_topright[1] - 0.5 - 1,
	]
	assert np.abs(CT2PN_RIGHT_corner_botleft[0] - CT2PN_RIGHT_corner_topright[0]) == 7
	assert np.abs(CT2PN_RIGHT_corner_botleft[1] - CT2PN_RIGHT_corner_topright[1]) == PIN_length - 2
	CT2PN_RIGHT_rectangle = gdstk.rectangle(CT2PN_RIGHT_corner_botleft, CT2PN_RIGHT_corner_topright, layer=layer, datatype=0)
	ret_cell.add(CT2PN_RIGHT_rectangle)
	return ret_cell, ret_o

def PAD_structure(PIN_length, RF_PAD_PITCH, start_point, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	taper_left_GND_topleft    = RF_PAD_cell_points[0]
	taper_left_GND_topright   = RF_PAD_cell_points[1]
	taper_left_SIG_topleft    = RF_PAD_cell_points[2]
	taper_left_SIG_topright   = RF_PAD_cell_points[3]
	taper_middle_GND_topleft  = RF_PAD_cell_points[4]
	taper_middle_GND_topright = RF_PAD_cell_points[5]
	taper_right_SIG_topleft   = RF_PAD_cell_points[6]
	taper_right_SIG_topright  = RF_PAD_cell_points[7]
	taper_right_GND_topleft   = RF_PAD_cell_points[8]
	taper_right_GND_topright  = RF_PAD_cell_points[9]
	# bottom pads
	ret_cell.add(gdstk.Reference(RF_PAD_cell))
	# metal line
	layer = LAYER_MET
	left_GND_line = gdstk.rectangle(
		taper_left_GND_topleft,
		[taper_left_GND_topright[0], taper_left_GND_topright[1] + PIN_length],
		layer=layer, datatype=0
	)
	left_SIG_line = gdstk.rectangle(
		taper_left_SIG_topleft,
		[taper_left_SIG_topright[0], taper_left_SIG_topright[1] + PIN_length],
		layer=layer, datatype=0
	)
	middle_GND_line = gdstk.rectangle(
		taper_middle_GND_topleft,
		[taper_middle_GND_topright[0], taper_middle_GND_topright[1] + PIN_length],
		layer=layer, datatype=0
	)
	right_SIG_line = gdstk.rectangle(
		taper_right_SIG_topleft,
		[taper_right_SIG_topright[0], taper_right_SIG_topright[1] + PIN_length],
		layer=layer, datatype=0
	)
	right_GND_line = gdstk.rectangle(
		taper_right_GND_topleft,
		[taper_right_GND_topright[0], taper_right_GND_topright[1] + PIN_length],
		layer=layer, datatype=0
	)
	ret_cell.add(left_GND_line)
	ret_cell.add(left_SIG_line)
	ret_cell.add(middle_GND_line)
	ret_cell.add(right_SIG_line)
	ret_cell.add(right_GND_line)
	# top pads
	ret_cell.add(gdstk.Reference(RF_PAD_cell, origin=(0, PIN_length), x_reflection=True))
	return ret_cell

def PINL100_01_route_cell(pos, end_point, layer, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	# top right port
	o = [
		pos[0] + 50,
		pos[1] + 492.916,
	]
	path = gdstk.FlexPath(o, wg_width, layer=layer, datatype=0, tolerance=1e-3)
	o = vertical(o, 10, layer, ret_cell)
	o = arc_UR(o, layer, ret_cell)
	o = horizontal(o, 50, layer, ret_cell)
	o = arc_RD(o, layer, ret_cell)
	vertical_length = o[1] - end_point[1] - radius - dr
	o = vertical(o, -vertical_length, layer, ret_cell)
	o = arc_DR(o, layer, ret_cell)
	horizontal_length = end_point[0] - o[0]
	o = horizontal(o, horizontal_length, layer, ret_cell)
	ret_cell.add(path)
	return ret_cell

top_cell = gdstk.Cell("top_cell")

pin_mzm_L100 = new_PIN_AMZM_cell(100, "CR_PINL100AMZ")
pin_mzm_L100_term = new_PIN_AMZM_TERM_cell(100, "CR_PINL100AMZ_TERM")
pin_mzm_L200 = new_PIN_AMZM_cell(200, "CR_PINL200AMZ")
pin_mzm_L200_term = new_PIN_AMZM_TERM_cell(200, "CR_PINL200AMZ_TERM")
pin_mzm_L500 = new_PIN_AMZM_cell(500, "CR_PINL500AMZ")
pin_mzm_L500_term = new_PIN_AMZM_TERM_cell(500, "CR_PINL500AMZ_TERM")

PINL100_01_origin = [0, 0]
PINL100_term_01_origin = [750, 0]
PINL200_01_origin = [0, 750]
PINL200_term_01_origin = [750, 750]
PINL500_01_origin = [0, 1500]
PINL500_term_01_origin = [750, 1500]

# PINL100_01_origin = [750, 1000]
# PINL100_02_origin = [250, 1000]
# PINL250_01_origin = [750,   50]
# PINL500_01_origin = [250,   50]

top_cell.add(gdstk.Reference(pin_mzm_L100, origin=PINL100_01_origin))
top_cell.add(gdstk.Reference(pin_mzm_L100_term, origin=PINL100_term_01_origin))
top_cell.add(gdstk.Reference(pin_mzm_L200, origin=PINL200_01_origin))
top_cell.add(gdstk.Reference(pin_mzm_L200_term, origin=PINL200_term_01_origin))
top_cell.add(gdstk.Reference(pin_mzm_L500, origin=PINL500_01_origin))
top_cell.add(gdstk.Reference(pin_mzm_L500_term, origin=PINL500_term_01_origin))

LIB.add(top_cell, *top_cell.dependencies(True))
LIB.write_gds("pin_amzm_custom_vertMMI_term.gds")
