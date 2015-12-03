#-------------------------------------------------------------------------------
# Name:        StopProcess
# Purpose:     Zooms to a selected process. To be used together with a "Select_Parcel" model that accepts user criteria.
#
# Author:      Courtney Worrell with Butler County, Kansas with tweaks by Kristen Jordan-Koenig with the Kansas Data Access and Support Center
#
# Created:     November 2015
#-------------------------------------------------------------------------------

# Process: Zoom to Parcel if selected
import arcpy
mxd = arcpy.mapping.MapDocument('CURRENT')
df = arcpy.mapping.ListDataFrames(mxd, "Layers") [0]
Layer = (mxd, "Parcel_Data", df)[0]

#see if any parcels are selected
count = 0

#loop through the layers in the TOC
for lyr in arcpy.mapping.ListLayers(mxd):

    #find when the layer name matches your parcel layer name
    if str(lyr.name) == "Parcel_Data":
        #run a count on selected parcels
		result = arcpy.GetCount_management(lyr)
		count = int(result.getOutput(0))

#see if the count is higher than 0
if count > 0:

	try:
        #if the count is higher than 0, it means a parcel is selected, so zoom to it
		df.zoomToSelectedFeatures()
		arcpy.RefreshActiveView()

	except Exception as e:
        #adds message to geoprocessing screen
		arcpy.AddMessage("Parcel number is invalid")
		sys.exit()

else:
	arcpy.AddMessage("Parcel number is invalid")





