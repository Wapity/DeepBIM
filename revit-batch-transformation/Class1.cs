using System;
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.ApplicationServices;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using System.Diagnostics;
using System.IO;

namespace RevitBatch
{
    [Transaction(TransactionMode.Manual)]
    [Regeneration(RegenerationOption.Manual)]
    public class Class1 : IExternalCommand
    {
        public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
        {
            string homeDirectory = Environment.GetEnvironmentVariable("HOMEPATH");
            // CHANGE PATH
            string repoDirectory = @"C:\UserData\z0044dcu\Documents\GitHub\private\DeepBIM";

            UIApplication uiapp = commandData.Application;
            Application app = uiapp.Application;
            try
            {
                string dataDirectory = repoDirectory + @"\Data";
                string[] dataFiles =
                    Directory.GetFiles(dataDirectory, "*.txt", SearchOption.AllDirectories);
                foreach (string dataFile in dataFiles)
                {
                    //Document doc = app.NewProjectDocument(UnitSystem.Metric);
                    // This template is needed to have the families for windows, doors available
                    // CHANGE PATH
                    Document doc = app.NewProjectDocument("C:\\ProgramData\\Autodesk\\RVT 2019\\Templates\\Generic\\Default_M_ENU.rte");
                    /*
                    Transaction t = new Transaction(doc);
                    t.Start("Add Level");
                    Level level = Level.Create(doc, 0);
                    t.Commit();
                    */
                    List<List<double>> walls;
                    List<List<double>> doors;
                    List<List<double>> windows;

                    readTxtFile(dataFile, out walls, out doors, out windows);


                    //If you want to change the level where the object will be created, just chance the next variable.
                    string levelName = "Level 1";
                    // LINQ to find the level by its name.
                    Level level = (from lvl in new FilteredElementCollector(doc).
                                   OfClass(typeof(Level)).
                                   Cast<Level>()
                                   where (lvl.Name == levelName)
                                   select lvl).First();
                    //Wall Creation

                    foreach (List<double> wallData in walls)
                    {
                        // WallCreation.CreateWall(x1, y1, x2, y2);
                        this.WallCreation(doc, level,
                                          wallData[0], wallData[1], wallData[2], wallData[3]);
                    }


                    //Get all the walls from the model in the specified level
                    List<Wall> WallList = GetAllWallsInLevel(doc, level);


                    //Specify the family of the doors
                    string fsFamilyNameDoor = "M_Single-Flush";
                    string fsNameDoor = "0915 x 2134mm";

                    //Specify the family of the Windos
                    string fsFamilyNameWindow = "M_Fixed";
                    string fsNameWindow = "0915 x 0610mm";


                    //Create the doors
                    foreach (List<double> doorData in doors)
                    {
                        this.CreateElement(doc, fsFamilyNameDoor, fsNameDoor,
                                           WallList, level,
                                           doorData[0], doorData[1], doorData[2], doorData[3]);
                    }

                    //Create the windows
                    foreach (List<double> windowData in windows)
                    {
                        this.CreateElement(doc, fsFamilyNameWindow, fsNameWindow,
                                          WallList, level,
                                          windowData[0], windowData[1], windowData[2], windowData[3]);
                    }

                    string prompt = "Going to start creating roof";
                    TaskDialog.Show("Revit", prompt);
               

                    //Create the Roof
                    RoofCreation(doc,
                                  WallList, level);



                    // Finishing up and saving changes
                    doc.SaveAs(dataFile + ".rvt");
                    doc.Close(false);
                }
                TaskDialog.Show("Revit", "Success!"); ;
                return Result.Succeeded;
            }

            catch (Exception e)
            {
                // this shows the whole error message in Revit
                //throw (e);
                
                string prompt = e.Message + "\n" + e.StackTrace;
				TaskDialog.Show("Revit", prompt);
                return Result.Failed;	
                
            }
        }

        public void WallCreation(Document doc, Level level,
                                 double x1, double y1, double x2, double y2)
        {

            using (Transaction trans = new Transaction(doc))
            {
                FailureHandlingOptions failureHandlingOptions
                  = trans.GetFailureHandlingOptions();

                FailureHandler failureHandler
                  = new FailureHandler();

                failureHandlingOptions.SetFailuresPreprocessor(failureHandler);
                failureHandlingOptions.SetClearAfterRollback(true);

                trans.SetFailureHandlingOptions(failureHandlingOptions);
                trans.Start("WallDataParser");

                XYZ start = new XYZ(x1, y1, 0.0);
                XYZ end = new XYZ(x2, y2, 0.0);
                Line wallLine = Line.CreateBound(start, end);
                Wall wall = Wall.Create(doc, wallLine as Line, level.Id, true);

                trans.Commit();
            }
        }

