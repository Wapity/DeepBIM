from BaseFunctions import *

def createOpening(x1, y1, x2, y2, height, width, XYZ_openingStartPosition, ifcfile, storey_placement):
    wall_placement = create_ifcLocalPlacement(ifcfile, relative_to=storey_placement)
    opening_placement = create_ifcLocalPlacement(ifcfile, XYZ_openingStartPosition, Z, X, wall_placement)

    #opening_extrusion_placement = create_ifcAxis2Placement(ifcfile, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 0.0, 0.0))
    #point_list_opening_extrusion_area = [(0.0, -0.1, 0.0), 
    #                                     (3.0, -0.1, 0.0), 
    #                                     (3.0,  0.1, 0.0), 
    #                                     (0.0,  0.1, 0.0), 
    #                                     (0.0, -0.1, 0.0)]
    deltaX = x2 - x1
    deltaY = y2 - y1
    lenght = math.sqrt(deltaX*deltaX + deltaY*deltaY)
    Zpoint = 0.0 # the area use as a base for the exrtrution is an horizontal plane
    if deltaX == 0:
        #create wall in plane YZ
        opening_extrusion_placement = create_ifcAxis2Placement(ifcfile, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 1.0, 0.0))
        point_list_opening_extrusion_area = [(y1,           -x1 - width/2,  Zpoint), 
                                     (y1 + lenght,  -x1 - width/2,  Zpoint),
                                     (y1 + lenght,  -x1 + width/2,  Zpoint), 
                                     (y1,           -x1 + width/2,  Zpoint), 
                                     (y1,           -x1 - width/2,  Zpoint)]

    else:
        #create wall in plane XZ
        opening_extrusion_placement = create_ifcAxis2Placement(ifcfile, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 0.0, 0.0))
        point_list_opening_extrusion_area = [(x1,           y1 - width/2,  Zpoint), 
                                        (x1 + lenght,  y1 - width/2,  Zpoint),
                                        (x1 + lenght,  y1 + width/2,  Zpoint), 
                                        (x1,           y1 + width/2,  Zpoint), 
                                        (x1,           y1 - width/2,  Zpoint)]

    opening_solid = create_ifcExtrudedAreaSolid(ifcfile, point_list_opening_extrusion_area, opening_extrusion_placement, Z, height)

    opening_representation = ifcfile.createIfcShapeRepresentation(context, "Body", "SweptSolid", [opening_solid])
    opening_shape = ifcfile.createIfcProductDefinitionShape(None, None, [opening_representation])
    opening_element = ifcfile.createIfcOpeningElement(create_guid(), owner_history, "Opening", "An awesome opening", None, opening_placement, opening_shape, None)
    
    return opening_element
