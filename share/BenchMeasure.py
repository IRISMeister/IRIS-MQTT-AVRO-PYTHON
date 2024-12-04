import platform
import sys

if __name__ == '__main__':

	pf = platform.system()
	if pf == 'Windows':
		datadir="C:\\git\\IRIS-MQTT-AVRO-PYTHON\\share\\"
		sys.path += ['c:\\intersystems\\iris\\lib\\python','c:\\intersystems\\iris\\mgr\\python', datadir]
	elif pf == 'Linux':
		datadir="/share/"
		sys.path += ['/usr/irissys/lib/python/','/usr/irissys/mgr/python/']

	import iris
	iris.system.Process.SetNamespace('AVRO')
	sql = "SELECT count(*),{fn TIMESTAMPDIFF(SQL_TSI_FRAC_SECOND,MIN(ReceiveTS),MAX(ReceiveTS))} FROM MQTT.SimpleClass"
	stmt = iris.sql.prepare(sql)

	try: 
		rs=stmt.execute()
		for idx, row in enumerate(rs):                                              
			print(f"{row}")   
	except Exception as ex:
		if ex.sqlcode != 0:
			print ('SQL error', ex.message, ex.sqlcode, ex.statement)

