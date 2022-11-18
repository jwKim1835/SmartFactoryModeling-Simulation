import simpy
from factory.Storage import Storage
from factory.Process import Process

class Factory: 
    def __init__(self, name):
        self.dictProcess:dict[str,Process] = {}
        self.dictStorage:dict[str,Storage] = {}
        self.name = name
        self.env = simpy.Environment()
    
    # make storage
    def makeStorage(self, name, maxSize, initSize):
        if name in self.dictStorage:
            return 
        
        nMaxSize = 0
        if type(maxSize) == int:
            nMaxSize = maxSize
        
        else:
            nMaxSize = int(maxSize)
        
        nInitSize = 0
        if type(initSize) == int:
            nInitSize = initSize
        
        else:
            nInitSize = int(initSize)
        
        self.dictStorage[name] = Storage(self.env, name, nMaxSize, nInitSize)
    
    # make prcess
    def makeProcess(self, name, processTime, minProcessTime, defectiveRate):
        if name in self.dictProcess:
            return
        
        nProcessTime = 0
        nMinProcessTime = 0
        fDefectiveRate = 0.0
        if type(processTime) == int:
            nProcessTime = processTime
        else:
            nProcessTime = int(processTime)
            
        if type(minProcessTime) == int:
            nMinProcessTime = minProcessTime
        else:
            nMinProcessTime = int(minProcessTime or 0)
        
        if type(defectiveRate) == int:
            fDefectiveRate = defectiveRate
        else:
            fDefectiveRate = int(defectiveRate or 0)
        
        newProcess = Process(name)      
        newProcess.setProcessTime(nProcessTime)
        newProcess.setMinProcessTime(nMinProcessTime)
        newProcess.setDefectiveRate(fDefectiveRate)
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
        
        nOldStorageCost = 0
        nCost = 0
        
        try:
            if type(oldStorageCost) == int:
                nOldStorageCost = oldStorageCost
            else:
                nOldStorageCost = int(oldStorageCost)
        except:
            print( f"read OldStorage: %s OldStorageCost: %s CurrentOldStorageCost: %d" % (oldStorageName, oldStorageCost, nOldStorageCost) )
        
        try:
            if type(cost) == int:
                nCost = cost
            else:
                nCost = int(cost)
        except:
            print( f"read Storage: %s StorageCost: %s CurrentStorageCost: %d" % (storageName, cost, nCost) )
                    
        self.dictProcess[processName].addOldProcessStorage(oldStorageName, self.dictStorage[oldStorageName], nOldStorageCost)
        self.dictProcess[processName].addProcessStorage(storageName, self.dictStorage[storageName], nCost)
    
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
        
        self.dictProcess[processName].removeProcessStorage(storageName)
    
    # run Factory
    def runProcess(self, time:int):
        print(f"running -- [%s] -- Factory" % self.name)
        for processName, process in self.dictProcess.items():
            print(f"running [%s] process!!!!!!!" % processName)
            self.env.process(process.run(self.env))
            
        self.env.run( until=time )
    
    # output
    def getFactoryName(self):
        return self.name
    
    def getStorageData(self):
        dictStorage = dict[str,int]()
        
        for name, storage in self.dictStorage.items():
            dictStorage[name] = storage.getSize()
            
        return dictStorage
        
        # dictStorage["Column"].append("Factory")
        # dictStorage["Data"].append(self.getFactoryName())
        # for name, storage in self.dictStorage.items():
        #     dictStorage["Column"].append(name)
        #     dictStorage["Data"].append(storage.getSize())
            
    def getProcessDefectData(self):
        dictProcessDefect = dict[str, int]()
        for name, process in self.dictProcess.items():
            dictProcessDefect[name] = process.getDefectCount()
    
    ## show stoarge
    def printStorageInfo(self):
        for storageName, storage in self.dictStorage.items():
            print( f'[%s] %s storage current size: %d' % (self.name, storageName, storage.getSize()) )
    
    ## show process
    def printProcessInfo(self):
        pass
    
    