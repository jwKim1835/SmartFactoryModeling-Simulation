import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))                    # import parent directory
import pandas as pd
import streamlit as st
import plotly.express as px
from factory.loader.CSVFactoryLoader import CSVFactoryLoader

class FactorySetting:
    def __init__(self):
        self.csvFileInfo = None
        pass
    
    def initialize(self):
        pass
    
    def drawFileUploader(self):
        uploadFile = st.file_uploader("CSV File ONLY", type=".csv")
        if uploadFile is not None:
            self.readFile(uploadFile)
            
    def drawSampleFileCheckBox(self):
        if self.csvFileInfo is not None:
            return
        
        isUseSampleFile = st.checkbox("Use Sample Data", False)
        if isUseSampleFile:
            self.readFile("resource/sample.csv")
            
            
    def drawDataFrame(self):
        st.dataframe(self.csvFileInfo)
            
    def drawTimeInput(self):
        with st.form("TimeForm"):
            factoryRunningTime = st.text_input("Factory Running Time")
            submitted = st.form_submit_button("Running")
            
            if submitted:
                try:
                    nFactoryRunningTime = int(factoryRunningTime)
                    
                    for factory in self.listFactory:
                        factory.runProcess(nFactoryRunningTime)
                        
                    self.drawDataInfo()
                except Exception as e:
                    st.error(f"ERROR) Only Number Input: %s" % (factoryRunningTime))
    
    def drawDataInfo(self):
        listStorageName = self.getFactoryStorageNames()
        listStorageChartColumn = ["Factory"]
        listStorageChartColumn.extend(listStorageName)
        
        listChartDatas = []                        
        for factory in self.listFactory:
            listStorageData = [factory.getFactoryName()]
            listColumData = ["" for index in range(listStorageName.__len__())]
            
            for column, data in factory.getStorageData().items():
                index = listStorageName.index(column)
                listColumData.insert(index, data)
                listColumData.pop(index+1)
            
            listStorageData.extend(listColumData)
            listChartDatas.append(listStorageData)
                
        storageFrame = pd.DataFrame(data=listChartDatas, columns=listStorageChartColumn)
        fig = px.bar(storageFrame, x="Factory", y=listStorageName, barmode="group")
            
        st.plotly_chart(fig)
            
        
    def readFile(self, file):
        if self.csvFileInfo is not None:
            return
        
        loader = CSVFactoryLoader()
        if loader.load( file ):
            self.listFactory = loader.makeFactory()
            self.csvFileInfo = loader.getCSVFileData()
            
    def getFactoryStorageNames(self):
        listStorageName = list[str]()
        
        for factory in self.listFactory:
            for storageName in factory.getStorageData().keys():
                if storageName not in listStorageName:
                    listStorageName.append(storageName)
                    
        return listStorageName

    def draw(self):
        st.markdown("# Factory Settings")
        self.drawFileUploader()
        self.drawSampleFileCheckBox()
        if self.csvFileInfo is not None:
            self.drawDataFrame()
            self.drawTimeInput()
        pass
    
    
factorySetting = FactorySetting()
factorySetting.draw()