This reads the 2D input files from the Data directory and transforms them into .rvt files in the same directory.

To set this up, follow https://knowledge.autodesk.com/support/revit-products/learn-explore/caas/simplecontent/content/lesson-1-the-basic-plug.html with the corresponding code/project files from this directory.

You also need to do:
Place the RevitBatch.addin file into C:\ProgramData\Autodesk\Revit\Addins\2019\ instead of their .addin file
Change the paths in Class1.cs to correspond to your machine (look for "CHANGE PATH" marks)
Unzip the the .zip file in the Data directory



TODO:
Automatically dismiss error messages
Add roofs/floors
Make paths system independent
[DONE]Make script read batch of 2D models instead of sample one
