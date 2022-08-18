import requests
from typing import Any, Tuple
from flask import Request
from flask import Response
from pykit import errors
from pykit.encoding import encoding
from pykit.errors import Error, UnknownReason


def default_error_encoder(request: Request, response: Response, err: Exception):
    err = errors.from_error(err)
    codec, _ = codec_for_request(request, "Accept")
    # try:
    data = codec.marshal(v=err.to_status())
    response.set_data(data)
    response.status = err.code
    response.mimetype = f'application/{codec.name}'
    return response
    # except Exception:
    # pass
    # w.Header().Set("Content-Type", httputil.ContentType(codec.Name()))
    # w.WriteHeader(int(se.Code))
    # _, _ = w.Write(body)


def codec_for_request(request: Request, name: str) -> Tuple[encoding.Codec, bool]:
    if name == "Content-Type":
        mimetypes = [request.content_type]
    else:
        mimetypes = request.accept_mimetypes

    for accept in mimetypes:
        content_subtype = accept[0].split("/")[1]
        print(content_subtype)
        codec = encoding.get_codec(content_subtype)
        if codec:
            return codec, True
    return encoding.get_codec("json"), False


def default_request_decoder(request) -> Any:
    codec, ok = codec_for_request(request, "Content-Type")
    if not ok:
        return errors.BadRequest("CODEC", request.content_type)

    data = request.body

    v = codec.unmarshal(data)
    return v


def default_response_encoder(request: Request, response: Response, v):
    if not v:
        response.set_data('')
        return response
    try:
        codec, _ = codec_for_request(request, "Accept")
        data = codec.marshal(v)

    except Exception:
        pass

    response.mimetype = f'application/{codec.name}'
    response.set_data(data)

    return response


def codec_for_response(r: requests.Response) -> encoding.Codec:
    # CodecForResponse get encoding.Codec via http.Response
    content_type = r.headers.get('Content-Type')
    content_subtype = content_type.split("/")[1]
    codec = encoding.get_codec(content_subtype)
    if codec:
        return codec

    return encoding.get_codec("json")


# DefaultRequestEncoder is an HTTP request encoder.
def default_request_encoder(content_type: str, req_pb2: Any) -> str:
    content_subtype = content_type.split("/")[1]
    codec = encoding.get_codec(content_subtype)
    body = codec.marshal(req_pb2)
    return body


# DefaultResponseDecoder is an HTTP response decoder.
def default_response_decoder(res: requests.Response) -> Tuple[Any, Error]:
    data = res.text
    codec = codec_for_response(res)
    return codec.unmarshal(data)


# DefaultErrorDecoder is an HTTP error decoder.
def default_error_decoder(res: requests.Response) -> Error:
    if res.status_code >= 200 and res.status_code <= 299:
        return None
    try:
        data = res.text
        codec = codec_for_response(res)
        err = Error.from_dict(codec.unmarshal(data))
        err.code = int(res.status_code)
        return err
    except Exception as e:
        err = Error(code=res.status_code, reason=UnknownReason, message="").with_cause(e)
        return err
