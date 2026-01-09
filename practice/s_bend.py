# AIST 2026 design script
# created on: 2026/01/09
# last change: 2026/01/09

import gdstk
import numpy as np

lib = gdstk.Library()
top_cell = lib.new_cell("top_cell")

# constants
wg_width = 0.5   # waveguide width (um)
radius = 10      # waveguide bending radius (um)
length = 100.0    # S-shape length (um)
offset = 40     # S-shape vertical offset (um)

def new_flex_path_cell(length, offset, layer, cell_name, gdstk_lib):
	ret_cell = gdstk_lib.new_cell(cell_name)
	points = [(0, 0), (length/2, 0), (length/2, offset), (length, offset)]
	sbend_flex = gdstk.FlexPath(
		points[0],
		wg_width,
		layer=layer,
		datatype=0
	)
	sbend_flex.interpolation(points[1:], angles=[0, None, None, 0])
	ret_cell.add(sbend_flex)
	return ret_cell
	
def new_curve_cell(length, offset, layer, cell_name, gdstk_lib):
	ret_cell = gdstk_lib.new_cell(cell_name)
	c = gdstk.Curve((0, 0)) # start point
	c.cubic([
		(length*0.50, 0),        # control point 1
		(length*0.50, offset),   # control point 1
		(length*1.00, offset),   # end point
	])
	sbend_curve = gdstk.FlexPath(c.points(), wg_width, layer=layer)
	ret_cell.add(sbend_curve)
	return ret_cell

def new_sbend_cell(start, end, layer, cell_name, gdstk_lib):
	sbend_width = end[0] - start[0]
	sbend_height = end[1] - start[1]
	ret_cell = gdstk_lib.new_cell(cell_name)
	path = gdstk.FlexPath(
		(0, 0),
		wg_width,
		layer=layer,
		datatype=0
	)
	path.horizontal(sbend_width/2 - radius)
	path.arc(radius, -np.pi / 2, 0)
	path.vertical(sbend_height - 2*radius, relative=True)
	path.arc(radius, np.pi, np.pi / 2)
	path.horizontal(sbend_width/2 - radius, relative=True)
	ret_cell.add(path)
	return ret_cell

sbend_flexpath = new_flex_path_cell(length, offset, 1, "sbend_flexpath", lib)
sbend_curve = new_curve_cell(length, offset, 1, "sbend_curve", lib)
sbend_circle = new_sbend_cell([0,0], [length,offset], 1, "sbend_circle", lib)

top_cell.add(gdstk.Reference(sbend_flexpath, origin=(0, 100)))
top_cell.add(gdstk.Reference(sbend_curve,    origin=(0,   0)))
top_cell.add(gdstk.Reference(sbend_circle,   origin=(0,-100)))
lib.write_gds("s_bend.gds")
