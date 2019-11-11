# the next was taken from the c++ example Open House
#https://github.com/IfcOpenShell/IfcOpenShell/blob/master/src/examples/IfcOpenHouse.cpp
'''
#// A single shape representation can contain multiple representiation items. This way a product
#// can be a composition of multiple solids. The following door will be composed of four boxes
#// which constitute the door and its frame.
IfcSchema::IfcDoor* door = new IfcSchema::IfcDoor(guid(), file.getSingle<IfcSchema::IfcOwnerHistory>(), null, null, null,
	file.addLocalPlacement(storey_placement, 4800, 1600, 0, 0, 0, 1, 0, 1, 0), 0, null, 2200, 1000
#ifdef USE_IFC4
	, IfcSchema::IfcDoorTypeEnum::IfcDoorType_DOOR
	, IfcSchema::IfcDoorTypeOperationEnum::IfcDoorTypeOperation_SINGLE_SWING_LEFT
	, null
#endif
);
door->setRepresentation(file.addBox(80, 80, 2120, 0, file.addPlacement3d(460, 0, 0)));
IfcSchema::IfcRepresentation::list::ptr door_representations = door->Representation()->Representations();
IfcSchema::IfcShapeRepresentation* door_body = 0;
for (IfcSchema::IfcRepresentation::list::it i = door_representations->begin(); i != door_representations->end(); ++i) {
	IfcSchema::IfcRepresentation* rep = *i;
	if (rep->is(IfcSchema::Type::IfcShapeRepresentation) && rep->RepresentationIdentifier() == "Body") {
		door_body = (IfcSchema::IfcShapeRepresentation*) rep;
	}
}
file.addBox(door_body,  80, 80, 2120, 0, file.addPlacement3d(-460, 0,   0));
file.addBox(door_body, 1000, 80,  80, 0, file.addPlacement3d(   0, 0, 2120));
file.addBox(door_body, 860, 30, 2120);
file.addBuildingProduct(door);
file.setSurfaceColour(door->Representation(), 0.9, 0.9, 0.9);
file.addEntity(new IfcSchema::IfcRelFillsElement(guid(), file.getSingle<IfcSchema::IfcOwnerHistory>(), null, null, door_opening, door));

IfcSchema::IfcDoorStyle* door_style = new IfcSchema::IfcDoorStyle(guid(), file.getSingle<IfcSchema::IfcOwnerHistory>(), S("Door type"), null, null, null, null, null,
	IfcSchema::IfcDoorStyleOperationEnum::IfcDoorStyleOperation_SINGLE_SWING_LEFT, IfcSchema::IfcDoorStyleConstructionEnum::IfcDoorStyleConstruction_WOOD, false, false);
file.addRelatedObject<IfcSchema::IfcRelDefinesByType>(door_style, door);
'''