        public void CreateElement(Document doc, string fsFamilyName, string fsName,
                                  List<Wall> WallList, Level level,
                                  double x1, double y1, double x2, double y2)
        {

            XYZ elementPoint = new XYZ((x2 + x1) / 2, (y2 + y1) / 2, level.Elevation);


            // LINQ to find the window's FamilySymbol by its type name.
            FamilySymbol familySymbol = (from fs in new FilteredElementCollector(doc).
                                         OfClass(typeof(FamilySymbol)).
                                         Cast<FamilySymbol>()
                                         where (fs.Family.Name == fsFamilyName && fs.Name == fsName)
                                         select fs).First();


            //Find the hosting Wall (nearst wall to the insertion point)

            Wall hostingWall = FindHostingWall(WallList, elementPoint);


            // Create Element.
            using (Transaction trans = new Transaction(doc, "Create Element"))

            {

                FailureHandlingOptions failureHandlingOptions
                  = trans.GetFailureHandlingOptions();

                FailureHandler failureHandler
                  = new FailureHandler();

                failureHandlingOptions.SetFailuresPreprocessor(failureHandler);
                failureHandlingOptions.SetClearAfterRollback(true);

                trans.SetFailureHandlingOptions(failureHandlingOptions);
                trans.Start();

                if (!familySymbol.IsActive)
                {
                    // Ensure the family symbol is activated.
                    familySymbol.Activate();
                    doc.Regenerate();
                }

                // Create Element
                FamilyInstance element = doc.Create.NewFamilyInstance(elementPoint, familySymbol, hostingWall,
                                                                      Autodesk.Revit.DB.Structure.StructuralType.NonStructural);
                trans.Commit();
            }

            //string prompt = "The element was created!";
            //TaskDialog.Show("Revit", prompt);
        }

        public void RoofCreation(Document doc,
                                 List<Wall> WallList, Level level)
        {
            // Get Level for roof, in our case level 2 is roof
            string levelName = "Level 2";
            // LINQ to find the level by its name.

            Level level2
             = new FilteredElementCollector(doc)
            .OfClass(typeof(Level))
             .Where<Element>(e =>
             !string.IsNullOrEmpty(e.Name)
             && e.Name.Equals(levelName))
            .FirstOrDefault<Element>() as Level;

            // Select roof type
            RoofType roofType
            = new FilteredElementCollector(doc)
            .OfClass(typeof(RoofType))
            .FirstOrDefault<Element>() as RoofType;

            // Get the handle of the application
            Application application = doc.Application;

            // Define the footprint for the roof based on our future selection (exterior walls)
            CurveArray footprint = application.Create
              .NewCurveArray();


            // Get Outermost walls
            List<Wall> ExteriorWalls;
            ExteriorWalls = GetAllExteriorWalls(doc, level);

            string prompt = "Exterior Walls Count: "+ ExteriorWalls.Count;
            TaskDialog.Show("Revit", prompt);


            // Go through the outer walls
            if (ExteriorWalls.Count != 0)
            {
                foreach(Wall wall in ExteriorWalls)
                {
                    if(wall != null)
                    {
                        LocationCurve wallCurve = wall.Location as LocationCurve;
                        footprint.Append(wallCurve.Curve);
                        continue;
                    }
                }
            }
            else
            {
                throw new Exception(
                "Please select a curve loop, wall loop or "
                + "combination of walls and curves to "
                + "create a footprint roof.");
            }

            //Do the mapping
            ModelCurveArray footPrintToModelCurveMapping
             = new ModelCurveArray();

            // Create Element Roof
            using (Transaction trans = new Transaction(doc, "Create Roof"))

            {

                FailureHandlingOptions failureHandlingOptions
                  = trans.GetFailureHandlingOptions();

                FailureHandler failureHandler
                  = new FailureHandler();

                failureHandlingOptions.SetFailuresPreprocessor(failureHandler);
                failureHandlingOptions.SetClearAfterRollback(true);

                trans.SetFailureHandlingOptions(failureHandlingOptions);
                trans.Start();

                // Create Roof
                FootPrintRoof footprintRoof
              = doc.Create.NewFootPrintRoof(
                footprint, level2, roofType,
                out footPrintToModelCurveMapping);

                ModelCurveArrayIterator iterator
                  = footPrintToModelCurveMapping.ForwardIterator();

                iterator.Reset();
                while (iterator.MoveNext())
                {
                    ModelCurve modelCurve = iterator.Current as ModelCurve;
                    footprintRoof.set_DefinesSlope(modelCurve, true);
                    footprintRoof.set_SlopeAngle(modelCurve, 0.5);
                }

                trans.Commit();
            }

            


        }

