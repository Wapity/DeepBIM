/*
 * Created by Miguel Vega.
 * Email: miguel.vega@tum.de
 * Date: 25.09.2019
 */
using System;
using Autodesk.Revit.UI;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI.Selection;
using System.Collections.Generic;
using System.Linq;
using System.Diagnostics;

namespace TestModule
{
	[Autodesk.Revit.Attributes.Transaction(Autodesk.Revit.Attributes.TransactionMode.Manual)]
	[Autodesk.Revit.DB.Macros.AddInId("DC59D99E-EBA8-424B-9684-93383F037CA1")]
	public partial class ThisDocument
	{
		#region Main Function
		
		public void Main()
		{
			try
			{
				Document doc = this.Application.ActiveUIDocument.Document;
				
				List<List<double>> walls;
				List<List<double>> doors;
				List<List<double>> windows;

				ReadTxt.readTxtFile("C:\\Users\\Dell\\Desktop\\HIWI with Jimmy\\03.SampleData\\0003_sample_floor_with_Windows.txt",
				                    out walls, out doors, out windows);

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
				string fsNameDoor  = "0915 x 2134mm";
				
				//Specify the family of the Windos
				string fsFamilyNameWindow = "M_Window-Casement-Double";
				string fsNameWindow  = "850 x 900mm";
				
				
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
				
			}
			
			catch (Exception e)
			{
				string prompt = e.Message;
				TaskDialog.Show("Revit", prompt);;
				
			}
			string message = "Success!";
			TaskDialog.Show("Revit", message);;
			
		}
		#endregion
			
		#region Wall and Element creation
		
		public void WallCreation(Document doc, Level level,
		                         double x1,double y1,double x2,double y2)
		{
			
			using ( Transaction trans = new Transaction( doc ) )
			{
				trans.Start( "WallDataParser" );

				XYZ start = new XYZ( x1, y1, 0.0 );
				XYZ end = new XYZ( x2, y2, 0.0 );
				Line wallLine = Line.CreateBound( start, end );
				Wall wall = Wall.Create( doc, wallLine as Line, level.Id, true );
				
				trans.Commit();
			}
		}
		
	


		public void CreateElement(Document doc, string fsFamilyName, string fsName,
		                          List<Wall> WallList, Level level,
		                          double x1,double y1,double x2,double y2)
		{
			
			XYZ  elementPoint = new XYZ((x2 + x1)/2 , (y2 + y1)/2, level.Elevation);


			// LINQ to find the window's FamilySymbol by its type name.
			FamilySymbol familySymbol = (from fs in new FilteredElementCollector(doc).
			                             OfClass(typeof(FamilySymbol)).
			                             Cast<FamilySymbol>()
			                             where (fs.Family.Name == fsFamilyName && fs.Name == fsName)
			                             select fs).First();
			

			//Find the hosting Wall (nearst wall to the insertion point)

			Wall hostingWall = FindHostingWall(WallList, elementPoint);

			
			// Create Element.
			using (Transaction t = new Transaction(doc, "Create Element"))
				
			{
				t.Start();

				if (!familySymbol.IsActive)
				{
					// Ensure the family symbol is activated.
					familySymbol.Activate();
					doc.Regenerate();
				}

				// Create Element
				FamilyInstance element = doc.Create.NewFamilyInstance(elementPoint, familySymbol, hostingWall,
				                                                      Autodesk.Revit.DB.Structure.StructuralType.NonStructural);
				t.Commit();
			}
			
			//string prompt = "The element was created!";
			//TaskDialog.Show("Revit", prompt);
		}
		
		#endregion
		
		#region HelpFuncitons
		public List<Wall> GetAllWallsInLevel(Document doc, Level level)
		{
			FilteredElementCollector collector = new FilteredElementCollector(doc);
			collector.OfClass(typeof(Wall));
			
			List<Wall> walls = new List<Wall>();
			walls = collector.Cast<Wall>().Where(wl => wl.LevelId == level.Id).ToList();
			return walls;
		}
		
		public Wall FindHostingWall(List<Wall> walls , XYZ elementPoint)
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
		
		#region Revit Macros generated code
		
			private void Module_Startup(object sender, EventArgs e)
		{

		}

		private void Module_Shutdown(object sender, EventArgs e)
		{

		}

		
		private void InternalStartup()
		{
			this.Startup += new System.EventHandler(Module_Startup);
			this.Shutdown += new System.EventHandler(Module_Shutdown);
		}
		#endregion
			
	}
}