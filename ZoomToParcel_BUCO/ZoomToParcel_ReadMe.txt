Contents: This project contains files for a toolbox, a Python script and this readme document. The toolbox includes a model and a script tool.

Purpose: This tool will take a user-defined parcel number and zoom to the parcel inside an open ArcMap session.

Directions: Inside ArcMap, make sure your parcel data is labelled "Parcel_Data" or see below for customization directions. In the ArcCatalog window, locate and 
then open the toolbox called "ZoomToParcelToolbox" and then double-click the model called "Select_Parcel". Customize the selection expression to fit your data, then click ok.


Customization Directions: Right now, the script "StopProcess.py" is hard-coded to look for a parcel layer in the ArcMap Table of Contents called "Parcel_Data". 
If your parcel layer is not name this, please either change the name in the table of contents or edit line 9 of the script to look for the name of your parcel layer.

For additional customization, please edit the Select By Attributes tool parameters inside the model to match your parcel data.

Credits: This tool was originally put together by Courtney Worrell with Butler County, Kansas
Certain aspects were tweaked by Kristen Jordan-Koenig with the Kansas Data Access and Support Center