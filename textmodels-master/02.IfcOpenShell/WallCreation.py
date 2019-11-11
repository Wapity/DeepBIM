from BaseFunctions import *

def create_wall(x1, y1, x2, y2, height, width, ifcfile, storey_placement):

    wall_placement = create_ifcLocalPlacement(ifcfile, relative_to=storey_placement)
    polyline = create_ifcPolyline(ifcfile, [(x1, y1, 0.0), (x2, y2, 0.0)])
    axis_representation = ifcfile.createIfcShapeRepresentation(context, "Axis", "Curve2D", [polyline])

    deltaX = x2 - x1
    deltaY = y2 - y1
    lenght = math.sqrt(deltaX*deltaX + deltaY*deltaY)
    Zpoint = 0.0 # the area use as a base for the exrtrution is an horizontal plane

    if deltaX == 0:
        #create wall in plane YZ
        extrusion_placement = create_ifcAxis2Placement(ifcfile, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 1.0, 0.0))
        point_list_extrusion_area = [(y1,           -x1 - width/2,  Zpoint), 
                                     (y1 + lenght,  -x1 - width/2,  Zpoint),
                                     (y1 + lenght,  -x1 + width/2,  Zpoint), 
                                     (y1,           -x1 + width/2,  Zpoint), 
                                     (y1,           -x1 - width/2,  Zpoint)]

    else:
        #create wall in plane XZ
        extrusion_placement = create_ifcAxis2Placement(ifcfile, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 0.0, 0.0))
        point_list_extrusion_area = [(x1,           y1 - width/2,  Zpoint), 
                                     (x1 + lenght,  y1 - width/2,  Zpoint),
                                     (x1 + lenght,  y1 + width/2,  Zpoint), 
                                     (x1,           y1 + width/2,  Zpoint), 
                                     (x1,           y1 - width/2,  Zpoint)]
    #       create_ifcExtrudedAreaSolid(ifcfile, point_list,                ifcAxis2Placement,   extrude_dir, extrusion):
    solid = create_ifcExtrudedAreaSolid(ifcfile, point_list_extrusion_area, extrusion_placement, (0.0, 0.0, 1.0), height) # I think extrusion is the hight of the wall
    body_representation = ifcfile.createIfcShapeRepresentation(context, "Body", "SweptSolid", [solid])
    product_shape = ifcfile.createIfcProductDefinitionShape(None, None, [axis_representation, body_representation])

    wall = ifcfile.createIfcWallStandardCase(create_guid(), owner_history, "Wall", "An awesome wall", None, wall_placement, product_shape, None)

    # Define and associate the wall material
    defineMaterial(ifcfile, wall, "wall material")

    return wall

def defineMaterial(ifcfile, wall, materialName):
    material = ifcfile.createIfcMaterial("wall material")
    material_layer = ifcfile.createIfcMaterialLayer(material, 0.2, None)
    material_layer_set = ifcfile.createIfcMaterialLayerSet([material_layer], None)
    material_layer_set_usage = ifcfile.createIfcMaterialLayerSetUsage(material_layer_set, "AXIS2", "POSITIVE", -0.1)
    ifcfile.createIfcRelAssociatesMaterial(create_guid(), owner_history, RelatedObjects=[wall], RelatingMaterial=material_layer_set_usage)

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