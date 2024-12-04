import platform
import sys

if __name__ == '__main__':

	pf = platform.system()
	if pf == 'Windows':
		datadir="C:\\git\\IRIS-MQTT-AVRO-PYTHON\\share\\"
		sys.path += ['c:\\intersystems\\iris\\lib\\python','c:\\intersystems\\iris\\mgr\\python',datadir]
	elif pf == 'Linux':
		sys.path += ['/usr/irissys/lib/python/','/usr/irissys/mgr/python/']

	import iris
	iris.system.Process.SetNamespace('AVRO')
	retcode = iris.cls('MQTT.Dispatcher').Reset()
	if (retcode!=1):
		print("Fatal Error.")
