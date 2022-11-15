import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))                    # import parent directory
import streamlit as st
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
                
                except:
                    st.error(f"ERROR) Only Number Input: %s" % (factoryRunningTime))
                pass
                
    def readFile(self, file):
        if self.csvFileInfo is not None:
            return
        
        loader = CSVFactoryLoader()
        if loader.load( file ):
            self.listFactory = loader.makeFactory()
            self.csvFileInfo = loader.getCSVFileData()

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