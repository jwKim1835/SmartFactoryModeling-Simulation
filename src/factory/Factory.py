import simpy
from factory.Storage import Storage
from factory.Process import Process

class Factory: 
    def __init__(self, name):
        self.dictProcess:dict[str,Process] = {}                 # Process 정보를 저장
        self.dictStorage:dict[str,Storage] = {}                 # Storage 정보를 저장
        self.name = name                                        # Factory 이름
        self.env = simpy.Environment()
    
    # make storage
    def makeStorage(self, name, maxSize, initSize):
        """ Factory에 Storage 등록

        Args:
            name (str): Storage 이름
            maxSize (int): Storage MAX 값
            initSize (int): Storage 현재 값
        """
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
        """ Factory에 Process를 등록

        Args:
            name (str): Process 이름
            processTime (int): Process 처리 시간
            minProcessTime (int): Process 최소 처리 시간
            defectiveRate (int): Process 불량률
        """
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
    
    def connectStorageToProcess(self, processName, oldStorageName, oldStorageCost, storageName, cost):
        """ Process가 처리할 Storage 등록

        Args:
            processName (str): 연결할 Process 이름
            oldStorageName (str): Process가 가공할 이전 공정의 자재 저장소 이름
            oldStorageCost (int): Process가 가공할 이전 공정의 자재 소모 값
            storageName (str): Process가 가공 후 자재 저장소 이름
            cost (int): Process가 가공후 자재 저장소에 저장할 값
        """
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
    
    def disconnectOldStorageToProcess(self, processName, oldStorageName):        
        """ Process에 연결 한 이전 공정의 저장소를 삭제

        Args:
            processName (str): Process 이름
            oldStorageName (str): 이전 공정의 저장소 이름
        """
        if processName not in self.dictProcess:
            print(f"ERROR) Process [%s] is not import!!!" % processName)
            return
        
        self.dictProcess[processName].removeOldProcessStorage(oldStorageName)
    
    # disconnectStorageToProcess
    def disconnectStorageToProcess(self, processName, storageName):
        """ Process에 연결 한 자재를 저장 할 저장소를 삭제

        Args:
            processName (str): Process 이름
            storageName (str): 자재를 저장할 저장소 이름
        """
        if processName not in self.dictProcess:
            print(f"ERROR) Process [%s] is not import!!!" % processName)
            return
        
        self.dictProcess[processName].removeProcessStorage(storageName)
    
    # run Factory
    def runProcess(self, time:int):
        """ Process를 실행

        Args:
            time (int): Process 가 자재를 가공하는데 걸리는 시간
        """
        print(f"running -- [%s] -- Factory" % self.name)
        for processName, process in self.dictProcess.items():
            print(f"running [%s] process!!!!!!!" % processName)
            self.env.process(process.run(self.env))
            
        self.env.run( until=time )
    
    # output
    def getFactoryName(self):
        """ 현재 Factory의 이름 반환

        Returns:
            str: Factory 이름
        """
        return self.name
    
    def getStorageData(self):
        """ Factory의 Process가 동작 후 저장소의 값 반환

        Returns:
            dict: 화면에 출력할 Storage 정보를 반환
        """
        dictStorage = dict[str,int]()
        
        for name, storage in self.dictStorage.items():
            dictStorage[name] = storage.getSize()
            
        return dictStorage
    
    def getProcessData(self):
        """ Factory의 Process가 처리한 정보를 반환

        Returns:
            dict: 화면에 출력 할 Process 정보를 반환
        """
        dictProcessData = dict[str, dict[str,list]]()
        for name, process in self.dictProcess.items():
            dictProcessData[name] = dict( Type = ["Process", "ProcessRunningCount", "DefectCount"]
                                         , Parent = ["", "Process", "Process"]
                                         , Value = [0, process.getProcessRunningCount(), process.getDefectCount()])
            
        return dictProcessData
    
    def printStorageInfo(self):
        """ 저장소 정보를 Console로 출력
        """
        for storageName, storage in self.dictStorage.items():
            print( f'[%s] %s storage current size: %d' % (self.name, storageName, storage.getSize()) )
    
    