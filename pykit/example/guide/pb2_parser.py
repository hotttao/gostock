import pandas
from helloworld_pb2 import DESCRIPTOR
from google.protobuf import reflection
from google.protobuf.descriptor import FieldDescriptor

pandas.set_option('display.max_rows', None)

message = DESCRIPTOR.message_types_by_name['HelloRequest']

# print(dir(message))
# print(dir(message.fields))


def get_attrs(obj):
    m = {"attr": [], "value": []}
    for i in dir(obj):
        if i.startswith('__'):
            continue
        try:
            attr = getattr(obj, i)
        except:
            print(f'----- {i} ---------')
            continue
        if callable(attr):
            k = f"call({i})"
            try:
                v = attr()
            except:
                v = 'need param'
        else:
            k = f"attr({i})"
            v = attr
        m["attr"].append(k)
        m["value"].append(v)
        # print(m)
    return pandas.DataFrame(m)


df_inner = get_attrs(message.fields_by_name['inner'].message_type)
df_metadata = get_attrs(message.fields_by_name['metadata'].message_type)
df = pandas.merge(df_inner, df_metadata, on=['attr'], suffixes=['_inner', "_meta"])
print(df)

df_inner = get_attrs(message.fields_by_name['inner'])
df_metadata = get_attrs(message.fields_by_name['metadata'])
df = pandas.merge(df_inner, df_metadata, on=['attr'], suffixes=['_inner', "_meta"])
print(df)