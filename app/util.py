import mimetypes

one_kb_bytes = 1024
one_mb_kbs = 1024
one_mb_bytes = one_mb_kbs * one_kb_bytes
json_mime_type = mimetypes.types_map['.json']
form_data_mime_type = 'multipart/form-data'
txt_mime_type = mimetypes.types_map['.txt']