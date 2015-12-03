def SQL_Command(command, db):
    import win32com, win32com.client, adoconstants
    from adoconstants import *

    conn = win32com.client.Dispatch(r'ADODB.Connection')
    DSN = 'DRIVER={SQL Server};SERVER=JADE\PARKS;DATABASE=' + db + ';uid=sa;pwd=nooracle123!;'
    conn.Open(DSN)

    cmd = win32com.client.Dispatch(r'ADODB.Command')
    cmd.ActiveConnection = conn
    cmd.CommandType = adCmdText
    cmd.CommandText = command
    cmd.Prepared = True

    success = 0
    try:
        cmd.Execute()
        success = 1
    except Exception as e:
        print str(e)
        try:
            cmd.Execute()
            success = 1
        except Exception as e:
            print str(e)
            print "Unable to execute command '" + command + "'"

    return success

ksdb = "KS"

kdorTblDict = {"KDOR_FinalAssessment":"vwKDOR_FinalAssessment", "KDOR_Sale_Date":"vwKDOR_Sale_Date", "KDOR_Sale_Source_Confirm":"vwKDOR_Sale_Source_Confirm",
            "KDOR_vwPropertyGeneral":"vwKDOR_vwPropertyGeneral", "KDOR_vwPropertyTransfer":"vwKDOR_vwPropertyTransfer"}

#iterate through the table/view dictionary to populate the command syntax
for tbl, vw in kdorTblDict.iteritems():
    delCommand1 = "DROP TABLE " + tbl
    print delCommand1
    vwCommand = "SELECT * INTO " + tbl + " FROM dbo." + vw
    print vwCommand

    SQL_Command(delCommand1, ksdb)
    SQL_Command(vwCommand, ksdb)
