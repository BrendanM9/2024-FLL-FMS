'''
from streaming_form_data import StreamingFormDataParser
from streaming_form_data.targets import ValueTarget, FileTarget, NullTarget
headers = {'Content-Type': 'multipart/form-data; boundary=boundary'}
parser = StreamingFormDataParser(headers=headers)
parser.register('name', ValueTarget())
parser.register('file', FileTarget('/tmp/file.txt'))
parser.register('discard-me', NullTarget())
for chunk in request.body:
    parser.data_received(chunk)
'''