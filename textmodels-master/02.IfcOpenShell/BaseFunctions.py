import uuid
import time
import tempfile
import ifcopenshell
import math
import os
# Helper function definitions

O = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.

# Creates an ifcAxis2Placement3D from Location, Axis and RefDirection specified as Python tuples
def create_ifcAxis2Placement(ifcfile, point=O, dir1=Z, dir2=X):
    point = ifcfile.createIfcCartesianPoint(point)
    dir1 = ifcfile.createIfcDirection(dir1)
    dir2 = ifcfile.createIfcDirection(dir2)
    axis2placement = ifcfile.createifcAxis2Placement3D(point, dir1, dir2)
    return axis2placement

# Creates an ifcLocalPlacement from Location, Axis and RefDirection, specified as Python tuples, and relative placement
def create_ifcLocalPlacement(ifcfile, point=O, dir1=Z, dir2=X, relative_to=None):
    axis2placement = create_ifcAxis2Placement(ifcfile,point,dir1,dir2)
    ifcLocalPlacement2 = ifcfile.createifcLocalPlacement(relative_to,axis2placement)
    return ifcLocalPlacement2

# Creates an ifcPolyline from a list of points, specified as Python tuples
def create_ifcPolyline(ifcfile, point_list):
    ifcpts = []
    for point in point_list:
        point = ifcfile.createIfcCartesianPoint(point)
        ifcpts.append(point)
    polyline = ifcfile.createifcPolyline(ifcpts)
    return polyline
    
# Creates an ifcExtrudedAreaSolid from a list of points, specified as Python tuples
def create_ifcExtrudedAreaSolid(ifcfile, point_list, ifcAxis2Placement, extrude_dir, extrusion):
    polyline = create_ifcPolyline(ifcfile, point_list)
    ifcclosedprofile = ifcfile.createIfcArbitraryClosedProfileDef("AREA", None, polyline)
    ifcdir = ifcfile.createIfcDirection(extrude_dir)
    ifcExtrudedAreaSolid = ifcfile.createifcExtrudedAreaSolid(ifcclosedprofile, ifcAxis2Placement, ifcdir, extrusion)
    return ifcExtrudedAreaSolid


create_guid = lambda: ifcopenshell.guid.compress(uuid.uuid1().hex)

# IFC template creation
filename = "hello_wall.ifc"

timestamp = time.time()
timestring = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(timestamp))
creator = "Miguel Vega"
organization = "TUM"
application, application_version = "IfcOpenShell", "0.5"
project_globalid, project_name = create_guid(), "Hello Wall"
    
# A template IFC file to quickly populate entity instances for an IfcProject with its dependencies
template = """ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');
FILE_NAME('%(filename)s','%(timestring)s',('%(creator)s'),('%(organization)s'),'%(application)s','%(application)s','');
FILE_SCHEMA(('IFC2X3'));
ENDSEC;
DATA;
#1=IFCPERSON($,$,'%(creator)s',$,$,$,$,$);
#2=IFCORGANIZATION($,'%(organization)s',$,$,$);
#3=IFCPERSONANDORGANIZATION(#1,#2,$);
#4=IFCAPPLICATION(#2,'%(application_version)s','%(application)s','');
#5=IFCOWNERHISTORY(#3,#4,$,.ADDED.,$,#3,#4,%(timestamp)s);
#6=IFCDIRECTION((1.,0.,0.));
#7=IFCDIRECTION((0.,0.,1.));
#8=IFCCARTESIANPOINT((0.,0.,0.));
#9=ifcAxis2Placement3D(#8,#7,#6);
#10=IFCDIRECTION((0.,1.,0.));
#11=IFCGEOMETRICREPRESENTATIONCONTEXT($,'Model',3,1.E-05,#9,#10);
#12=IFCDIMENSIONALEXPONENTS(0,0,0,0,0,0,0);
#13=IFCSIUNIT(*,.LENGTHUNIT.,$,.METRE.);
#14=IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.);
#15=IFCSIUNIT(*,.VOLUMEUNIT.,$,.CUBIC_METRE.);
#16=IFCSIUNIT(*,.PLANEANGLEUNIT.,$,.RADIAN.);
#17=IFCMEASUREWITHUNIT(IFCPLANEANGLEMEASURE(0.017453292519943295),#16);
#18=IFCCONVERSIONBASEDUNIT(#12,.PLANEANGLEUNIT.,'DEGREE',#17);
#19=IFCUNITASSIGNMENT((#13,#14,#15,#18));
#20=IFCPROJECT('%(project_globalid)s',#5,'%(project_name)s',$,$,$,$,(#11),#19);
ENDSEC;
END-ISO-10303-21;
""" % locals()

# Write the template to a temporary file 
temp_handle, temp_filename = tempfile.mkstemp(suffix=".ifc")
with open(temp_filename, "wb") as f:
    f.write(bytes(template, 'utf-8'))
 
# Obtain references to instances defined in template
ifcfile = ifcopenshell.open(temp_filename)
owner_history = ifcfile.by_type("IfcOwnerHistory")[0]
project = ifcfile.by_type("IfcProject")[0]
context = ifcfile.by_type("IfcGeometricRepresentationContext")[0]

# IFC hierarchy creation

site_placement = create_ifcLocalPlacement(ifcfile)
site = ifcfile.createIfcSite(create_guid(), owner_history, "Site", None, None, site_placement, None, None, "ELEMENT", None, None, None, None, None)

building_placement = create_ifcLocalPlacement(ifcfile, relative_to=site_placement)
building = ifcfile.createIfcBuilding(create_guid(), owner_history, 'Building', None, None, building_placement, None, None, "ELEMENT", None, None, None)

storey_placement = create_ifcLocalPlacement(ifcfile, relative_to=building_placement)
elevation = 0.0
building_storey = ifcfile.createIfcBuildingStorey(create_guid(), owner_history, 'Storey', None, None, storey_placement, None, None, "ELEMENT", elevation)

container_storey = ifcfile.createIfcRelAggregates(create_guid(), owner_history, "Building Container", None, building, [building_storey])
container_site = ifcfile.createIfcRelAggregates(create_guid(), owner_history, "Site Container", None, site, [building])
container_project = ifcfile.createIfcRelAggregates(create_guid(), owner_history, "Project Container", None, project, [site])

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