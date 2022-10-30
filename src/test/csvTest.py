import os
import sys
import csv
import simpy
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))                    # import parent directory
from factory.loader.CSVFactoryLoader import CSVFactoryLoader

from factory.Factory import Factory

env = simpy.Environment()

loader = CSVFactoryLoader(env)
if loader.load( "resource/sample.csv " ):
    listFactory = loader.makeFactory()
    
    try:
        for factory in listFactory:
            time = int(input(f"Input Factory[%s] Time: " % factory.name))
            factory.runProcess(time)
        
        for factory in listFactory:
            factory.printStorageInfo()
    except ValueError as err:
        print( "입력이 잘못 되었습니다.", err)