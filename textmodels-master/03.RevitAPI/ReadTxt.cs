using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace TestModule
{
    public class ReadTxt
    {
        //"C:\\Sample.txt"
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
        
    }
}
