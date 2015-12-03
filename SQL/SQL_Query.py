def getCRSLis1():
    import os
    query = "SELECT CountyAbbreviation, ParcelTaxYear FROM OrkaCountyData.dbo.CountyData"
    rs = getSQLInfo(query)
    crsList = {}
    while not rs.EOF:
        co_abbr = rs.Fields.Item("CountyAbbreviation").value
        taxYear = rs.Fields.Item("ParcelTaxYear").value
        crsList[co_abbr] = taxYear
        rs.MoveNext()
    return crsList

def getSQLdsn():
    DSN = 'DRIVER={SQL Server};SERVER=JADE\PARKS;DATABASE=OrkaCountyData;uid=orka_web;pwd=;'
    return DSN

def getSQLInfo(query):
    import win32com.client

    conn = win32com.client.Dispatch(r'ADODB.Connection')
    DSN = getSQLdsn()
    conn.Open(DSN)

    rs = win32com.client.Dispatch(r'ADODB.Recordset')
    rs.Open(query, conn, 1, 3)
    return rs
    rs.Close()
    conn.Close()
    del rs, conn