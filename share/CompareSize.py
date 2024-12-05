import io
import sys
import avro.schema
import avro.io
import json
import base64
import random

record_count=1 #単一ファイルに含めるレコードの数
args = sys.argv
if 2 <= len(args):
  if args[1].isdigit():
    record_count=int(args[1])
                    
schema = avro.schema.parse(open('SimpleClass.avsc', 'rb').read())

writer = avro.io.DatumWriter(schema)
bytes_writer = io.BytesIO()
encoder = avro.io.BinaryEncoder(bytes_writer)

arraysize=100
myBytes = bytes(range(0, arraysize))

rondom_list1 = []

for k in range(arraysize):
  x = random.random()
  rondom_list1.append(x)

data = {'myInt': 1, 'myLong': 2, 'myBool': True, 'myDouble': 3.14, 'myFloat': 0.01590000092983246, 'myBytes': myBytes , 'myFilename': 'data.hex', 'myString': 'this is a 1st SimpleClass', 'myArray': rondom_list1}
writer.write(data,encoder)

raw_bytes = bytes_writer.getvalue()

f = open('compare.avro', 'wb')
for k in range(record_count):
  f.write(raw_bytes)
f.close()

data['myBytes']=base64.b64encode(data['myBytes']).decode('ascii')
with open('compare.json', 'w') as f:
    f.write('[')
    for k in range(record_count):
       json.dump(data,f)
       if k!=(record_count-1): f.write(',')
    f.write(']')

