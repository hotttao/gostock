
from helloworld_pb2 import DESCRIPTOR
from google.protobuf import reflection
from google.protobuf.descriptor import FieldDescriptor

reflection

message = DESCRIPTOR.message_types_by_name['HelloRequest']

print(dir(message))
print(dir(message.fields))
print("============ inner  message ===========")
print(dir(message.fields_by_name['inner']))
print(message.fields_by_name['inner'].type)
print(message.fields_by_name['inner'].message_type)
print(FieldDescriptor.TYPE_MESSAGE)

print("============ maps  map ===========")
print(dir(message.fields_by_name['maps']))
print(message.fields_by_name['maps'].type)
print(message.fields_by_name['maps'].message_type)
print(FieldDescriptor.TYPE_MESSAGE)

print("============ nums  list ===========")
print(dir(message.fields_by_name['nums']))
print(message.fields_by_name['nums'].type)
print(message.fields_by_name['nums'].message_type)
print(FieldDescriptor.TYPE_MESSAGE)