import factory.storage

class process:
    def __init__(self, processId):
        self.processId = processId
        self.processTime = 0
        self.defectiveRate = 0.0
        self.oldProcessStorage = {}
        self.processStorage = {}
        
        self.STORAGE = 'STORAGE'
        self.COST = 'COST'
        self.defectCount = 0
        
    def setProcessId(self, processId):
        self.processId = processId
        
    def getProcessId(self):
        return self.processId
        
    def setProcessTime(self, processTime):
        self.processTime = processTime
                
    def setDefectiveRate(self, defectiveRate):
        self.defectiveRate = defectiveRate
        
    def addOldProcessStorage(self, storageId, storage, cost):
        if storageId in self.oldProcessStorage:
            return
        
        self.oldProcessStorage[storageId] = {}
        self.oldProcessStorage[storageId][self.STORAGE] = storage
        self.oldProcessStorage[storageId][self.COST] = cost
        
    def removeOldProcessStorage(self, storageId):
        if storageId not in self.oldProcessStorage:
            return
        
        self.oldProcessStorage.pop(storageId)
        
    def addProcessStorage(self, storageId, storage, cost):
        if storageId in self.processStorage:
            return
        
        self.processStorage[storageId] = {}        
        self.processStorage[storageId][self.STORAGE] = storage
        self.processStorage[storageId][self.COST] = cost
        
    def removeProcessStorage(self, storageId):
        if storageId not in self.processStorage:
            return
        
        self.processStorage.pop(storageId)
        
    def run(self, env):
        defectCount = 0
        while True:
            for oldStorage in self.oldProcessStorage.values():
                yield oldStorage[self.STORAGE].get(oldStorage[self.COST])
            
            yield env.timeout(self.processTime)
            
            # 불량확율 조건 필요
            
            for storage in self.processStorage.values():
                yield storage[self.STORAGE].put(storage[self.COST])
            
            
    def printProcessInfo(self):
        pass        # 현재 process 정보를 Print하는 로직 추가 필요