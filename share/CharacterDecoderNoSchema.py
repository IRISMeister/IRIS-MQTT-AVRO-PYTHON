import io
import avro.schema
from avro.io import DatumReader,BinaryDecoder

schema = avro.schema.parse(open("Characters.avsc", "rb").read())

fr = open('Characters.avro', 'rb')
byte_data = fr.read()

bytes_reader = io.BytesIO(byte_data)
decoder = BinaryDecoder(bytes_reader)
reader = DatumReader(schema)
print(len(bytes_reader.getvalue()))

while bytes_reader.tell() < len(bytes_reader.getvalue()):
    data = reader.read(decoder)
    print(data)
    bytes_reader.tell()