            #region HelpFuncitons
            public List<Wall> GetAllWallsInLevel(Document doc, Level level)
        {
            FilteredElementCollector collector = new FilteredElementCollector(doc);
            collector.OfClass(typeof(Wall));

            List<Wall> walls = new List<Wall>();
            walls = collector.Cast<Wall>().Where(wl => wl.LevelId == level.Id).ToList();
            return walls;
        }

        public Wall FindHostingWall(List<Wall> walls, XYZ elementPoint)
        {

            Wall wall = null;

            double distance = double.MaxValue;

            foreach (var w in walls)
            {
                double proximity = (w.Location as LocationCurve).Curve.Distance(elementPoint);

                if (proximity < distance)
                {
                    distance = proximity;
                    wall = w;
                }
            }

            return wall;
        }
        #endregion

        public static void readTxtFile(string pathToTxtFile,
                                       out List<List<double>> walls,
                                       out List<List<double>> doors,
                                       out List<List<double>> windows)
        {

            walls = new List<List<double>>();
            doors = new List<List<double>>();
            windows = new List<List<double>>();

            string line;
            try
            {
                //Pass the file path and file name to the StreamReader constructor
                StreamReader sr = new StreamReader(pathToTxtFile);

                //Read the first line of text
                line = sr.ReadLine();

                //Continue to read until you reach end of file
                while (line != null)
                {
                    //write the line to console window
                    Console.WriteLine(line);

                    // Splite the line with the \t separator and converted into a list of strings
                    List<string> dividedLine = line.Split('\t').ToList();
                    //List<string> dividedLine = line.Split('\t').Select(string.Parse).ToList();
                    if (dividedLine[4] == "door")
                    {
                        insertNewData(ref doors, dividedLine);
                    }
                    else if (dividedLine[4] == "wall")
                    {
                        insertNewData(ref walls, dividedLine);
                    }
                    else if (dividedLine[4] == "window")
                    {
                        insertNewData(ref windows, dividedLine);
                    }

                    //Read the next line
                    line = sr.ReadLine();
                }
                //close the file
                sr.Close();
            }
            catch (Exception e)
            {
                Console.WriteLine("Exception: " + e.Message);
            }
            finally
            {
                Console.WriteLine("Executing finally block.");
            }
        }

        static void insertNewData(ref List<List<double>> list, List<string> data)
        {
            //Remove the last four entries of the list
            data.RemoveRange(data.Count - 4, 4);
            //Convert the string list into double list
            List<double> doubleList = data.Select(x => double.Parse(x, System.Globalization.CultureInfo.InvariantCulture)).ToList();
            //Dividing every element by the unit convertion factor 
            //(1feet = 3.048 dm) (the coordinates in the text file are in dm 
            var newDoubleList = doubleList.Select(x => x / 3.048).ToList();
            //Add the converted list to the doors list of doubles
            list.Add(newDoubleList);
        }

        // Helper functions added by Haider:

        /// <summary>
        /// Wall type predicate for exterior wall function
        /// </summary>
        bool IsExterior(WallType wallType)
        {
            Parameter p = wallType.get_Parameter(
              BuiltInParameter.FUNCTION_PARAM);

            Debug.Assert(null != p, "expected wall type "
              + "to have wall function parameter");

            WallFunction f = (WallFunction)p.AsInteger();

            return WallFunction.Exterior == f;
        }

        List<Wall> GetAllExteriorWalls(
     Document doc, Level level)
        {
            FilteredElementCollector collector = new FilteredElementCollector(doc);
              collector.OfClass(typeof(Wall))
              .Cast<Wall>()
              .Where<Wall>(w =>
               IsExterior(w.WallType));

            List<Wall> walls = new List<Wall>();
            walls = collector.Cast<Wall>().Where(wl => wl.LevelId == level.Id).ToList();
            return walls;
        }

    }
}
