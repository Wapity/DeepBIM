
from Functions import *

width = 0.2
height = 1
lenght = 3.0


# Wall creation: Define the wall shape as a polyline axis and an extruded area solid
wall_placement = create_ifcLocalPlacement(ifcfile, relative_to=storey_placement)
polyline = create_ifcPolyline(ifcfile, [(0.0, 0.0, 0.0), (lenght, 0.0, 0.0)])
axis_representation = ifcfile.createIfcShapeRepresentation(context, "Axis", "Curve2D", [polyline])

extrusion_placement = create_ifcAxis2Placement(ifcfile, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 0.0, 0.0))

point_list_extrusion_area = [(0.0, -width/2, 0.0), (lenght, -width/2, 0.0), (lenght, width/2, 0.0), (0.0, width/2, 0.0), (0.0, -width/2, 0.0)]
#       create_ifcExtrudedAreaSolid(ifcfile, point_list,                ifcAxis2Placement,   extrude_dir, extrusion):
solid = create_ifcExtrudedAreaSolid(ifcfile, point_list_extrusion_area, extrusion_placement, (0.0, 0.0, 1.0), height) # I think extrusion is the hight of the wall
body_representation = ifcfile.createIfcShapeRepresentation(context, "Body", "SweptSolid", [solid])
product_shape = ifcfile.createIfcProductDefinitionShape(None, None, [axis_representation, body_representation])

wall = ifcfile.createIfcWallStandardCase(create_guid(), owner_history, "Wall", "An awesome wall", None, wall_placement, product_shape, None)

# Define and associate the wall material
material = ifcfile.createIfcMaterial("wall material")
material_layer = ifcfile.createIfcMaterialLayer(material, 0.2, None)
material_layer_set = ifcfile.createIfcMaterialLayerSet([material_layer], None)
material_layer_set_usage = ifcfile.createIfcMaterialLayerSetUsage(material_layer_set, "AXIS2", "POSITIVE", -0.1)
ifcfile.createIfcRelAssociatesMaterial(create_guid(), owner_history, RelatedObjects=[wall], RelatingMaterial=material_layer_set_usage)


###############################################################################

# Wall2 (woriking) creation: Define the wall shape as a polyline axis and an extruded area solid
'''
wall_placement = create_ifcLocalPlacement(ifcfile, relative_to=storey_placement)
polyline = create_ifcPolyline(ifcfile, [(0.0, 0.0, 0.0), (0.0, lenght, 0.0)])
axis_representation = ifcfile.createIfcShapeRepresentation(context, "Axis", "Curve2D", [polyline])

extrusion_placement = create_ifcAxis2Placement(ifcfile, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 1.0, 0.0))

point_list_extrusion_area = [(0.0, -width/2, 0.0), (lenght, -width/2, 0.0), (lenght, width/2, 0.0), (0.0, width/2, 0.0), (0.0, -width/2, 0.0)]
#       create_ifcExtrudedAreaSolid(ifcfile, point_list,                ifcAxis2Placement,   extrude_dir, extrusion):
solid = create_ifcExtrudedAreaSolid(ifcfile, point_list_extrusion_area, extrusion_placement, (0.0, 0.0, 1.0), height) # I think extrusion is the hight of the wall
body_representation = ifcfile.createIfcShapeRepresentation(context, "Body", "SweptSolid", [solid])
product_shape = ifcfile.createIfcProductDefinitionShape(None, None, [axis_representation, body_representation])

wall = ifcfile.createIfcWallStandardCase(create_guid(), owner_history, "Wall", "An awesome wall", None, wall_placement, product_shape, None)

# Define and associate the wall material
material = ifcfile.createIfcMaterial("wall material")
material_layer = ifcfile.createIfcMaterialLayer(material, 0.2, None)
material_layer_set = ifcfile.createIfcMaterialLayerSet([material_layer], None)
material_layer_set_usage = ifcfile.createIfcMaterialLayerSetUsage(material_layer_set, "AXIS2", "POSITIVE", -0.1)
ifcfile.createIfcRelAssociatesMaterial(create_guid(), owner_history, RelatedObjects=[wall], RelatingMaterial=material_layer_set_usage)

'''

###################################################################################
# Wall3 creation: Define the wall shape as a polyline axis and an extruded area solid
#create_wall(x1, y1, x2, y2, height, width, ifcfile, storey_placement
height = 5
x1 = 2.0
y1 = 1.0
x2 = 2.0
y2 = 6.0
wall = create_wall(x1, y1, x2, y2, height, width, ifcfile, storey_placement)



