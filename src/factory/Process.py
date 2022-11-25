from asyncio.windows_events import NULL
import random
from factory.Storage import Storage


class Process:
    def __init__(self, processId):
        self.processId = processId
        self.minProcessTime = NULL                                      # 최소 Process 동작 시간
        self.processTime = 0                                            # Process 동작 시간
        self.defectiveRate = 0                                          # 불량률
        self.oldProcessStorage:dict[str,Storage] = {}                   # 이전 공정 Storage 정보
        self.processStorage:dict[str,Storage] = {}                      # 현재 공정 Storage 정보
        
        self.STORAGE = 'STORAGE'                                        # Constant
        self.COST = 'COST'                                              # Constant
        self.defectCount = 0                                            # 불량 발생 횟수
        self.processRunningCount = 0                                    # Process 동작 횟수
        
    def setProcessId(self, processId):
        self.processId = processId
        
    def getProcessId(self):
        return self.processId
        
    def setProcessTime(self, processTime:int):
        self.processTime = processTime
        
    def setMinProcessTime( self, minProcessTime:int):
        self.minProcessTime = minProcessTime
                
    def setDefectiveRate(self, defectiveRate:int):
        # 100 보다 클정우 100으로 고정
        if defectiveRate > 100:
            self.defectiveRate = 100
        else:
            self.defectiveRate = defectiveRate
        
    def addOldProcessStorage(self, storageId, storage, cost:int):
        """ 이전 공정 Storage 지정

        Args:
            storageId (str): 이전 공정 저장소 ID
            storage (obj): 이전 공정 객체
            cost (int): 이전 공정 자재 소모값
        """
        if storageId in self.oldProcessStorage:
            return
        
        self.oldProcessStorage[storageId] = {}
        self.oldProcessStorage[storageId][self.STORAGE] = storage
        self.oldProcessStorage[storageId][self.COST] = cost
        
    def removeOldProcessStorage(self, storageId):
        """ 이전 공정 저장소 삭제

        Args:
            storageId (str): 이전 공정 저장소 ID
        """
        if storageId not in self.oldProcessStorage:
            return
        
        self.oldProcessStorage.pop(storageId)
        
    def addProcessStorage(self, storageId, storage, cost:int):
        """ 현재 공정 저장소 등록

        Args:
            storageId (str): 저장소 ID
            storage (obj): 저장소 객체
            cost (int): 저장소 소모 값
        """
        if storageId in self.processStorage:
            return
        
        self.processStorage[storageId] = {}        
        self.processStorage[storageId][self.STORAGE] = storage
        self.processStorage[storageId][self.COST] = cost
        
    def removeProcessStorage(self, storageId):
        """ 현재 공정 저장소 삭제

        Args:
            storageId (str): 저장소 ID
        """
        if storageId not in self.processStorage:
            return
        
        self.processStorage.pop(storageId)
        
    def getDefectCount(self):
        """ 불량 발생 횟수 반환

        Returns:
            int: 불량 발생 횟수
        """
        return self.defectCount
    
    def getProcessRunningCount(self):
        """ Process 동작 횟수

        Returns:
            int: 동작 횟수
        """
        return self.processRunningCount
        
    def run(self, env):
        """ Process 동작

        Args:
            env (obj): simpy 객체
        """
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