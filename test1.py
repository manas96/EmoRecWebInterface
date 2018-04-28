from multiprocessing import Process, Queue
from faceRecog import realtime_plot

inputCamera = 0
farmeSkip = 10



faceRecogData = Queue()
faceRecogProcess = Process(target=realtime_plot.run, args=(inputCamera,farmeSkip,faceRecogData,))
faceRecogProcess.start()


while(True):
	print('********************************' + 	str(faceRecogData.get(True)))
