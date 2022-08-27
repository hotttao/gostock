import re
from pykit.protoc_gen_http.autogen import build_path_vars
from pykit.protoc_gen_http.template import trans_path


def test_build_path_vars():
    path = "/helloworld/{name}"
    path_vars = build_path_vars(path)
    print(path_vars)

    pattern = re.compile("(?i){([a-z\.0-9_\s]*)=?([^{}]*)}")
    print(pattern.findall(path))


def test_replace_path():
    print('\n')
    path = "/test/{message.id}/{message.name=messages/*}"
    path_vars = build_path_vars(path)

    new_path, var_trans = trans_path(path, path_vars)
    right = '/test/<message_id>/messages/<path:message_name>'
    print(right)
    print(new_path)
    print(var_trans)
    print(right == new_path)
