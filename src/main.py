import simpy
import factory.process
import factory.storage

TOTAL_TIME = 30

env = simpy.Environment()
testProcess = factory.process.process('Test')
testStorage = factory.storage.storage(env, 'Test', 100, 50)
testStorage2 = factory.storage.storage(env, 'Test2', 100, 0)

testProcess.setProcessTime(4)
testProcess.addOldProcessStorage(testStorage.getStorageId(), testStorage, 2)
testProcess.addProcessStorage(testStorage2.getStorageId(), testStorage2, 1)

testRunProcess = env.process(testProcess.run(env))

env.run( TOTAL_TIME )


print( f'%s storage current size: %d' % (testStorage.getStorageId(), testStorage.container.level) )
print( f'%s storage current size: %d' % (testStorage2.getStorageId(), testStorage2.container.level) )