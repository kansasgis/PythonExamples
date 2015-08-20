#-------------------------------------------------------------------------------
# Name:        NG911_CreateAddressLocators
# Purpose:     Creates address locators from address points, road centerlines, and a composite locator
#
# Author:      Kristen Jordan-Koenig, kristen@kgs.ku.edu
#
# Created:     20/08/2015
#-------------------------------------------------------------------------------

from arcpy import AddMessage, CreateAddressLocator_geocoding, CreateCompositeAddressLocator_geocoding, Exists, env
from os.path import join

def userMessage(message):
    print message
    AddMessage(message)

def main():

    co_abbr = "" #countyabbreviation
    workspace = r"" #where the locators should live
    NG911_gdb = r"" #the NG911 database

    streetPath = join(NG911_gdb, "NG911", "RoadCenterline")
    roadAliasPath = join(NG911_gdb, "RoadAlias")
    addressPointPath = join(NG911_gdb, "NG911", "AddressPoints")

    env.workspace = workspace

    #set geocoding variables
    AL1 = join(workspace, co_abbr + "_AddressPoint_Loc") #address point locator
    AL2 = join(workspace, co_abbr + "_RoadCenterline_Loc") #road centerline locator
    AL3 = join(workspace, co_abbr + "_Composite_Loc") #composite locator

    if not Exists(AL1):
        #Create address locator from NG911 Address points AL1
        addyFieldMap = """'Feature ID' OBJECTID VISIBLE NONE;'*House Number' HNO VISIBLE NONE;Side <None> VISIBLE NONE;'Prefix Direction' PRD VISIBLE NONE;
            'Prefix Type' STP VISIBLE NONE;'*Street Name' RD VISIBLE NONE;'Suffix Type' STS VISIBLE NONE;'Suffix Direction' POD VISIBLE NONE;
            'City or Place' MUNI VISIBLE NONE;'ZIP Code' ZIP VISIBLE NONE;State STATE VISIBLE NONE;'Street ID' <None> VISIBLE NONE;'Display X' <None> VISIBLE NONE;
            'Display Y' <None> VISIBLE NONE;'Min X value for extent' <None> VISIBLE NONE;'Max X value for extent' <None> VISIBLE NONE;'Min Y value for extent' <None> VISIBLE NONE;
            'Max Y value for extent' <None> VISIBLE NONE;'Additional Field' <None> VISIBLE NONE;'Altname JoinID' <None> VISIBLE NONE"""

        userMessage("Creating locator from address points...")

        try:
            CreateAddressLocator_geocoding("US Address - Single House", addressPointPath + " 'Primary Table'", addyFieldMap, AL1, "", "DISABLED")
        except:
            try:
                CreateAddressLocator_geocoding("US Address - Single House", addressPointPath + " 'Primary Table'", addyFieldMap, AL1, "")
            except:
                userMessage("Could not create locator from address points.")

        #report on locator status and edit minimum match score down to 75
        if Exists(AL1):
            userMessage("Created locator from address points.")

    if not Exists(AL2):
        #Create address locator from NG911 Road centerline AL2
         #generate locator
        fieldMap = """'Primary Table:Feature ID' <None> VISIBLE NONE;'*Primary Table:From Left' RoadCenterline:L_F_ADD VISIBLE NONE;
            '*Primary Table:To Left' RoadCenterline:L_T_ADD VISIBLE NONE;'*Primary Table:From Right' RoadCenterline:R_F_ADD VISIBLE NONE;
            '*Primary Table:To Right' RoadCenterline:R_T_ADD VISIBLE NONE;'Primary Table:Prefix Direction' RoadCenterline:PRD VISIBLE NONE;
            'Primary Table:Prefix Type' RoadCenterline:STP VISIBLE NONE;'*Primary Table:Street Name' RoadCenterline:RD VISIBLE NONE;
            'Primary Table:Suffix Type' RoadCenterline:STS VISIBLE NONE;'Primary Table:Suffix Direction' RoadCenterline:POD VISIBLE NONE;
            'Primary Table:Left City or Place' RoadCenterline:MUNI_L VISIBLE NONE;
            'Primary Table:Right City or Place' RoadCenterline:MUNI_R VISIBLE NONE;
            'Primary Table:Left ZIP Code' RoadCenterline:ZIP_L VISIBLE NONE;'Primary Table:Right ZIP Code' RoadCenterline:ZIP_R VISIBLE NONE;
            'Primary Table:Left State' RoadCenterline:STATE_L VISIBLE NONE;'Primary Table:Right State' RoadCenterline:STATE_R VISIBLE NONE;
            'Primary Table:Left Street ID' <None> VISIBLE NONE;'Primary Table:Right Street ID' <None> VISIBLE NONE;
            'Primary Table:Min X value for extent' <None> VISIBLE NONE;'Primary Table:Max X value for extent' <None> VISIBLE NONE;
            'Primary Table:Min Y value for extent' <None> VISIBLE NONE;'Primary Table:Max Y value for extent' <None> VISIBLE NONE;
            'Primary Table:Left Additional Field' <None> VISIBLE NONE;'Primary Table:Right Additional Field' <None> VISIBLE NONE;
            'Primary Table:Altname JoinID' RoadCenterline:SEGID VISIBLE NONE;'*Alternate Name Table:JoinID' RoadAlias:SEGID VISIBLE NONE;
            'Alternate Name Table:Prefix Direction' RoadAlias:A_PRD VISIBLE NONE;'Alternate Name Table:Prefix Type' RoadAlias:A_STP VISIBLE NONE;
            'Alternate Name Table:Street Name' RoadAlias:A_RD VISIBLE NONE;'Alternate Name Table:Suffix Type' RoadAlias:A_STS VISIBLE NONE;
            'Alternate Name Table:Suffix Direction' RoadAlias:A_POD VISIBLE NONE"""

        userMessage("Creating locator from road centerlines...")

        try:
            CreateAddressLocator_geocoding("US Address - Dual Ranges", streetPath + " 'Primary Table';" + roadAliasPath + " 'Alternate Name Table'", fieldMap, AL2, "")
        except:
            try:
                fieldMap = """'Primary Table:Feature ID' <None> VISIBLE NONE;'*Primary Table:From Left' RoadCenterline:L_F_ADD VISIBLE NONE;
                '*Primary Table:To Left' RoadCenterline:L_T_ADD VISIBLE NONE;'*Primary Table:From Right' RoadCenterline:R_F_ADD VISIBLE NONE;
                '*Primary Table:To Right' RoadCenterline:R_T_ADD VISIBLE NONE;'Primary Table:Prefix Direction' RoadCenterline:PRD VISIBLE NONE;
                'Primary Table:Prefix Type' RoadCenterline:STP VISIBLE NONE;'*Primary Table:Street Name' RoadCenterline:RD VISIBLE NONE;
                'Primary Table:Suffix Type' RoadCenterline:STS VISIBLE NONE;'Primary Table:Suffix Direction' RoadCenterline:POD VISIBLE NONE;
                'Primary Table:Left City or Place' RoadCenterline:MUNI_L VISIBLE NONE;
                'Primary Table:Right City or Place' RoadCenterline:MUNI_R VISIBLE NONE;
                'Primary Table:Left ZIP Code' RoadCenterline:ZIP_L VISIBLE NONE;'Primary Table:Right ZIP Code' RoadCenterline:ZIP_R VISIBLE NONE;
                'Primary Table:Left State' RoadCenterline:STATE_L VISIBLE NONE;'Primary Table:Right State' RoadCenterline:STATE_R VISIBLE NONE;
                'Primary Table:Left Street ID' <None> VISIBLE NONE;'Primary Table:Right Street ID' <None> VISIBLE NONE;
                'Primary Table:Display X' <None> VISIBLE NONE;'Primary Table:Display Y' <None> VISIBLE NONE;
                'Primary Table:Min X value for extent' <None> VISIBLE NONE;'Primary Table:Max X value for extent' <None> VISIBLE NONE;
                'Primary Table:Min Y value for extent' <None> VISIBLE NONE;'Primary Table:Max Y value for extent' <None> VISIBLE NONE;
                'Primary Table:Left Additional Field' <None> VISIBLE NONE;'Primary Table:Right Additional Field' <None> VISIBLE NONE;
                'Primary Table:Altname JoinID' RoadCenterline:SEGID VISIBLE NONE;'*Alternate Name Table:JoinID' RoadAlias:SEGID VISIBLE NONE;
                'Alternate Name Table:Prefix Direction' RoadAlias:A_PRD VISIBLE NONE;'Alternate Name Table:Prefix Type' RoadAlias:A_STP VISIBLE NONE;
                'Alternate Name Table:Street Name' RoadAlias:A_RD VISIBLE NONE;'Alternate Name Table:Suffix Type' RoadAlias:A_STS VISIBLE NONE;
                'Alternate Name Table:Suffix Direction' RoadAlias:A_POD VISIBLE NONE"""
                CreateAddressLocator_geocoding("US Address - Dual Ranges", streetPath + " 'Primary Table';" + roadAliasPath + " 'Alternate Name Table'", fieldMap, AL2, "", "DISABLED")
            except:
                try:
                    CreateAddressLocator_geocoding("US Address - Dual Ranges", streetPath + " 'Primary Table';" + roadAliasPath + " 'Alternate Name Table'", fieldMap, AL2, "")
                except:
                    userMessage("Could not create locator from road data")

        if Exists(AL2):
            userMessage("Created road centerline locator")

    #Create composite address locator from addresspoints/road centerline AL3
    if not Exists(AL3):
        userMessage("Creating composite address locator...")
        compositeFieldMap = "Street \"Street or Intersection\" true true true 100 Text 0 0 ,First,#," + AL1 + ",Street,0,0," + AL2 + ",Street,0,0;City \"City or Placename\" true true false 40 Text 0 0 ,First,#,"  + \
            AL1 + ",City,0,0," + AL2 + ",City,0,0;State \"State\" true true false 20 Text 0 0 ,First,#," + AL1 + ",State,0,0," + AL2 + ",State,0,0;ZIP \"ZIP Code\" true true false 10 Text 0 0 ,First,#," + \
            AL1 + ",ZIP,0,0," + AL2 + ",ZIP,0,0"

        CreateCompositeAddressLocator_geocoding(AL1 + " " + co_abbr + "_AddyPt;" + AL2 + " " + co_abbr + "_Roads", compositeFieldMap, co_abbr + "_AddyPt #;" + co_abbr + "_Roads #", AL3)

if __name__ == '__main__':
    main()
