from asyncio.windows_events import NULL
import random
from factory.Storage import Storage


class Process:
    def __init__(self, processId):
        self.processId = processId
        self.minProcessTime = NULL
        self.processTime = 0
        self.defectiveRate = 0
        self.oldProcessStorage:dict[str,Storage] = {}
        self.processStorage:dict[str,Storage] = {}
        
        self.STORAGE = 'STORAGE'
        self.COST = 'COST'
        self.defectCount = 0
        self.processRunningCount = 0
        
    def setProcessId(self, processId):
        self.processId = processId
        
    def getProcessId(self):
        return self.processId
        
    def setProcessTime(self, processTime:int):
        self.processTime = processTime
        
    def setMinProcessTime( self, minProcessTime:int):
        self.minProcessTime = minProcessTime
                
    def setDefectiveRate(self, defectiveRate:int):
        if defectiveRate > 100:
            self.defectiveRate = 100
        else:
            self.defectiveRate = defectiveRate
        
    def addOldProcessStorage(self, storageId, storage, cost:int):
        if storageId in self.oldProcessStorage:
            return
        
        self.oldProcessStorage[storageId] = {}
        self.oldProcessStorage[storageId][self.STORAGE] = storage
        self.oldProcessStorage[storageId][self.COST] = cost
        
    def removeOldProcessStorage(self, storageId):
        if storageId not in self.oldProcessStorage:
            return
        
        self.oldProcessStorage.pop(storageId)
        
    def addProcessStorage(self, storageId, storage, cost:int):
        if storageId in self.processStorage:
            return
        
        self.processStorage[storageId] = {}        
        self.processStorage[storageId][self.STORAGE] = storage
        self.processStorage[storageId][self.COST] = cost
        
    def removeProcessStorage(self, storageId):
        if storageId not in self.processStorage:
            return
        
        self.processStorage.pop(storageId)
        
    def getDefectCount(self):
        return self.defectCount
    
    def getProcessRunningCount(self):
        return self.processRunningCount
        
    def run(self, env):
        self.defectCount = 0
        while True:
            for oldStorage in self.oldProcessStorage.values():
                yield oldStorage[self.STORAGE].get(oldStorage[self.COST])
            
            yield env.timeout(self.processTime)
            
            self.processRunningCount += 1
            
            # 불량확율 조건 필요
            if random.randrange(1, 101) < self.defectiveRate:
                self.defectCount += 1
                continue
            
            for storage in self.processStorage.values():
                yield storage[self.STORAGE].put(storage[self.COST])            
            
    def printProcessInfo(self):
        pass        # 현재 process 정보를 Print하는 로직 추가 필요