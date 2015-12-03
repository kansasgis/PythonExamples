# ---------------------------------------------------------------------------
# 
# Created on: 2013-09-04 16:49:00.00000
#   Created by: Terrol Palmer
# Description: 
# ---------------------------------------------------------------------------

# Set the necessary product code




import arcpy

users = arcpy.ListUsers("Database Connections/cico_sde.sde")
for user in users:
    print("ClientName: {0}, Connected at: {1}".format(
        user.ID, user.ConnectionTime))
