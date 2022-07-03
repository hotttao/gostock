

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

# def DefaultErrorEncoder(w http.ResponseWriter, r *http.Request, err error) {
# 	se := errors.FromError(err)
# 	codec, _ := CodecForRequest(r, "Accept")
# 	body, err := codec.Marshal(se)
# 	if err != nil {
# 		w.WriteHeader(http.StatusInternalServerError)
# 		return
# 	}
# 	w.Header().Set("Content-Type", httputil.ContentType(codec.Name()))
# 	w.WriteHeader(int(se.Code))
# 	_, _ = w.Write(body)
# }

# def codec_for_request(request, name string) (encoding.Codec, bool) {
# 	for _, accept := range r.Header[name] {
# 		codec := encoding.GetCodec(httputil.ContentSubtype(accept))
# 		if codec != nil {
# 			return codec, true
# 		}
# 	}
# 	return encoding.GetCodec("json"), false
# }
