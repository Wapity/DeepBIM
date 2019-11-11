using System;
using Xbim.Ifc;
using Xbim.Ifc2x3.GeometryResource;

namespace xBIMTest
{
    class Program
    {
        static void Main()
        {
            string fileName = @"../path/to/Sample.ifc";

            // Open the file
            using (var model = IfcStore.Open(fileName))
            {
				// Start transaction to modify the model
                using (var txn = model.BeginTransaction("Create Point"))
                {
					//Create the point
                    var Point = model.Instances.New<IfcCartesianPoint>();
                    Point.SetXY(10, 11);
                }

                //Save the changed model.
				//IfcStore will use the extension to save it as *.ifc, *.ifczip or *.ifcxml.
                model.SaveAs("SampleHouse_withPoint.ifc");
            }
        }     
    }
}
