#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kristen
#
# Created:     24/03/2015
# Copyright:   (c) kristen 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def counties_SearchCursor():
    from arcpy.da import SearchCursor
    #define feature class
    fc = r"\\elbert\c$\Kristen\Python\UserGroup\KS_Counties.shp"

    #identify fields for search cursor
    fields = ("County", "CO_ABBR", "STATECODE")

    #set up search cursor
    with SearchCursor(fc, fields) as rows:
        #loop through rows
        for row in rows:
            #print field information
            print row[0], row[1], row[2]

def counties_InsertCursor():
    from arcpy.da import InsertCursor, SearchCursor
    from arcpy import CreateFeatureclass_management, AddField_management, Describe, Exists, Delete_management
    from os.path import join

    root = r"\\elbert\c$\Kristen\Python\UserGroup"

    #define feature classes
    fc = join(root, "KS_Counties.shp")
    newfc = "KS_Counties_new.shp"
    newfcFull = join(root, newfc)

    #see if newfc already exists
    if Exists(newfc):
        Delete_management(newfc)
        print "Deleted KS_Counties_new.shp"

    #identify fields for search cursor
    fields = ("County", "CO_ABBR", "STATECODE", "SHAPE@")

    #set up where clause
    where_clause = "County like 'C%'"

    #identify spatial reference of original feature class
    sr = Describe(fc).spatialReference

    #create feature class & add fields
    CreateFeatureclass_management(root, newfc, "POLYGON", "", "", "", sr)
    AddField_management(newfcFull, "County_KS","TEXT", "","", 30)
    AddField_management(newfcFull, "CO_ABBR", "TEXT", "","", 2)
    AddField_management(newfcFull, "PVDCode", "TEXT", "", "", 3)

    #identify fields for insert cursor
    new_fields = ("County_KS", "CO_ABBR", "PVDCode", "SHAPE@")

    #set up search cursor on counties using a where clause
    with SearchCursor(fc, fields, where_clause) as rows:
        for row in rows:
            #create insert cursor
            i_cursor = InsertCursor(newfcFull, new_fields)

            #input the row from the search cursor
            i_cursor.insertRow(row)

            #delete the insert cursor object so it can be recreated
            del i_cursor

def counties_UpdateCursor():
    from arcpy.da import UpdateCursor

    #define feature class
    fc = r"\\elbert\c$\Kristen\Python\UserGroup\KS_Counties_new.shp"

    #define fields to work with
    fields = ("County_KS", "CO_ABBR")

    with UpdateCursor(fc, fields) as rows:
        for row in rows:
            #get existing name & abbreviation
            name = row[0]
            co_abbr = row[1]

            #create new name & abbreviation
            name_new = name.replace("C", "X")
            co_abbr_new = co_abbr.replace("C", "X")

            #set new values
            row[0] = name_new
            row[1] = co_abbr_new

            #officially update the row
            rows.updateRow(row)


def main():
##    counties_SearchCursor()
#    counties_InsertCursor()
    counties_UpdateCursor()


if __name__ == '__main__':
    main()