'''
#the NEXT LINES ARE NOT WORKING: createIfcPropertySingleValue is not found
# Create and assign property set
property_values = [
    ifcfile.createIfcPropertySingleValue("Reference", "Reference", ifcfile.create_entity("IfcText", "Describe the Reference"), None),
    ifcfile.createIfcPropertySingleValue("IsExternal", "IsExternal", ifcfile.create_entity("IfcBoolean", True), None),
    ifcfile.createIfcPropertySingleValue("ThermalTransmittance", "ThermalTransmittance", ifcfile.create_entity("IfcReal", 2.569), None),
    ifcfile.createIfcPropertySingleValue("IntValue", "IntValue", ifcfile.create_entity("IfcInteger", 2), None)
]
property_set = ifcfile.createIfcPropertySet(create_guid(), owner_history, "Pset_WallCommon", None, property_values)
ifcfile.createIfcRelDefinesByProperties(create_guid(), owner_history, None, None, [wall], property_set)
'''

'''
# Add quantity information
quantity_values = [
    ifcfile.createIfcQuantityLength("Length", "Length of the wall", None, 5.0),
    ifcfile.createIfcQuantityArea("Area", "Area of the front face", None, 5.0 * solid.Depth),
    ifcfile.createIfcQuantityVolume("Volume", "Volume of the wall", None, 5.0 * solid.Depth * material_layer.LayerThickness)
]
element_quantity = ifcfile.createIfcElementQuantity(create_guid(), owner_history, "BaseQuantities", None, None, quantity_values)
ifcfile.createIfcRelDefinesByProperties(create_guid(), owner_history, None, None, [wall], element_quantity)
'''



# Create and associate an opening for the window in the wall
opening_placement = create_ifcLocalPlacement(ifcfile, (0.5, 0.0, 1.0), (0.0, 0.0, 1.0), (1.0, 0.0, 0.0), wall_placement)
opening_extrusion_placement = create_ifcAxis2Placement(ifcfile, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 0.0, 0.0))
point_list_opening_extrusion_area = [(0.0, -0.1, 0.0), (3.0, -0.1, 0.0), (3.0, 0.1, 0.0), (0.0, 0.1, 0.0), (0.0, -0.1, 0.0)]
opening_solid = create_ifcExtrudedAreaSolid(ifcfile, point_list_opening_extrusion_area, opening_extrusion_placement, (0.0, 0.0, 1.0), 1.0)
opening_representation = ifcfile.createIfcShapeRepresentation(context, "Body", "SweptSolid", [opening_solid])
opening_shape = ifcfile.createIfcProductDefinitionShape(None, None, [opening_representation])
opening_element = ifcfile.createIfcOpeningElement(create_guid(), owner_history, "Opening", "An awesome opening", None, opening_placement, opening_shape, None)
ifcfile.createIfcRelVoidsElement(create_guid(), owner_history, None, None, wall, opening_element)

'''
# Create a simplified representation for the Window
window_placement = create_ifcLocalPlacement(ifcfile, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 0.0, 0.0), opening_placement)
window_extrusion_placement = create_ifcAxis2Placement(ifcfile, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 0.0, 0.0))
point_list_window_extrusion_area = [(0.0, -0.01, 0.0), (3.0, -0.01, 0.0), (3.0, 0.01, 0.0), (0.0, 0.01, 0.0), (0.0, -0.01, 0.0)]
window_solid = create_ifcExtrudedAreaSolid(ifcfile, point_list_window_extrusion_area, window_extrusion_placement, (0.0, 0.0, 1.0), 1.0)
window_representation = ifcfile.createIfcShapeRepresentation(context, "Body", "SweptSolid", [window_solid])
window_shape = ifcfile.createIfcProductDefinitionShape(None, None, [window_representation])
window = ifcfile.createIfcWindow(create_guid(), owner_history, "Window", "An awesome window", None, window_placement, window_shape, None, None)

# Relate the window to the opening element
ifcfile.createIfcRelFillsElement(create_guid(), owner_history, None, None, opening_element, window)

# Relate the window and wall to the building storey
ifcfile.createIfcRelContainedInSpatialStructure(create_guid(), owner_history, "Building Storey Container", None, [wall, window], building_storey)
'''
# Write the contents of the file to disk

ifcfile.write(filename)
os.system(filename) # open the created IFC file