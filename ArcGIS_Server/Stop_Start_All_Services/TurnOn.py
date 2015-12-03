print """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

*******   *******   *******   *******
*******   *******   *******   *******
**   **   **        **        **   **
**   **   **        **        **   **
**   **   **  ***   **        **   **
**   **   **   **   **        **   **
*******   *******   *******   *******
*******   *******   *******   *******

GIS Division
Information Technology
Douglas County, Kansas

TurnOn.py
Purpose: Resumes the cico_published database and then restarts all
web services.

Version history:
Created 2013-09-04 16:49:00 by Terrol Palmer
Modified 2014-08-27 by Amy Roust to add simple print statements.
Modified 2015-02-27 by Amy Roust to add comments, sleep timer,
and make minor cosmetic changes.
Modified 2015-06-09 by Amy Roust to replace resume command with
new AcceptConnections Python tool.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

# Acquire an available ArcInfo license
import arcinfo

# Import required Python libraries
import arcpy, subprocess
from time import sleep

# RESUMING CICO_PUBLISHED GEODATABASE
print 'Allowing connections to cico_published geodatabase...'
arcpy.AcceptConnections(r'Database Connections\cico_published_sde.sde', True)
print 'Successful.'

print '\nAllowing connections to DGCOPub geodatabase...'
arcpy.AcceptConnections(r'Database Connections\DGCOPub_sde.sde', True)
print 'Successful.'

print '\nAllowing connections to ExternalData geodatabase...'
arcpy.AcceptConnections(r'Database Connections\ExternalData_sde.sde', True)
print 'Successful.'
    

# STARTING WEB SERVICES
print "\nStarting web services..."
filepath5 = r'f:\GIS\Operations\ScheduledTasks\StartWebServices.bat'
p5 = subprocess.Popen(filepath5, shell = True, stdout = subprocess.PIPE)
stdout, stderr = p5.communicate()
result3 = p5.returncode
result4 = str(result3)
print '\tCompleted process. Return code will be 0 if successful: %s' % result4
del result3
del result4

print '\nAll processes complete. Window will close in 5 seconds.'

sleep(5)
