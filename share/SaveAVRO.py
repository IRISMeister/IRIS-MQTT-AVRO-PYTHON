# 既にメンテしていません。実行するにはSaveFastAVRO.pyを参考に修正する必要があります。

import os
import io
import avro.schema
import avro.io
import json

def init(datadir):
	global schema
	global stmt
	schema = avro.schema.parse(open(datadir+'SimpleClass.avsc', 'rb').read())
	import iris
	iris.system.Process.SetNamespace('AVRO')
	sql = "INSERT INTO MQTT.SimpleClass (myArray, myBool, myBytes, myDouble, myFloat, myInt, myLong, myString,seq, topic) VALUES(?,?,?,?,?,?,?,?,?,?)"
	stmt = iris.sql.prepare(sql)

# copy me in mgr\python\
def save(seq,topic,avromsg):
	import iris

	bytes_reader = io.BytesIO(avromsg)
	decoder = avro.io.BinaryDecoder(bytes_reader)
	reader = avro.io.DatumReader(schema)

	while bytes_reader.tell() < len(bytes_reader.getvalue()):
		data = reader.read(decoder)
		try: 
			rs=stmt.execute(json.dumps(data['myArray']),int(data['myBool']),data['myBytes'],data['myDouble'],data['myFloat'],data['myInt'],data['myLong'],data['myString'],seq,topic)
		except Exception as ex:
			if ex.sqlcode != 0:
				print ('SQL error', ex.message, ex.sqlcode, ex.statement)

	return 0

if __name__ == '__main__':
	import platform
	import sys
	import time

	global schema
	args = sys.argv
	pf = platform.system()
	if pf == 'Windows':
		datadir="/share/"
		sys.path += ['c:\\intersystems\\iris\\lib\\python','c:\\intersystems\\iris\\mgr\\python']
	elif pf == 'Linux':
		datadir="/share/"
		sys.path += ['/usr/irissys/lib/python/','/usr/irissys/mgr/python/']

	avrofile=datadir+'compare.avro'
	fr = open(avrofile, 'rb')
	byte_data = fr.read()	
	topic="/XGH/PYAVRO/"
	init(datadir)
	
	start = time.time()

	if 2 <= len(args):
		if args[1].isdigit():
			for seq in range (0,int(args[1])):
				save(seq+1,topic+str(seq+1),byte_data)
	else:
		save(1,topic+'1',byte_data)

	t = time.time() - start
	#print(t)