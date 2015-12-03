import arcpy

arcpy.env.overwriteOutput = True

# Local variables:
cico_owner = "Database Connections\\cico_owner.sde"
cico_sde = "Database Connections\\cico_sde.sde"
CICO_R_P = "C:\\Users\\gisadmin\\Documents\\CICO_R&P"

#Block new connections to the database
print 'Blocking new connections to the database...'
arcpy.AcceptConnections(cico_sde, False)

# Disconnect users
print 'Disconnecting users...'
arcpy.DisconnectUser(cico_sde, 'ALL')

#Allow the database to begin accepting connections again
print 'Allowing the database to begin accepting connections again...'
arcpy.AcceptConnections(cico_sde, True)
