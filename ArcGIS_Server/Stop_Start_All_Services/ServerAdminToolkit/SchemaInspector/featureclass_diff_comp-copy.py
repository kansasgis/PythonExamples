
import arcpy, sets, os, smtplib


gdb1 = "Database Connections/cico_owner.sde/cico.GIS_OWNER.cogo"
gdb2 = "Database Connections/Orthos_owner.sde/Orthos.GIS_OWNER.cogo"
#gdb1 = "\\\\dggissrv2\\temp\\ServerAdminToolkit\\SchemaInspector\\gdb1.gdb\\cogo"
#gdb2 = "\\\\dggissrv2\\temp\\ServerAdminToolkit\\SchemaInspector\\gdb2.gdb\\cogo"
output = "text.txt"
compFlds = arcpy.GetParameterAsText(3)

print_list = []
outFile = open(output, "w")

def write_it(string):
    print string
    outFile.write(string + "\n")


def process_fds(print_list):
    dictFC1 = {}
    dictFC2 = {}
    rcNamesList1 = []
    rcNamesList2 = []

    arcpy.env.workspace = gdb1

    fdsList1 = arcpy.ListDatasets("", "Feature")
    for fds in fdsList1:
        fcList1 = arcpy.ListFeatureClasses("", "", fds)
        dictFC1[fds] = fcList1            


    arcpy.env.workspace = gdb2

    fdsList2 = arcpy.ListDatasets("", "Feature")
    for fds in fdsList2:
        fcList2 = arcpy.ListFeatureClasses("", "", fds)
        dictFC2[fds] = fcList2


    for key in dictFC1.keys():
        if not dictFC2.has_key(key):
            del dictFC1[key]


    for key in dictFC1.keys():
        fcs1 = dictFC1[key]
        fcs2 = dictFC2[key]
        fc1Diff = set(fcs1) - set(fcs2)
        fc1Diff.Split('.').Last()
        fc2Diff = set(fcs2) - set(fcs1)
        for diff in fc2Diff:
            print_list.append(diff)
            fcs2.remove(diff)
        print_list_fcs(gdb1 + os.sep + key, print_list)
        print_list = []
        
        for diff in fc1Diff:
            print_list.append(diff)
            fcs1.remove(diff)
        print_list_fcs(gdb2 + os.sep + key, print_list)
        print_list = []



#**********************************************************
# Main
#.Split('.').Last()

#def modify_a(a):
    #new = a.split('.').last()
    #return new


#**********************************************************
# Get Feature Class lists for both geodatabases
arcpy.env.workspace = gdb1
gdb1FCList = arcpy.ListFeatureClasses()
ngdb1FCList = []
for a in gdb1FCList:
    a = a.split(".",2) [2]
    ngdb1FCList.append(a)
    
print ", ".join(map(str, ngdb1FCList))
    


arcpy.env.workspace = gdb2
gdb2FCList = arcpy.ListFeatureClasses()
ngdb2FCList = []
for b in gdb2FCList:
    b = b.split(".",2) [2]
    ngdb2FCList.append(b)

print ", ".join(map(str, ngdb2FCList))

#**********************************************************
# Process Feature Classes in Feature Datasets
#process_fds(print_list)


#**********************************************************
# Compare Feature Classes
def get_diff1(feat_type, db, list1, list2):
    diffList = set(list1) - set(list2)
    if len(diffList) > 0:
        write_it("*****************************************************************")
        write_it(feat_type + " missing from " + db + ":")
        for diff in diffList:
            write_it(diff)
            arcpy.CopyFeatures_management(gdb2+"/"+diff, gdb1+"/"+diff)
            list1.remove(diff)
        write_it("\n")
    return list1

    

fcList2 = get_diff1("Feature Classes", gdb2, ngdb2FCList, ngdb1FCList)


def get_diff2(feat_type, db, list1, list2):
    diffList1 = set(list1) - set(list2)
    if len(diffList1) > 0:
        write_it("*****************************************************************")
        write_it(feat_type + " missing from " + db + ":")
        for diff in diffList1:
            write_it(diff)
            arcpy.CopyFeatures_management(gdb1+"/"+diff, gdb2+"/"+diff)
            list1.remove(diff)
        write_it("\n")
    return list1
fcList1 = get_diff2("Feature Classes", gdb1, ngdb1FCList, ngdb2FCList)





FILE = open(

if [item for item in fcList1 if item not in fcList2]:
    TO = ["Terrol Palmer <tpalmer@douglas-county.com>"]
    SUBJECT = "City of Lawrence GIS new COGO"
    MSG = "test"
else:
    print "fcList2"



if [item for item in fcList2 if item not in fcList1]:
    TO = ["Terrol Palmer <tpalmer@douglas-county.com>"]
    SUBJECT = "Douglas County GIS GIS new COGO"
    MSG = "test"
else:
    print "fcList1"    


if [fcList2==fcList1]:
    TO = ["Terrol Palmer <tpalmer@douglas-county.com>"]
    SUBJECT = "COGO Dataset is Syncronized"
    MSG = "test"
else:
    print "not equal"

    
#emailList = ["Terrol Palmer <tpalmer@douglas-county.com>"]
# take the email list and use it to send an email to connected users.
SERVER = "DGMAILSRV3.dgco.net"
FROM = "SDE Admin <SDEAdmin@douglas-county.com>"
#TO = emailList
#SUBJECT = "New BOLL and Parcels were built"
#MSG = "Auto Generated Message.\n\r Python scripts are working!!!"
#MSG = "Auto generated Message.\n\rServer maintenance will be performed in 15 minutes. Please log off."

# Prepare actual message
MESSAGE = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, MSG)

# Send the mail
server = smtplib.SMTP(SERVER)
server.sendmail(FROM, TO, MESSAGE)
server.quit()








outFile.close()
arcpy.SetParameterAsText(4, output)

print "Done!"


