So far this only uses one sample 2D file, does the 3D transformation 10X to create 10 .rvt files with the 3D model in the users Document folder.

To set this up, follow https://knowledge.autodesk.com/support/revit-products/learn-explore/caas/simplecontent/content/lesson-1-the-basic-plug.html with the corresponding code/project files from this directory.

You also need to do:
Place the RevitBatch.addin file into C:\ProgramData\Autodesk\Revit\Addins\2019\ instead of their .addin file
Change the paths in Class1.cs to correspond to your machine (look for "CHANGE PATH" marks)



TODO:
Make paths system independent
Make script read batch of 2D models instead of sample one
Add roofs/floors
