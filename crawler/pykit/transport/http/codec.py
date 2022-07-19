
from typing import Tuple
from flask import Request
from flask import Response
from pykit import errors
from pykit.encoding import encoding


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
    accept_mimetypes = request.accept_mimetypes

    for accept in accept_mimetypes:
        content_subtype = accept[0].split("/")[1]
        # print(content_subtype)
        codec = encoding.get_codec(content_subtype)
        if codec:
            return codec, True
    return encoding.get_codec("json"), False

# def DefaultRequestDecoder(request) {
# 	codec, ok := CodecForRequest(r, "Content-Type")
# 	if !ok {
# 		return errors.BadRequest("CODEC", r.Header.Get("Content-Type"))
# 	}
# 	data, err := io.ReadAll(r.Body)
# 	if err != nil {
# 		return errors.BadRequest("CODEC", err.Error())
# 	}
# 	if len(data) == 0 {
# 		return nil
# 	}
# 	if err = codec.Unmarshal(data, v); err != nil {
# 		return errors.BadRequest("CODEC", err.Error())
# 	}
# 	return nil
# }


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
