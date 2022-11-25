import csv
import pprint

import simpy

from factory.Factory import Factory

class CSVFactoryLoader:
    
    def __init__(self):
        self.factoryInfo:dict[str,dict] = {}
        self.csvFileInfo:list = []
    
    def load(self, path):
        """CSV File을 읽어와 dict에 저장

        Args:
            path (str): csv 파일 위치

        Returns:
            bool: 파일 읽어온 후 처리 결과(정상: True, 실패: False)
        """
        try:
            fileInfo = {}
            printPretty = pprint.PrettyPrinter()
            with open("resource/sample.csv", newline="") as csvFile:
                reader = csv.DictReader(csvFile)
                for row in reader:
                    self.csvFileInfo.append(row)
                    # Factory 등록
                    if row["Factory"] not in fileInfo:
                        fileInfo[row["Factory"]] = { "Process": dict[str,list](), "Storage": {}}
                
                    # Factory에 해당하는 Process 등록
                    if row["Type"] == "Process":
                        if row["Name"] not in fileInfo[row["Factory"]]["Process"]:
                            fileInfo[row["Factory"]]["Process"][row["Name"]] = []
                        
                        fileInfo[row["Factory"]]["Process"][row["Name"]].append(row)

                    # Factory에 해당하는 Storage를 등록
                    elif row["Type"] == "Storage":
                        fileInfo[row["Factory"]]["Storage"][row["Name"]] = row
            
            # CSV File 정보 출력
            print( f"csv Path: %s" % path)
            print( f"csv file info: ", end='')
            printPretty.pprint(fileInfo)
            
            # CSV File 검증
            if self.verifyLoadData(fileInfo) == False:
                return False
            
            self.factoryInfo = fileInfo
            
            return True
            
        except FileNotFoundError as fileExceiptn:
            print( f"File Not Found Error!!!! [%s]" % path)
            
        return False
            
    def verifyLoadData(self, fileInfo:dict()):
        """CSV File 검증

        Args:
            fileInfo (dict): 검증할 CSV 파일 정보를 담은 dict

        Returns:
            bool: 성공(True), 실패(False)
        """
        
        for type, factory in fileInfo.items():
            print( f"Factory Name: %s" % type )
    
            # Process 검증
            for processName, processList in fileInfo[type]["Process"].items():
                for process in processList:
                    # Storage 검증
                    # OldProcessStorage Name이 Storage에 있는가?
                    if process.get("OldProcessStorage") not in fileInfo[type]["Storage"]:
                        print( f"OldProcessStorage %s is not import csv file" % process.get("OldProcessStorage") )
                        return False
    
                    # ProcessStorage Name이 Storage에 있는가?
                    elif process.get("ProcessStorage") not in fileInfo[type]["Storage"]:
                        print( f"ProcessStorage %s is not import csv file" % process.get("ProcessStorage") )
                        return False
                    
        print( "verify complete" )
        return True
    
    def makeFactory(self):
        """ CSV 파일을 읽어온 dict를 통해 Factory 객체를 생성

        Returns:
            list[Factory]: 생성된 Factory 객체를 담은 list를 반환
        """
        resultFactoryList:list[Factory] = []
        
        for name, factoryData in self.factoryInfo.items():
            # Factory 생성
            factory = Factory(name)
            resultFactoryList.append(factory)
    
            # Factory에 Storage 정보를 등록
            for storageName, storage in self.factoryInfo[name]["Storage"].items():
                factory.makeStorage(storageName, storage.get("MaxSize"), storage.get("InitSize"))
        
            # Factory에 Process 정보를 등록
            for processName, processList in self.factoryInfo[name]["Process"].items():
                for process in processList:
                    factory.makeProcess(processName, process.get("Time"), process.get("MinTime"), process.get("DefectiveRate"))                                                                             # Process 생성
                    factory.connectStorageToProcess(processName, process.get("OldProcessStorage"), process.get("OldProcessStorageCost"), process.get("ProcessStorage"), process.get("ProcessStorageCost"))  # Process에 Storage 연결
                
        return resultFactoryList
    
    def getCSVFileData(self):
        """ 읽어온 CSV 파일 정보를 반환

        Returns:
           list[dict] : CSV 파일 정보를 반환
        """
        return self.csvFileInfo