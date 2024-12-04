from avro.datafile import DataFileReader
from avro.io import DatumReader

reader = DataFileReader(open("Binary.avro", "rb"), DatumReader())
for user in reader:    
    print (user)

reader.close()

