
from typing import Tuple
from pykit import errors
from pykit.transport import http
from pykit import encoding


def default_error_encoder(ctx: http.Context, err: Exception):
    err = errors.from_error(err)
    codec, _ = codec_for_request(ctx, "Accept")
    try:
        return codec.marshal(err.to_status()), err.code
    except Exception:
        pass
    # w.Header().Set("Content-Type", httputil.ContentType(codec.Name()))
    # w.WriteHeader(int(se.Code))
    # _, _ = w.Write(body)


def codec_for_request(ctx: http.Context, name: str) -> Tuple[encoding.Codec, bool]:
    for accept in ctx.headers.getlist('Accept'):
        print(accept)
        # codec = encoding.GetCodec(httputil.ContentSubtype(accept))
        # if codec:
        #     return codec, True
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

# def DefaultResponseEncoder(request) {
# 	if v == nil {
# 		_, err := w.Write(nil)
# 		return err
# 	}
# 	codec, _ := CodecForRequest(r, "Accept")
# 	data, err := codec.Marshal(v)
# 	if err != nil {
# 		return err
# 	}
# 	w.Header().Set("Content-Type", httputil.ContentType(codec.Name()))
# 	_, err = w.Write(data)
# 	if err != nil {
# 		return err
# 	}
# 	return nil
# }
