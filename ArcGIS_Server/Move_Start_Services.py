#-------------------------------------------------------------------------------
# Name:        DASC_MoveServices
# Purpose:     Republish ArcGIS Services on Linux
#
# Author:      kristen
#
# Created:     30/11/2015
#-------------------------------------------------------------------------------
from os.path import basename, join, dirname
from os import walk
from arcpy import ListFiles, env, StageService_server, UploadServiceDefinition_server, GetMessages
from arcpy.mapping import MapDocument, CreateMapSDDraft, AnalyzeForSD
from shutil import copy2

def publishService(mxdPath, unpublishedServices):
    #publish MXD's as services on linux cluster
    #http://server.arcgis.com/en/server/latest/administer/linux/example-publish-a-map-service-from-a-map-document-mxd-.htm
    #arcpy.mapping root help- http://resources.arcgis.com/EN/HELP/MAIN/10.1/index.html#//00s300000032000000
    mapDoc = MapDocument(mxdPath)

    # Provide path to connection file
    # To create this file, right-click a folder in the Catalog window and
    #  click New > ArcGIS Server Connection
    con = r'GIS Servers\Linux_DASC_Tin'
    wrkspc = dirname(mxdPath)

    # Provide other service details
    service = basename(mxdPath).split(".")[0]
    sddraft = join(wrkspc, service + '.sddraft')
    sd = join(wrkspc, service + '.sd')
    summary = mapDoc.description
    tags = mapDoc.tags

    # Create service definition draft
    CreateMapSDDraft(mapDoc, sddraft, service, 'ARCGIS_SERVER', con, True, "admin_boundaries", summary, tags)

    # Analyze the service definition draft
    analysis = AnalyzeForSD(sddraft)

    # Print errors, warnings, and messages returned from the analysis
    print "The following information was returned during analysis of the MXD:"
    for key in ('messages', 'warnings', 'errors'):
      print '----' + key.upper() + '---'
      vars = analysis[key]
      for ((message, code), layerlist) in vars.iteritems():
        print '    ', message, ' (CODE %i)' % code
        print '       applies to:',
        for layer in layerlist:
            print layer.name,
        print

    # Stage and upload the service if the sddraft analysis did not contain errors
    if analysis['errors'] == {}:
        # Execute StageService. This creates the service definition.
        StageService_server(sddraft, sd)

        # Execute UploadServiceDefinition. This uploads the service definition and publishes the service.
        try:
            UploadServiceDefinition_server(sd, con)
            print "Service successfully published"
        except:
            unpublishedServices.append(sd)
            print "HELP. I really need somebody. HELP."

    else:
        print "Service could not be published because errors were found during analysis."

    print GetMessages()

    return unpublishedServices


def main():

    #copy over MXD's in one folder to ricochet
    rootFolder = r"\\magnesium\d$\arcgisserver\mxd\admin_boundaries"
    targetFolder = r"\\ricochet\c$\BigDrives\webdata\webdata0\ArcGISServer_Projects\dasc_catalog\administrative_boundaries"

    #set workspace
    env.workspace = rootFolder

    unpublishedServices = []

    #loop through mxd's in workspace
    for mxd in ListFiles():
        #define paths
        fullCurrentPath = join(rootFolder, mxd)
        newTargetPath = join(targetFolder, mxd)

        #copy mxd
        copy2(fullCurrentPath, newTargetPath)

        #publish mxd as service
        unpublishedServices = publishService(newTargetPath, unpublishedServices)

    if unpublishedServices != []:
        con = r'GIS Servers\Linux_DASC_Tin'
        for us in unpublishedServices:
            try:
                UploadServiceDefinition_server(us, con)
                print "Service successfully published"
                unpublishedServices.remove(us)
            except:
                print us + "still won't publish"

        print unpublishedServices


if __name__ == '__main__':
    main()
