import re
from pykit.protoc_gen_http.autogen import build_path_vars
from pykit.protoc_gen_http.autogen import replace_path


def test_build_path_vars():
    path = "/helloworld/{name}"
    path_vars = build_path_vars(path)
    print(path_vars)

    pattern = re.compile("(?i){([a-z\.0-9_\s]*)=?([^{}]*)}")
    print(pattern.findall(path))


def test_replace_path():
    path = "/test/{message.id}/{message.name=messages/*}"
    new_path = replace_path("message.name", "messages/*", path)
    right = '/test/{message.id}/{message.name:messages/.*}'
    print(right)
    print(new_path)
    print(right == new_path)