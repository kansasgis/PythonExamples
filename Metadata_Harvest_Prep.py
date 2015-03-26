#-------------------------------------------------------------------------------
# Name:        Metadata_Harvest_Prep
# Purpose:
#
# Author:      kristen
#
# Created:     11/09/2014
#-------------------------------------------------------------------------------
def listmetadatafiles(folder):
    import os
    mList = []
    list = os.listdir(folder)
    for names in list:
        if names.endswith(".xml"):
            mList.append(names)
    return mList

def getPermalink(data_id):
    #return permanent link to the website for a given data id
    permalink = 'http://kansasgis.org/catalog/index.cfm?data_id=' + data_id + '&show_cat=1'
    return permalink

def getOracleInfo(qry):
    import cx_Oracle

    #submit query
    connstr = ''
    conn = cx_Oracle.connect('DASC2', '', connstr)
    curs = conn.cursor()
    try:
        curs.execute(qry)

    except:
        curs = ""

    return curs
    conn.close()

def editXMLInfo(metadataPath, node, value):
    import xml.etree.ElementTree as ET

    #get xml file set up
    xml1 = ET.ElementTree()
    xml1.parse(metadataPath)
    root = xml1.getroot()

    #make sure node already exists
    k = root.getiterator(node)

    if len(k) != 0:
        for r in k:
            #edit node value
            r.text = value
            #save metadata file
            xml1.write(metadataPath)

def addXMLInfo(metadataPath, newNode, aboveNode, value):
    import xml.etree.ElementTree as ET

    #get xml file set up
    xml1 = ET.ElementTree()
    xml1.parse(metadataPath)
    root = xml1.getroot()

    #see if the node already exists
    k = root.getiterator(newNode)
    #if not, it needs to be added
    if len(k) == 0:
        #adds new sub element to first node named like aboveNode
        r = root.getiterator(aboveNode)[0]
        #create new node
        a = ET.SubElement(r, newNode)
        #set node value
        a.text = value
        #save metadata file
        xml1.write(metadataPath)

def main():
    import os, shutil
    #set root folder
    root = r"\\ricochet\c$\BigDrives\webdata\webdata0\dascweb\docs\catalog\metadata\LinkFix"
##    root = r"E:\Kristen\Metadata\Harvesting"

    #get list of metadata files
    metadatas = listmetadatafiles(root)

    for metadata in metadatas:

        archive = 0
        permalink = ''
        used = 0

        qry = "SELECT META_ID FROM METADATA_FILES WHERE FILE_NAME = '" + metadata + "'"

        curs = getOracleInfo(qry)

        for m in curs:
            meta_id = str(m[0])
            used = 1

            qry2 = '''SELECT data_metadata_lnk.DATA_ID, data_catg_lnk.CAT_ID
                FROM data_metadata_lnk inner join data_catg_lnk on data_metadata_lnk.data_id = data_catg_lnk.data_id WHERE data_metadata_lnk.META_ID = ''' + meta_id

            curs2 = getOracleInfo(qry2)

            for data_item in curs2:
                data_id = str(data_item[0])
                cat_id = str(data_item[1])

                if cat_id == '99':
                    archive = 1

                permalink = getPermalink(data_id)
                fullPath = os.path.join(root, metadata)
##                editXMLInfo(fullPath, "networkr", permalink)
##                editXMLInfo(fullPath, "onlink", permalink)
                addXMLInfo(fullPath, "onlink", "citeinfo", permalink)

            if used == 1 and archive == 0 and permalink == '':
                used = 0

        if used == 0:
            fullPath = os.path.join(root, metadata)
            newPath = os.path.join(root, "not_currently_used", metadata)
            shutil.move(fullPath, newPath)

        print '"' + metadata + '"', str(used), str(archive), permalink

if __name__ == '__main__':
    main()
