import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))                    # import parent directory
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from factory.loader.CSVFactoryLoader import CSVFactoryLoader
from factory import Factory

class FactorySetting:
    def __init__(self):
        self.csvFileInfo = None
        self.listFactory = None
    
    def drawFileUploader(self):
        uploadFile = st.file_uploader("CSV File ONLY", type=".csv")
        if uploadFile is not None:
            self.readFile(uploadFile)
            
    def drawSampleFileCheckBox(self):
        if self.csvFileInfo is not None:
            return
        
        # isUseSampleFile = st.checkbox("Use Sample Data")
        if st.checkbox("Use Sample Data", value=False) == True:
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
                        
                except Exception as e:
                    st.error(f"ERROR) Only Number Input: %s" % (factoryRunningTime))
                    
        if submitted:
            with st.expander("Storage Info"):
                self.drawStorageDataInfo()
                
            with st.expander("Process Info"):
                self.drawDefectDataInfo()
    
    def drawStorageDataInfo(self):
        
        st.header("Storage Data")
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
        figure = px.bar(storageFrame, x="Factory", y=listStorageName, barmode="group")
            
        st.plotly_chart(figure)
        
    def drawDefectDataInfo(self):
        listFactoryName = []
        mapFactory = dict[str,]()
        COL_MAX = 2
        st.header("Process Data")
        
        for factory in self.listFactory:
            listFactoryName.append(factory.getFactoryName())
            mapFactory[factory.getFactoryName()] = factory
        
        processTabs = st.tabs(listFactoryName)
        
        for index in range(listFactoryName.__len__()):
            with processTabs[index]:
                col = None
                st.subheader(listFactoryName[index])
                colIndex = 0
                factoryProcessData = mapFactory[listFactoryName[index]].getProcessData()
            
                for processName, processData in factoryProcessData.items():
                    if colIndex % COL_MAX == 0:
                        colIndex = 0
                        col = st.columns(COL_MAX)
                    
                    with col[colIndex]:
                        # Sample 1
                        # fig1, ax = plt.subplots()
                        # ax.pie(processData["Value"], labels=processData["Type"], shadow=True, autopct='%d%%')
                        # st.pyplot(fig1)
                        
                        # Sample 2
                        st.caption(processName)
                        figure = px.sunburst(
                            processData,
                            names='Type',
                            # parents=list("" for i in range(processData["Type"].__len__())),
                            parents='Parent',
                            values='Value',
                        )
                        figure.update_layout(
                            autosize=False,
                            width=512)
                        
                        # Sample 3
                        # data = dict(
                        #     character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
                        #     parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
                        #     value=[10, 14, 12, 10, 2, 6, 6, 4, 4])

                        # figure = px.sunburst(
                        #     data,
                        #     names='character',
                        #     parents='parent',
                        #     values='value',
                        # )
                        st.plotly_chart(figure)
                        
                    colIndex += 1
        
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
    
st.set_page_config(layout="wide") 
factorySetting = FactorySetting()
factorySetting.draw()