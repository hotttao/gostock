import pandas


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
