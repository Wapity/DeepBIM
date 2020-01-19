using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Architecture;
using Autodesk.Revit.UI;
using Autodesk.Revit.UI.Selection;
using Autodesk.Revit.ApplicationServices;

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
            //string repoDirectory = @"C:\UserData\z0044dcu\Documents\GitHub\private\DeepBIM";
            string repoDirectory = @"C:\Users\gunther\dev\DeepBIM";


            UIApplication uiapp = commandData.Application;
            Application app = uiapp.Application;
            UIDocument uiDoc = commandData.Application.ActiveUIDocument;




            try
            {
                string dataDirectory = repoDirectory + @"\Data";
                string[] dataFiles =
                    Directory.GetFiles(dataDirectory, "*.txt", SearchOption.AllDirectories);
                System.IO.StreamWriter failLogFile =
                            new System.IO.StreamWriter(@"C:\Users\gunther\dev\DeepBIM\Data\failing.txt", false);
                System.IO.StreamWriter successLogFile =
                            new System.IO.StreamWriter(@"C:\Users\gunther\dev\DeepBIM\Data\success.txt", false);
                foreach (string dataFile in dataFiles)
                {
                    //Document doc = app.NewProjectDocument(UnitSystem.Metric);
                    // This template is needed to have the families for windows, doors available
                    // CHANGE PATH
                    Document doc = app.NewProjectDocument("C:\\ProgramData\\Autodesk\\RVT 2019\\Templates\\Generic\\Default_M_ENU.rte");

                    List<List<double>> walls;
                    List<List<double>> doors;
                    List<List<double>> windows;

                    readTxtFile(dataFile, out walls, out doors, out windows);
                    // connect dead ends of walls to nearest wall endpoint
                    connectUnconnectedWalls(walls);
                    // separate walls, if they intersect into nonintersecting parts
                    walls = separateWalls(walls);

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

                    string prompt0 = "Total Walls Count: " + WallList.Count;
                    //TaskDialog.Show("Revit", prompt0);


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

                    string prompt = $"Going to start creating roof for file {dataFile}";
                    //TaskDialog.Show("Revit", prompt);


                    //Create the Roof
                    // Remove try/catch if you want to see the error message in revit
                    try
                    {
                        RoofCreation(doc,
                                      WallList, level, commandData);
                        successLogFile.WriteLine(dataFile);
                        successLogFile.Flush();
                    }
                    catch
                    {
                        failLogFile.WriteLine(dataFile);
                        failLogFile.Flush();
                        //TaskDialog.Show("Revit", "Failed Roof creation");
                    }



                    // Finishing up and saving changes
                    SaveAsOptions overwrite = new SaveAsOptions();
                    overwrite.OverwriteExistingFile = true;
                    doc.SaveAs(dataFile + ".rvt", overwrite);
                    doc.Close(false);
                }
                failLogFile.Close();
                successLogFile.Close();
                //TaskDialog.Show("Revit", "Success!"); ;
                return Result.Succeeded;
            }

            catch (Exception e)
            {
                // this shows the whole error message in Revit
                // throw (e);
                
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
                                 List<Wall> WallList, Level level, ExternalCommandData commandData)
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

            
            string prompt1 = "level2 Name: " + level2.Name;
            //TaskDialog.Show("Revit", prompt1);



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
            List<ElementId> ExteriorWalls;
            //ExteriorWalls = GetAllExteriorWalls(doc, level);
            ExteriorWalls = GetOuterWallByRoom( commandData, doc, level);

            string prompt = "Exterior Walls Count: "+ ExteriorWalls.Count;
            //TaskDialog.Show("Revit", prompt);


            // Go through the outer walls
            if (ExteriorWalls.Count != 0)
            {
                foreach(ElementId id in ExteriorWalls)
                {
                    Element element = doc.GetElement(id);
                    Wall wall = element as Wall;

                    if (wall != null)
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
            var newDoubleList = doubleList.Select(x => Math.Round(x / 3.048)).ToList();
            //Add the converted list to the doors list of doubles
            list.Add(newDoubleList);
        }

        // geometry helper functions
        static double dist(List<double> p, List<double> q)
        {
            return Math.Sqrt(Math.Pow(p[0] - q[0], 2) + Math.Pow(p[1] - q[1], 2));
        }
        static bool btw(double x, double a, double b)
        {
            bool a_b = a <= b && a <= x && x <= b;
            bool b_a = b <= a && b <= x && x <= a;
            return (a_b || b_a);
        }
        static bool onSegment(double px, double py, double ax, double ay, double bx, double by)
        {
            return (btw(px, ax, bx) && btw(py, ay, by));
        }
        static List<double> intersect(List<double> wall1, List<double> wall2)
        {
            // a-b and c-d parrallel
            if ((wall1[3] - wall1[1]) * (wall2[2] - wall2[0]) == (wall1[2] - wall1[0]) * (wall2[3] - wall2[1]))
            {
                List<double> noIntersection = new List<double>();
                return noIntersection;
            }
            double px_numerator = (wall1[2] - wall1[0]) * (wall2[0] * wall2[3] - wall2[2] * wall2[1]) -
              (wall2[2] - wall2[0]) * (wall1[0] * wall1[3] - wall1[2] * wall1[1]);
            double px_denom = (wall1[2] - wall1[0]) * (wall2[3] - wall2[1]) - (wall1[3] - wall1[1]) * (wall2[2] - wall2[0]);
            double px = px_numerator / px_denom;

            double py_numerator = (wall1[3] - wall1[1]) * (wall2[0] * wall2[3] - wall2[2] * wall2[1]) - (wall2[3] - wall2[1]) * (wall1[0] * wall1[3] - wall1[2] * wall1[1]);
            double py_denom = px_denom;
            double py = py_numerator / py_denom;

            if (!onSegment(px, py, wall1[0], wall1[1], wall1[2], wall1[3]) ||
                !onSegment(px, py, wall2[0], wall2[1], wall2[2], wall2[3]))
            {
                List<double> noIntersection = new List<double>();
                return noIntersection;
            }
            return new List<double> { px, py };
        }
        static List<List<double>> separateWalls(List<List<double>> walls)
        {
            // track all intersections for every wall
            List<List<List<double>>> intersections = new List<List<List<double>>>();
            for(int i = 0; i < walls.Count; i++)
            {
                intersections.Add(new List<List<double>>());
            }
            for(int i = 0; i < walls.Count; i++)
            {
                List<double> wall1 = walls[i];
                for(int j = i+1; j < walls.Count; j++)
                {
                    List<double> wall2 = walls[j];
                    List<double> intersection = intersect(wall1, wall2);
                    if(intersection.Count > 0)
                    {
                        List<double> copy = intersection.ToList();
                        intersections[i].Add(intersection);
                        intersections[j].Add(copy);
                    }
                }
            }

            // new list of separated / intersection free walls
            List<List<double>> separated = new List<List<double>>();
            // separate every wall i at every intersections[i]
            for(int i = 0; i < walls.Count; i++)
            {
                List<double> wall = walls[i];
                List<double> wallStart = wall.GetRange(0, 2);
                List<List<double>> wallIntersections = intersections[i];
                wallIntersections.Sort((p, q) =>
                    (int)Math.Round(dist(p, wallStart) - dist(q, wallStart), MidpointRounding.AwayFromZero));
                wallIntersections.Prepend(wallStart);
                wallIntersections.Add(wall.GetRange(2, 2));
                for (int j = 0; j < wallIntersections.Count - 1; j += 1)
                {
                    List<double> start = wallIntersections[j];
                    List<double> end = wallIntersections[j+1];
                    if(dist(start, end) > 0.00001)
                    {
                        start.AddRange(end);
                        Console.WriteLine($"{start[0]}, {start[1]}, {start[2]}, {start[3]}");
                        separated.Add(start);
                    }
                }
            }
            return separated;
        }

        static void connectUnconnectedWalls(List<List<double>> walls)
        {
            for(int i = 0; i < walls.Count; i++)
            {
                List<bool> connected = new List<bool> { false, false };
                for(int j = 0; j < walls.Count; j++)
                {
                    if(i != j)
                    {
                        for(int k = 0; k <= 1; k++)
                        {
                            for(int l = 0; l <= 1; l++)
                            {
                                if(dist(walls[i].GetRange(2*k,2), walls[j].GetRange(2*l,2)) == 0)
                                {
                                    connected[k] = true;
                                }
                            }
                        }
                    }
                    if (connected[0] && connected[1])
                    {
                        break;
                    }
                }
                if(!connected[0])
                {
                    List<double> nearest = getNearest(walls, i, 0);
                    walls[i][0] = nearest[0];
                    walls[i][1] = nearest[1];
                }
                if(!connected[1])
                {
                    List<double> nearest = getNearest(walls, i, 1);
                    walls[i][2] = nearest[0];
                    walls[i][3] = nearest[1];
                }
            }
        }
        static List<double> getNearest(List<List<double>> walls, int wallIndex, int wallPoint)
        {
            double min = Double.PositiveInfinity;
            List<double> p = walls[wallIndex].GetRange(2 * wallPoint, 2);
            int nearestWallIndex = -1;
            int nearestWallPoint = -1;
            for(int i = 0; i < walls.Count; i++)
            {
                if(i != wallIndex)
                {
                    List<double> wall = walls[i];
                    for(int k = 0; k <= 1; k++)
                    {
                        double d = dist(p, wall.GetRange(2 * k, 2));
                        if(d < min)
                        {
                            min = d;
                            nearestWallIndex = i;
                            nearestWallPoint = k;
                        }
                    }
                }
            }
            if(nearestWallIndex == -1)
            {
                return null;
            }
            return walls[nearestWallIndex].GetRange(2 * nearestWallPoint, 2);
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
            walls = collector.Cast<Wall>().ToList();
            return walls;
        }

        // Adding code to Search for exterior walls
        private List<ElementId> GetOuterWallByRoom(ExternalCommandData commandData, Document doc, Level level1)
        {
           // this.commandData = commandData;
            UIDocument uiDoc = commandData.Application.ActiveUIDocument;
            Autodesk.Revit.ApplicationServices.Application app = commandData.Application.Application;

            //this.doc = uiDoc.Document;
            //Selection sel = uiDoc.Selection;

            double offset = 1000 / 304.8;

            List<Wall> wallList = new FilteredElementCollector(doc).OfClass(typeof(Wall)).Cast<Wall>().ToList();
            double maxX = -1D;
            double minX = -1D;
            double maxY = -1D;
            double minY = -1D;
            wallList.ForEach((wall) =>
            {
                Curve curve = (wall.Location as LocationCurve).Curve;
                XYZ xyz1 = curve.GetEndPoint(0);
                XYZ xyz2 = curve.GetEndPoint(1);

                double _minX = Math.Min(xyz1.X, xyz2.X);
                double _maxX = Math.Max(xyz1.X, xyz2.X);
                double _minY = Math.Min(xyz1.Y, xyz2.Y);
                double _maxY = Math.Max(xyz1.Y, xyz2.Y);

                if (curve.IsCyclic)
                {
                    Arc arc = curve as Arc;
                    double _radius = arc.Radius;
                 
                    _maxX += _radius;
                    _minX -= _radius;
                    _maxY += _radius;
                    _minY += _radius;
                }

                if (minX == -1) minX = _minX;
                if (maxX == -1) maxX = _maxX;
                if (maxY == -1) maxY = _maxY;
                if (minY == -1) minY = _minY;

                if (_minX < minX) minX = _minX;
                if (_maxX > maxX) maxX = _maxX;
                if (_maxY > maxY) maxY = _maxY;
                if (_minY < minY) minY = _minY;
            });
            minX -= offset;
            maxX += offset;
            minY -= offset;
            maxY += offset;

            CurveArray curves = new CurveArray();
            Line line1 = Line.CreateBound(new XYZ(minX, maxY, 0), new XYZ(maxX, maxY, 0));
            Line line2 = Line.CreateBound(new XYZ(maxX, maxY, 0), new XYZ(maxX, minY, 0));
            Line line3 = Line.CreateBound(new XYZ(maxX, minY, 0), new XYZ(minX, minY, 0));
            Line line4 = Line.CreateBound(new XYZ(minX, minY, 0), new XYZ(minX, maxY, 0));
            curves.Append(line1); curves.Append(line2); curves.Append(line3); curves.Append(line4);
            Transaction transaction = new Transaction(doc, "createNewRoomBoundaryLines");
            transaction.Start();
            //View view = uiDoc.ActiveView;
            var arbitaryFloorPlan = new FilteredElementCollector(doc).OfClass(typeof(ViewPlan)).Cast<ViewPlan>().Where(x => !x.IsTemplate).FirstOrDefault();
            View view = arbitaryFloorPlan;


            string prompt = "View Name: " + view.Name;
            //TaskDialog.Show("Revit", prompt);

            SketchPlane sketchPlane = SketchPlane.Create(doc, level1.Id);

            ModelCurveArray modelCaRoomBoundaryLines = doc.Create.NewRoomBoundaryLines(sketchPlane, curves, view);

            Room newRoom = null;
            RoomTag tag1 = null;
            if (true)
            {
        
                XYZ point = new XYZ(minX + 600 / 304.8, maxY - 600 / 304.8, 0);

               
                newRoom = doc.Create.NewRoom(view.GenLevel, new UV(point.X, point.Y));

                if (newRoom == null)
                {
                    string msg = "Error Message, New Room is null";
                    //TaskDialog.Show("xx", msg);
                    transaction.RollBack();
                    return null;
                }
                tag1 = doc.Create.NewRoomTag(new LinkElementId(newRoom.Id), new UV(point.X, point.Y), view.Id);
            }
            transaction.Commit();

            
            List<ElementId> elemengIds = DetermineAdjacentElementLengthsAndWallAreas(newRoom, doc);

            
            transaction = new Transaction(doc, "deleteX");
            transaction.Start();
            doc.Delete(tag1.Id);
            doc.Delete(newRoom.Id);
            foreach (ModelCurve item in modelCaRoomBoundaryLines)
            {
                doc.Delete(item.Id);
            }
            transaction.Commit();
      

            //sel.SetElementIds(elemengIds);
            return elemengIds;
        }



        List<ElementId> DetermineAdjacentElementLengthsAndWallAreas(Room room, Document doc)
        {
            List<ElementId> elementIds = new List<ElementId>();

            IList<IList<BoundarySegment>> boundaries
              = room.GetBoundarySegments(new SpatialElementBoundaryOptions());

            int n = boundaries.Count;//.Size;

            //Debug.Print(
            //  "{0} has {1} boundar{2}{3}",
            //  Util.ElementDescription(room),
            //  n, Util.PluralSuffixY(n),
            //  Util.DotOrColon(n));

            int iBoundary = 0, iSegment;

            foreach (IList<BoundarySegment> b in boundaries)
            {
                ++iBoundary;
                iSegment = 0;
                foreach (BoundarySegment s in b)
                {
                    ++iSegment;
                    //Element neighbour = s.Element;
                    Element neighbour = doc.GetElement(s.ElementId);// s.Element;
                    Curve curve = s.GetCurve();//.Curve;
                    double length = curve.Length;

                    //Debug.Print(
                    //  "  Neighbour {0}:{1} {2} has {3}"
                    //  + " feet adjacent to room.",
                    //  iBoundary, iSegment,
                    //  Util.ElementDescription(neighbour),
                    //  Util.RealString(length));

                    if (neighbour is Wall)
                    {
                        Wall wall = neighbour as Wall;

                        Parameter p = wall.get_Parameter(
                          BuiltInParameter.HOST_AREA_COMPUTED);

                        double area = p.AsDouble();

                        LocationCurve lc
                          = wall.Location as LocationCurve;

                        double wallLength = lc.Curve.Length;

                        //string promptm = "iSegment: " + iSegment +"\n This Wall has total length: " + wallLength + "\n Wall Id: " + wall.Id;
                        //TaskDialog.Show("Revit", promptm);


                        //Debug.Print(
                        //  "    This wall has a total length"
                        //  + " and area of {0} feet and {1}"
                        //  + " square feet.",
                        //  Util.RealString(wallLength),
                        //  Util.RealString(area));

                        elementIds.Add(wall.Id);
                    }
                }
            }
            //elementIds.RemoveAt(1);
            return elementIds;
        }
        // Added code ends here

    }
}
