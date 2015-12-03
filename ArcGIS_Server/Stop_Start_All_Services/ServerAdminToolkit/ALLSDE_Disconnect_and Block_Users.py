import arcpy

arcpy.env.overwriteOutput = True

# Local variables:
cico_sde = "Database Connections\\cico_sde.sde"
cico_published_sde = "Database Connections\\cico_published_sde.sde"
orthos_sde = "Database Connections\\orthos_sde.sde" 
Production_sde = "Database Connections\\Production_sde.sde"
PublicWorks_sde = "Database Connections\\PublicWorks_sde.sde"
PublicWorks_published_sde = "Database Connections\\PublicWorks_published_sde.sde"

#Block new connections to the databases
print 'Blocking new connections to cico ...'
arcpy.AcceptConnections(cico_sde, False)

print 'Blocking new connections to cico_published...'
arcpy.AcceptConnections(cico_published_sde, False)

print 'Blocking new connections to orthos...'
arcpy.AcceptConnections(orthos_sde, False)

print 'Blocking new connections to Production...'
arcpy.AcceptConnections(Production_sde, False)

print 'Blocking new connections to PublicWorks...'
arcpy.AcceptConnections(PublicWorks_sde, False)

print 'Blocking new connections to PublicWorks_published...'
arcpy.AcceptConnections(PublicWorks_published_sde, False)

print 'All databases blocked from accepting new connections.'

# Disconnect users
print 'Disconnecting users from cico...'
arcpy.DisconnectUser(cico_sde, 'ALL')

print 'Disconnecting users from cico_published...'
arcpy.DisconnectUser(cico_published_sde, 'ALL')

print 'Disconnecting users from orthos...'
arcpy.DisconnectUser(orthos_sde, 'ALL')

print 'Disconnecting users from Production...'
arcpy.DisconnectUser(Production_sde, 'ALL')

print 'Disconnecting users from PublicWorks...'
arcpy.DisconnectUser(PublicWorks_sde, 'ALL')

print 'Disconnecting users from PublicWorks_published...'
arcpy.DisconnectUser(PublicWorks_published_sde, 'ALL')

print 'Users disconnected from all databases.'


#Allow the databases to begin accepting connections again
print 'Allowing the cico database to begin accepting connections again...'
arcpy.AcceptConnections(cico_sde, True)

print 'Allowing the cico_published database to begin accepting connections again...'
arcpy.AcceptConnections(cico_published_sde, True)

print 'Allowing the orthos database to begin accepting connections again...'
arcpy.AcceptConnections(orthos_sde, True)

print 'Allowing the Production database to begin accepting connections again...'
arcpy.AcceptConnections(Production_sde, True)

print 'Allowing the PublicWorks database to begin accepting connections again...'
arcpy.AcceptConnections(PublicWorks_sde, True)

print 'Allowing the PublicWorks_published database to begin accepting connections again...'
arcpy.AcceptConnections(PublicWorks_published_sde, True)

print 'All databases are now accepting new connections.'

