import avro.schema
from avro.datafile import DataFileWriter
from avro.io import DatumWriter
schema = avro.schema.parse(open("Binary.avsc", "rb").read())

writer = DataFileWriter(open("Binary.avro", "wb"), DatumWriter(), schema)

arraysize=10
myBytes = bytes(range(0, arraysize))
bytes_list1 = []
for k in range(arraysize):
  bytes_list1.append(k)
data = {'myArray': bytes_list1}

writer.append(data)
writer.close()
