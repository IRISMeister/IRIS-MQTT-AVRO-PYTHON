import io
import json
import time
import fastavro

def init(datadir):
	global schema
	global stmt
	# global decodeTime
	# for fastavro

	# 実装上、スキーマのパースを毎回繰り返すようなことは恐らくしないので、経過時間の対象から除外する
	# start = time.time()
	schema = json.loads(open(datadir+'SimpleClass.avsc', 'r').read()) 
	schema = fastavro.parse_schema(schema)
	#t = time.time() - start
	#decodeTime=decodeTime+t

	# 注意) import irisはカレントを'/usr/irissys/mgr/user'に移動させる
	import iris
	iris.system.Process.SetNamespace('AVRO')
	sql = "INSERT INTO MQTT.SimpleClass (myArray, myBool, myBytes, myDouble, myFloat, myInt, myLong, myString,seq, topic) VALUES(?,?,?,?,?,?,?,?,?,?)"
	stmt = iris.sql.prepare(sql)

def saveFromString(seq,topic,byte_data):
	import iris
	bytes_reader = io.BytesIO(byte_data)
	data = fastavro.schemaless_reader(bytes_reader, schema)

	try: 
		rs=stmt.execute(json.dumps(data['myArray']),int(data['myBool']),data['myBytes'],data['myDouble'],data['myFloat'],data['myInt'],data['myLong'],data['myString'],seq,topic)
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
	avrofile=datadir+'compare.avro'
	fr = open(avrofile, 'rb')
	byte_data = fr.read()	

	bytes_reader = io.BytesIO(byte_data)
	data = fastavro.schemaless_reader(bytes_reader, schema)
	t = time.time() - start
	decodeTime=decodeTime+t

	start = time.time()
	try: 
		rs=stmt.execute(json.dumps(data['myArray']),int(data['myBool']),data['myBytes'],data['myDouble'],data['myFloat'],data['myInt'],data['myLong'],data['myString'],seq,topic)
	except Exception as ex:
		if ex.sqlcode != 0:
			print ('SQL error', ex.message, ex.sqlcode, ex.statement)
	t = time.time() - start
	sqlTime=sqlTime+t

	return 0

if __name__ == '__main__':
	import platform
	import sys

	global schema
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
		# /usr/irissys/lib/python/ ... enables import iris
		sys.path += ['/usr/irissys/lib/python/',datadir]

	topic="/XGH/PYAVRO/"
	init(datadir)

	if 2 <= len(args):
		if args[1].isdigit():
			for seq in range (0,int(args[1])):
				save(seq+1,topic+str(seq+1),datadir)
	else:
		save(1,topic+'1',datadir)

	print([decodeTime,sqlTime,decodeTime+sqlTime])
