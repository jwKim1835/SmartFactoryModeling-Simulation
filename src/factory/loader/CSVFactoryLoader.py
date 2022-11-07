import csv
import pprint

import simpy

from factory.Factory import Factory

#-------------------------------------------------------------------------------------------------------------------
# Sample Read Data
# {
#     'Machine1': 
#     {
#         'Process': 
#         {
#             'TestProcess': 
#             {
#                 'Factory': 'Machine1', 'Type': 'Process', 'Name': 'TestProcess', 'MaxSize': '', 'InitSize': '', 'Time': '3', 'MinTime': '', 'OldProcessStorage': 'Test', 'OldProcessStorageCost': '2', 'ProcessStorage': 'Test2', 'ProcessStorageCost': '1', 'DefectiveRate': ''
#             }
#         },   
#         'Storage': 
#         {
#             'Test': 
#             {
#                 'Factory': 'Machine1', 'Type': 'Storage', 'Name': 'Test', 'MaxSize': '1000', 'InitSize': '500', 'Time': '', 'MinTime': '', 'OldProcessStorage': '', 'OldProcessStorageCost': '', 'ProcessStorage': '', 'ProcessStorageCost': '', 'DefectiveRate': ''
#             }, 
#             'Test2': 
#             {
#                 'Factory': 'Machine1', 'Type': 'Storage', 'Name': 'Test2', 'MaxSize': '2000', 'InitSize': '0', 'Time': '', 'MinTime': '', 'OldProcessStorage': '', 'OldProcessStorageCost': '', 'ProcessStorage': '', 'ProcessStorageCost': '', 'DefectiveRate': ''
#             }
#         }
#     }
# }
#-------------------------------------------------------------------------------------------------------------------
class CSVFactoryLoader:
    
    def __init__(self):
        self.factoryInfo:dict[str,dict] = {}
    
    def load(self, path):
        try:
            fileInfo = {}
            printPretty = pprint.PrettyPrinter()
            with open("resource/sample.csv", newline="") as csvFile:
                reader = csv.DictReader(csvFile)
                for row in reader:
                    if row["Factory"] not in fileInfo:
                        fileInfo[row["Factory"]] = { "Process": dict[str,list](), "Storage": {}}
                
                    if row["Type"] == "Process":
                        if row["Name"] not in fileInfo[row["Factory"]]["Process"]:
                            fileInfo[row["Factory"]]["Process"][row["Name"]] = []
                        
                        fileInfo[row["Factory"]]["Process"][row["Name"]].append(row)

                    elif row["Type"] == "Storage":
                        fileInfo[row["Factory"]]["Storage"][row["Name"]] = row
                        
            print( f"csv Path: %s" % path)
            print( f"csv file info: ", end='')
            printPretty.pprint(fileInfo)
            
            if self.verifyLoadData(fileInfo) == False:
                return False
            
            self.factoryInfo = fileInfo
            
            return True
            
        except FileNotFoundError as fileExceiptn:
            print( f"File Not Found Error!!!! [%s]" % path)
            
        return False
            
    def verifyLoadData(self, fileInfo:dict()):
        
        for type, factory in fileInfo.items():
            print( f"Factory Name: %s" % type )
    
            # check process Storage
            for processName, processList in fileInfo[type]["Process"].items():
                for process in processList:
                    # chekc storage
                    if process.get("OldProcessStorage") not in fileInfo[type]["Storage"]:
                        print( f"OldProcessStorage %s is not import csv file" % process.get("OldProcessStorage") )
                        return False
        
                    elif process.get("ProcessStorage") not in fileInfo[type]["Storage"]:
                        print( f"ProcessStorage %s is not import csv file" % process.get("ProcessStorage") )
                        return False
                    
        print( "verify complete" )
        return True
    
    def makeFactory(self):
        resultFactoryList:list[Factory] = []
        
        for name, factoryData in self.factoryInfo.items():
            factory = Factory(name)
            resultFactoryList.append(factory)
    
            for storageName, storage in self.factoryInfo[name]["Storage"].items():
                factory.makeStorage(storageName, storage.get("MaxSize"), storage.get("InitSize"))
        
            for processName, processList in self.factoryInfo[name]["Process"].items():
                for process in processList:
                    factory.makeProcess(processName, process.get("Time"), process.get("MinTime"), process.get("DefectiveRate"))
                    factory.connectStorageToProcess(processName, process.get("OldProcessStorage"), process.get("OldProcessStorageCost"), process.get("ProcessStorage"), process.get("ProcessStorageCost"))
                
        return resultFactoryList