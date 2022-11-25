import simpy

class Storage:
    def __init__(self, env, storageId, maxSize:int, initSize:int):
        self.storageId = storageId
        self.maxSize = maxSize
        self.initSize = initSize
        self.container = simpy.Container(env, capacity = self.maxSize, init = self.initSize)
        
    def get(self, size):
        """ 저장소 데이터 반환

        Args:
            size (int): 반환 값

        Returns:
            int: 현재 저장소 값
        """
        return self.container.get(size)
    
    def put(self, size):
        """ 저장소 데이터 입력

        Args:
            size (int): 입력 값

        Returns:
            int: 현재 저장소 값
        """
        return self.container.put(size)
    
    def getStorageId(self):
        """ 저장소 ID

        Returns:
            str: 저장소 ID
        """
        return self.storageId
    
    def getSize(self):
        """ 현재 저장소 Size 반환

        Returns:
            int: 저장소 Level
        """
        return self.container.level