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
        if self.csvFileInfo is not None:
            st.dataframe(self.csvFileInfo)
                
    def readFile(self, file):
        loader = CSVFactoryLoader()
        if loader.load( file ):
            self.listFactory = loader.makeFactory()
            self.csvFileInfo = loader.getCSVFileData()

    def draw(self):
        st.markdown("# Factory Settings")
        self.drawFileUploader()
        self.drawSampleFileCheckBox()
        self.drawDataFrame()
        pass
    
    
factorySetting = FactorySetting()
factorySetting.draw()