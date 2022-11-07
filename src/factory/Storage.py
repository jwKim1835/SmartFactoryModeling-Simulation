import simpy

class Storage:
    def __init__(self, env, storageId, maxSize:int, initSize:int):
        self.storageId = storageId
        self.maxSize = maxSize
        self.initSize = initSize
        self.container = simpy.Container(env, capacity = self.maxSize, init = self.initSize)
        
    def get(self, size):
        return self.container.get(size)
    
    def put(self, size):
        return self.container.put(size)
    
    def getStorageId(self):
        return self.storageId
    
    def getSize(self):
        return self.container.level