
from BaseFunctions import *
from WallCreation import *
from OpeningCreation import *

###################################################################################
# Wall Creation: Define the wall shape as a polyline axis and an extruded area solid
#create_wall(x1, y1, x2, y2, height, width, ifcfile, storey_placement
height = 5
x1 = 0.0
y1 = 0.0
x2 = 5.0
y2 = 0.0
width = 0.2
wall = create_wall(x1, y1, x2, y2, height, width, ifcfile, storey_placement)


#############################################################################
# Create and associate an opening for the window in the wall

height_opening = 2.0
x1 = 0.0
y1 = 0.0
x2 = 3.0
y2 = 0.0
width = 0.2

XYZ_openingStartPosition = (1.0, 0.0, 2.0) # lower left corner of the opening 

opening_element = createOpening(x1, y1, x2, y2, height_opening, width, XYZ_openingStartPosition, ifcfile, storey_placement)

#Critical opening wall relationship (withopu this the opening is not created)
ifcfile.createIfcRelVoidsElement(create_guid(), owner_history, None, None, wall, opening_element) 



# Create a simplified representation for the Window
window_placement = create_ifcLocalPlacement(ifcfile, (0.0, 0.0, 0.0), Z, X, opening_placement)

window_extrusion_placement = create_ifcAxis2Placement(ifcfile, (0.0, 0.0, 0.0), Z, X)
point_list_window_extrusion_area = [(0.0, -0.01, 0.0), (3.0, -0.01, 0.0), (3.0, 0.01, 0.0), (0.0, 0.01, 0.0), (0.0, -0.01, 0.0)]
window_solid = create_ifcExtrudedAreaSolid(ifcfile, point_list_window_extrusion_area, window_extrusion_placement, (0.0, 0.0, 1.0), 1.0)

window_representation = ifcfile.createIfcShapeRepresentation(context, "Body", "SweptSolid", [window_solid])
window_shape = ifcfile.createIfcProductDefinitionShape(None, None, [window_representation])

window = ifcfile.createIfcWindow(create_guid(), owner_history, "Window", "An awesome window", None, window_placement, window_shape, None, None)

# Relate the window to the opening element
ifcfile.createIfcRelFillsElement(create_guid(), owner_history, None, None, opening_element, window)


ifcfile.createIfcRelAggregates(create_guid(), owner_history,  None, None, window, window_parts)

# Relate the window and wall to the building storey
ifcfile.createIfcRelContainedInSpatialStructure(create_guid(), owner_history, "Building Storey Container", None, [wall, window], building_storey)

# Write the contents of the file to disk

ifcfile.write(filename)
os.system(filename) # open the created IFC file
