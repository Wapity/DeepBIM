using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using Xbim.Common;
using Xbim.Common.Step21;
using Xbim.Ifc;
using Xbim.IO;
using Xbim.Ifc4.ActorResource;
using Xbim.Ifc4.DateTimeResource;
using Xbim.Ifc4.ExternalReferenceResource;
using Xbim.Ifc4.PresentationOrganizationResource;
using Xbim.Ifc4.GeometricConstraintResource;
using Xbim.Ifc4.GeometricModelResource;
using Xbim.Ifc4.GeometryResource;
using Xbim.Ifc4.Interfaces;
using Xbim.Ifc4.Kernel;
using Xbim.Ifc4.MaterialResource;
using Xbim.Ifc4.MeasureResource;
using Xbim.Ifc4.ProductExtension;
using Xbim.Ifc4.ProfileResource;
using Xbim.Ifc4.PropertyResource;
using Xbim.Ifc4.QuantityResource;
using Xbim.Ifc4.RepresentationResource;
using Xbim.Ifc4.SharedBldgElements;

namespace TxtToIFC
{
    class Program
    {
        static int Main()
        {
            List<List<double>> doors;
            List<List<double>> walls;

            ReadTxt.readTxtFile("..\\..\\..\\..\\03.SampleData\\002_sample_floor.txt", out doors, out walls);

            // To iterate over the components of the list doors.
            //foreach (List<int> subList in doors)
            //{
            //    foreach (int item in subList)
            //    {
            //        Console.WriteLine(item.ToString());
            //    }
            //}

            // return 0;
            List<List<double>> temWalls = new List<List<double>>();
            temWalls.Add(walls[0]);
            //temWalls.Add(new List<int>{ walls[0][0], walls[0][1], 443, walls[0][1] }); // temWall [1] has the same origin as wall 0
            temWalls.Add(walls[1]);
            temWalls.Add(walls[2]);
            //first create and initialise a model called Hello Wall
            Console.WriteLine("Initialising the IFC Project....");
            using (var model = ModelCreation.CreateandInitModel("HelloWall"))
            {
                if (model != null)
                {
                    IfcBuilding building = BuildingCreation.CreateBuilding(model, "Default Building");

                    //foreach (List<double> wallData in temWalls)
                    foreach (List<double> wallData in walls)
                    {
                        //double length = 2000;//sqrt((x2-x1)* (x2 - x1) + (y2 - y1)* (y2 - y1));
                        double width = 5;     //to be defined
                        double height = 100;   //to be defined
                        //CreateWall(IfcStore model, double length, double width, double height)
                        IfcWallStandardCase wall = WallCreation.CreateWall(model, wallData[0], wallData[1],
                            wallData[2], wallData[3], width, height);

                        //if (wall != null) WallCreation.AddPropertiesToWall(model, wall);


                        if (wall != null)
                        {
                            try
                            {
                                using (var txn = model.BeginTransaction("Add Wall"))
                                {
                                    building.AddElement(wall);
                                    txn.Commit();
                                }
                                Console.WriteLine("Standard Wall successfully created and added....");
                            }
                            catch (Exception e)
                            {
                                Console.WriteLine("Failed to create adn add the wall");
                                Console.WriteLine(e.Message);
                            }
                        }
                    }
                    try
                    {
                        //write the Ifc File
                        model.SaveAs("NewIfc4file.ifc", StorageType.Ifc);
                        Console.WriteLine("NewIfc4file.ifc has been successfully written");
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine("Failed to save HelloWall.ifc");
                        Console.WriteLine(e.Message);
                    }
                }
                else
                {
                    Console.WriteLine("Failed to initialise the model");
                }
            }
            Console.WriteLine("Press any key to exit to view the IFC file....");
            //Console.ReadKey();
            LaunchNotepadClass.LaunchNotepad("NewIfc4file.ifc");
            return 0;
        }


        // THE NEXT WAS WHAT I HAT BEFOR -> TO DELETE AFTERWARDS
        /*
        static void Main()
       {
           var credentials = new XbimEditorCredentials
           {
               ApplicationDevelopersName = "Miguel Arturo Vega Torres",
               ApplicationFullName = "Creation of IFC files from txt files",
               ApplicationIdentifier = "2019_09_01",
               ApplicationVersion = "1.0",
               EditorsFamilyName = "Team",
               EditorsGivenName = "Jimmy",
               EditorsOrganisationName = "TUM"
           };

           DateTime a = DateTime.Now;

           //Create an IFC file
           using (var model = IfcStore.Create(credentials, IfcSchemaVersion.Ifc4, XbimStoreType.InMemoryModel))
           {
               //...do something with the model
           Console.WriteLine("Last: DateTime.Now - a = " + (DateTime.Now - a));
               DateTime d = DateTime.Now;
               using (var txn = model.BeginTransaction("Create Wall"))
               {
                   DateTime b = DateTime.Now;
                   //the next two lines were gotten from: https://docs.xbim.net/examples/proper-wall-in-3d.html
                   var Point = model.Instances.New<IfcCartesianPoint>();
                   Point.SetXY(10, 11); //insert at arbitrary position
                   Console.WriteLine("Last: DateTime.Now - b = " + (DateTime.Now - b));
               }
               Console.WriteLine("Transaction time = " + (DateTime.Now - d));

               DateTime c = DateTime.Now;
               //save your changed model. IfcStore will use the extension to save it as *.ifc, *.ifczip or *.ifcxml.
               model.SaveAs("SampleHouse_withPoint.ifc");
               Console.WriteLine("Last: DateTime.Now - b = " + (DateTime.Now - c));
           }
           Console.WriteLine("Complite time: DateTime.Now - a = " + (DateTime.Now - a));
       }
       */

        
    }
}
