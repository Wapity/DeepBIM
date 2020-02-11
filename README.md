# DeepBIM

## Creation of 3D floorplans with roof and floors : 
 - Follow the setup and requirements in revit-batch-transformation, then run the Revit Addin to create all the Revit files
 - A Success file is created indicating the floorplans where roofs and floors have been added correctly
 
 ## Batch Analysis :
 - In EnergyReports, use Files.py to rename all the successul files (change local path)
 - Gather all these files with different names into one folder manually
 - For each file :
    - Open Revit 
    - Open Dynamo and load SetSpaces.dyn to automatically change above level and upper limit of spaces, let it run in         background
    - Place spaces automatically with the tool 
    - Run heating and cooling load (change the type of materials/profile of building and HVAC sytem used if wanted) 
    - Get the temporary htm file containing the report created at file:///C:/Users/"UserName"/AppData/Local/Temp and transfer it into a common folder
    - Close the report and floorplan
- Repeat for 400 files
- When the folder of html reports is complete, in EnergyReports, run parser_main.py to extract all the information (parameters and heating and cooling load) and write the dataset in bim_train.csv (change local path)

## Training the model and predicting new values :
 - RandomForest : run train_predict.py to train and test the model on the dataset, and predict new heating and cooling loads for new values put in data/bim_prediction.csv (for further use) 
   - Requirements : scikit-learn
 - KerasRegressor : run train.py to train and test the model for each load. The best models are then saved and can be loaded to predict new heating and cooling loads with predict.py , for new values put in data/bim_prediction.csv (for further use) 
   - Requirements : Tensorflow, Keras

    
    
 
