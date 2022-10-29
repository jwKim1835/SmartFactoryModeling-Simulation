import simpy
from factory.Storage import Storage
from factory.Process import Process

class Factory: 
    def __init__(self, env):
        self.dictProcess:dict[str,Process] = {}
        self.dictStorage:dict[str,Storage] = {}
    
    # make storage
    def makeStorage(self, name, maxSize, initSize):
        if name in self.dictStorage:
            return 
        
        self.dictStorage[name] = Storage(name, maxSize, initSize)
    
    # make prcess
    def makeProcess(self, name, processTime, minProcessTime, defectiveRate):
        if name in self.dectPrcess:
            return
        
        newProcess = Process(name)
        newProcess.setProcessTime(processTime)
        newProcess.setMinProcessTime(minProcessTime)
        newProcess.setDefectiveRate(defectiveRate)
        self.dictProcess[name] = newProcess
    
    # connect storage to process
    def connectStorageToProcess(self, processName, oldStorageName, oldStorageCost, storageName, cost):
        if processName not in self.dictProcess:
            print(f"ERROR) Process [%s] is not import!!!" % processName)
            return 
        
        if oldStorageName not in self.dictStorage:
            print(f"ERROR) Storage [%s] is not import!!!!" % oldStorageName)
            return 
        
        if storageName not in self.dictStorage:
            print(f"ERROR) Storage [%s] is not import!!!!" % storageName)
            return 
        
        self.dictProcess[processName].addOldProcessStorage(oldStorageName, self.dictStorage[oldStorageName], oldStorageCost)
        self.dictProcess[processName].addProcessStorage(storageName, self.dictStorage[storageName], cost)
    
    # disconnectOldStorageToProcess
    def disconnectOldStorageToProcess(self, processName, oldStorageName):        
        if processName not in self.dictProcess:
            print(f"ERROR) Process [%s] is not import!!!" % processName)
            return
        
        self.dictProcess[processName].removeOldProcessStorage(oldStorageName)
    
    # disconnectStorageToProcess
    def disconnectStorageToProcess(self, processName, storageName):
        if processName not in self.dictProcess:
            print(f"ERROR) Process [%s] is not import!!!" % processName)
            return
        
        self.dictProcess[processName].removeOldProcessStorage(storageName)
    
    # run Factory
    
    # output
    
    ## show stoarge
    def printStorageInfo(self):
        pass
    
    ## show process
    def printProcessInfo(self):
        pass
    
    