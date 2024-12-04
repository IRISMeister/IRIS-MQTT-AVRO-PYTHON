import json
import time
import base64

def init():
	global stmt
	import iris
	iris.system.Process.SetNamespace('AVRO')
	sql = "INSERT INTO MQTT.SimpleClass (myArray, myBool, myBytes, myDouble, myFloat, myInt, myLong, myString,seq, topic) VALUES(?,?,?,?,?,?,?,?,?,?)"
	stmt = iris.sql.prepare(sql)

def saveFromString(seq,topic,byte_data):
	import iris

	json_str = byte_data.decode('utf-8')
	data = json.loads(json_str)

	myBytes=base64.b64decode(data['myBytes']).decode('utf-8')

	try: 
		rs=stmt.execute(json.dumps(data['myArray']),int(data['myBool']),myBytes,data['myDouble'],data['myFloat'],data['myInt'],data['myLong'],data['myString'],seq,topic)
	except Exception as ex:
		if ex.sqlcode != 0:
			print ('SQL error', ex.message, ex.sqlcode, ex.statement)

	return 0

# copy me in mgr\python\
def save(seq,topic,datadir):
	global decodeTime
	global sqlTime
	import iris

	start = time.time()
	jsonfile=datadir+'compare.json'
	fr = open(jsonfile, 'rb')
	byte_data = fr.read()

	json_str = byte_data.decode('utf-8')
	data = json.loads(json_str)

	myBytes=base64.b64decode(data['myBytes']).decode('utf-8')
	t = time.time() - start
	decodeTime=decodeTime+t

	start = time.time()
	try: 
		rs=stmt.execute(json.dumps(data['myArray']),int(data['myBool']),myBytes,data['myDouble'],data['myFloat'],data['myInt'],data['myLong'],data['myString'],seq,topic)
	except Exception as ex:
		if ex.sqlcode != 0:
			print ('SQL error', ex.message, ex.sqlcode, ex.statement)
	t = time.time() - start
	sqlTime=sqlTime+t

	return 0

if __name__ == '__main__':
	import platform
	import sys

	global decodeTime
	global sqlTime

	decodeTime=0
	sqlTime=0

	args = sys.argv
	pf = platform.system()
	if pf == 'Windows':
		datadir="C:\\git\\IRIS-MQTT-AVRO-PYTHON\\share\\"
		sys.path += ['c:\\intersystems\\iris\\lib\\python','c:\\intersystems\\iris\\mgr\\python',datadir]
	elif pf == 'Linux':
		datadir="/share/"
		sys.path += ['/usr/irissys/lib/python/',datadir]

	topic="/XGH/PYJSON/"
	init()

	if 2 <= len(args):
		if args[1].isdigit():
			for seq in range (0,int(args[1])):
				save(seq+1,topic+str(seq+1),datadir)
	else:
		save(1,topic+'1',datadir)

	print([decodeTime,sqlTime,decodeTime+sqlTime])
