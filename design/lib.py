# AIST 2025 design library
# created on: 2026/01/09
# last change: 2026/01/09

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

def get_cell_size(cell):
	min_xy, max_xy = cell.bounding_box()
	width = max_xy[0] - min_xy[0]
	height = max_xy[1] - min_xy[1]
	return width, height

def horizontal(origin, length, layer):
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0)
	path.horizontal(length, relative=True)
	origin_next = [
		origin[0] + length,
		origin[1],
	]
	return path, origin_next

def vertical(origin, length, layer):
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0)
	path.vertical(length, relative=True)
	origin_next = [
		origin[0],
		origin[1] + length,
	]
	return path, origin_next

def arc_RU(origin, layer):
	theta_start, theta_end = -np.pi / 2, 0
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0)
	path.horizontal(dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.vertical(dr, relative=True)
	origin_next = [
		origin[0] + radius + dr,
		origin[1] + radius + dr,
	]
	return path, origin_next

def arc_RD(origin, layer):
	theta_start, theta_end = np.pi / 2, 0
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0)
	path.horizontal(dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.vertical(-dr, relative=True)
	origin_next = [
		origin[0] + radius + dr,
		origin[1] - radius - dr,
	]
	return path, origin_next

def arc_LU(origin, layer):
	theta_start, theta_end = -np.pi / 2, -np.pi
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0)
	path.horizontal(-dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.vertical(dr, relative=True)
	origin_next = [
		origin[0] - radius - dr,
		origin[1] + radius + dr,
	]
	return path, origin_next

def arc_LD(origin, layer):
	theta_start, theta_end = np.pi / 2, np.pi
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0)
	path.horizontal(-dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.vertical(-dr, relative=True)
	origin_next = [
		origin[0] - radius - dr,
		origin[1] - radius - dr,
	]
	return path, origin_next

def arc_UR(origin, layer):
	theta_start, theta_end = np.pi, np.pi / 2
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0)
	path.vertical(dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.horizontal(dr, relative=True)
	origin_next = [
		origin[0] + radius + dr,
		origin[1] + radius + dr,
	]
	return path, origin_next

def arc_DR(origin, layer):
	theta_start, theta_end = -np.pi, -np.pi / 2
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0)
	path.vertical(-dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.horizontal(dr, relative=True)
	origin_next = [
		origin[0] + radius + dr,
		origin[1] - radius - dr,
	]
	return path, origin_next

def arc_UL(origin, layer):
	theta_start, theta_end = 0, np.pi / 2
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0)
	path.vertical(dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.horizontal(-dr, relative=True)
	origin_next = [
		origin[0] - radius - dr,
		origin[1] + radius + dr,
	]
	return path, origin_next

def arc_DL(origin, layer):
	theta_start, theta_end = 0, -np.pi / 2
	path = gdstk.FlexPath(origin, wg_width, layer=layer, datatype=0)
	path.vertical(-dr, relative=True)
	path.arc(radius, theta_start, theta_end)
	path.horizontal(-dr, relative=True)
	origin_next = [
		origin[0] - radius - dr,
		origin[1] - radius - dr,
	]
	return path, origin_next

def new_sbend_RUR_cell(start, end, layer, cell_name):
	sbend_width = end[0] - start[0]
	sbend_height = end[1] - start[1]
	assert sbend_width > 0
	assert sbend_height > 0
	ret_cell = gdstk.Cell(cell_name)
	o = start
	path, o = horizontal(o, sbend_width/2 - (radius + dr), layer); ret_cell.add(path)
	path, o = arc_RU(o, layer); ret_cell.add(path)
	path, o = vertical(o, sbend_height - 2*(radius + dr), layer); ret_cell.add(path)
	path, o = arc_UR(o, layer); ret_cell.add(path)
	path, o = horizontal(o, sbend_width/2 - (radius + dr), layer); ret_cell.add(path)
	return ret_cell

def new_sbend_RDR_cell(start, end, layer, cell_name):
	sbend_width = end[0] - start[0]
	sbend_height = end[1] - start[1]
	assert sbend_width > 0
	assert sbend_height < 0
	ret_cell = gdstk.Cell(cell_name)
	o = start
	path, o = horizontal(o, sbend_width/2 - (radius + dr), layer); ret_cell.add(path)
	path, o = arc_RD(o, layer); ret_cell.add(path)
	path, o = vertical(o, sbend_height + 2*(radius + dr), layer); ret_cell.add(path)
	path, o = arc_DR(o, layer); ret_cell.add(path)
	path, o = horizontal(o, sbend_width/2 - (radius + dr), layer); ret_cell.add(path)
	return ret_cell

def new_sbend_LUL_cell(start, end, layer, cell_name):
	sbend_width = end[0] - start[0]
	sbend_height = end[1] - start[1]
	assert sbend_width < 0
	assert sbend_height > 0
	ret_cell = gdstk.Cell(cell_name)
	o = start
	path, o = horizontal(o, sbend_width/2 + (radius + dr), layer); ret_cell.add(path)
	path, o = arc_LU(o, layer); ret_cell.add(path)
	path, o = vertical(o, sbend_height - 2*(radius + dr), layer); ret_cell.add(path)
	path, o = arc_UL(o, layer); ret_cell.add(path)
	path, o = horizontal(o, sbend_width/2 + (radius + dr), layer); ret_cell.add(path)
	return ret_cell

def new_sbend_LDL_cell(start, end, layer, cell_name):
	sbend_width = end[0] - start[0]
	sbend_height = end[1] - start[1]
	assert sbend_width < 0
	assert sbend_height < 0
	ret_cell = gdstk.Cell(cell_name)
	o = start
	path, o = horizontal(o, sbend_width/2 + (radius + dr), layer); ret_cell.add(path)
	path, o = arc_LD(o, layer); ret_cell.add(path)
	path, o = vertical(o, sbend_height + 2*(radius + dr), layer); ret_cell.add(path)
	path, o = arc_DL(o, layer); ret_cell.add(path)
	path, o = horizontal(o, sbend_width/2 + (radius + dr), layer); ret_cell.add(path)
	return ret_cell

def new_ssc_cell(layer, cell_name, position='left'):
	length = ssc_length # um
	width_small = ssc_width_small # um
	width_large = wg_width # um
	ret_cell = gdstk.Cell(cell_name)
	if position == 'left':
		path = gdstk.FlexPath((-dicing_length, 0), width_small, layer=layer, datatype=0)
		path.horizontal(dicing_length, relative=True)
		ret_cell.add(path)
		path = gdstk.FlexPath((0, 0), width_small, layer=layer, datatype=0)
		path.horizontal(dicing_length, relative=True)
		ret_cell.add(path)
		path = gdstk.FlexPath((dicing_length, 0), width_small, layer=layer, datatype=0)
		path.horizontal(length, width=width_large, relative=True)
		ret_cell.add(path)
	else:
		path = gdstk.FlexPath((-length-dicing_length, 0), width_large, layer=layer, datatype=0)
		path.horizontal(length, width=width_small, relative=True)
		ret_cell.add(path)
		path = gdstk.FlexPath((-dicing_length, 0), width_small, layer=layer, datatype=0)
		path.horizontal(dicing_length, relative=True)
		ret_cell.add(path)
		path = gdstk.FlexPath((0, 0), width_small, layer=layer, datatype=0)
		path.horizontal(dicing_length, relative=True)
		ret_cell.add(path)
	return ret_cell

def new_loopback_cell(straight_length, layer, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	o = (0, 0)
	path, o = horizontal(o, straight_length, layer); ret_cell.add(path)
	path, o = arc_RU(o, layer); ret_cell.add(path)
	path, o = vertical(o, ssc_pitch-2*(radius+dr), layer); ret_cell.add(path)
	path, o = arc_UL(o, layer); ret_cell.add(path)
	path, o = horizontal(o, -straight_length, layer); ret_cell.add(path)
	return ret_cell

def PINL100_01_route_cell(pos, end_point, layer, cell_name):
	ret_cell = gdstk.Cell(cell_name)
	# top right port
	o = [
		pos[0] + 50,
		pos[1] + 492.916,
	]
	path = gdstk.FlexPath(o, wg_width, layer=layer, datatype=0)
	path, o = vertical(o, 10, layer); ret_cell.add(path)
	path, o = arc_UR(o, layer); ret_cell.add(path)
	path, o = horizontal(o, 50, layer); ret_cell.add(path)
	path, o = arc_RD(o, layer); ret_cell.add(path)
	vertical_length = o[1] - end_point[1] - radius - dr
	path, o = vertical(o, -vertical_length, layer); ret_cell.add(path)
	path, o = arc_DR(o, layer); ret_cell.add(path)
	horizontal_length = end_point[0] - o[0]
	path, o = horizontal(o, horizontal_length, layer); ret_cell.add(path)
	ret_cell.add(path)
	return ret_cell
