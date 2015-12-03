#This script not used by any tools directly
'''
This script will list all services

==Inputs==
ServerName
Port
AdminUser
AdminPassword (sent in clear text)
'''

import urllib, urllib2, json
import arcpy

class MyClass():
    def gentoken(server, port, adminUser, adminPass, expiration=60):
        #Re-usable function to get a token required for Admin changes
        
        query_dict = {'username':   adminUser,
                      'password':   adminPass,
                      'expiration': str(expiration),
                      'client':     'requestip'}
        
        query_string = urllib.urlencode(query_dict)
        url = "http://{}:{}/arcgis/admin/generateToken".format(server, port)
        
        token = json.loads(urllib.urlopen(url + "?f=json", query_string).read())
            
        if "token" not in token:
            arcpy.AddError(token['messages'])
            quit()
        else:
            return token['token']



    def getServiceList(server, port,adminUser, adminPass, token=None):
        ''' Function to get all services
        Requires Admin user/password, as well as server and port (necessary to construct token if one does not exist).
        If a token exists, you can pass one in for use.  
        Note: Will not return any services in the Utilities or System folder
        '''    
        
        
        if token is None:    
            token = gentoken(server, port, adminUser, adminPass)    
        
        services = []    
        folder = ''    
        URL = "http://{}:{}/arcgis/admin/services{}?f=pjson&token={}".format(server, port, folder, token)    

        serviceList = json.loads(urllib2.urlopen(URL).read())

        # Build up list of services at the root level
        for single in serviceList["services"]:
            services.append(single['serviceName'] + '.' + single['type'])
         
        # Build up list of folders and remove the System and Utilities folder (we dont want anyone playing with them)
        folderList = serviceList["folders"]
        folderList.remove("Utilities")             
        #folderList.remove("System")
            
        if len(folderList) > 0:
            for folder in folderList:                                              
                URL = "http://{}:{}/arcgis/admin/services/{}?f=pjson&token={}".format(server, port, folder, token)    
                fList = json.loads(urllib2.urlopen(URL).read())
                
                for single in fList["services"]:
                    services.append(folder + "//" + single['serviceName'] + '.' + single['type'])                    
        
        return services
       
      


    def stopStartServices(server, port, adminUser, adminPass, stopStart, serviceList, token=None):  
        ''' Function to stop, start or delete a service.
        Requires Admin user/password, as well as server and port (necessary to construct token if one does not exist).
        stopStart = Stop|Start|Delete
        serviceList = List of services. A service must be in the <name>.<type> notation
        If a token exists, you can pass one in for use.  
        '''    
        
        # Get and set the token
        if token is None:       
            token = gentoken(server, port, adminUser, adminPass)
        
        # Getting services from tool validation creates a semicolon delimited list that needs to be broken up
        services = serviceList.split(';')
        
        #modify the services(s)    
        for service in services:        
            service = urllib.quote(service.encode('utf8'))
            op_service_url = "http://{}:{}/arcgis/admin/services/{}/{}?token={}&f=json".format(server, port, service, stopStart, token)        
            status = urllib2.urlopen(op_service_url, ' ').read()
            
            if 'success' in status:
                arcpy.AddMessage(str(service) + " === " + str(stopStart))
            else:
                arcpy.AddWarning(status)
        
        return 

    
if __name__ == "__main__":     
    
    # Gather inputs      
    server = "dggissrv2" 
    port = "6080" 
    adminUser = "siteadmin"  
    adminPass ="gisserver2"
    stopStart = "Start" 
    #serviceList = getServiceList(server, port,adminUser, adminPass, token=None)
    
my_class = MyClass()
my_class.getServiceList(server, port, adminUser, adminPass)
my_class.stopStartServices(server, port, adminUser, adminPass, stopStart, serviceList)
      
        
