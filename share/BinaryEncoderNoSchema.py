import io
import avro.schema
from avro.io import DatumWriter,BinaryEncoder

schema = avro.schema.parse(open("Binary.avsc", "rb").read())

writer = DatumWriter(schema)
bytes_writer = io.BytesIO()
encoder = BinaryEncoder(bytes_writer)

arraysize=10
int_list = []
for k in range(arraysize):
  int_list.append(k)
data = {'myArray': int_list}

writer.write(data,encoder)

raw_bytes = bytes_writer.getvalue()

f = open('BinaryNoSchema.avro', 'wb')
f.write(raw_bytes)
f.close()
