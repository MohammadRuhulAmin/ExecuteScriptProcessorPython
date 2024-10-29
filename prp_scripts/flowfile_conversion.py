from org.apache.nifi.processor.io import StreamCallback
from java.io import BufferedReader, InputStreamReader, OutputStreamWriter
import json
from datetime import datetime 

class SimpleStreamCallback(StreamCallback):
    def date_conversion(self, time_in_ms):
        return datetime.fromtimestamp(time_in_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
    
    def process(self, inputStream, outputStream):
        content = BufferedReader(InputStreamReader(inputStream, "UTF-8")).readLine()
        data = json.loads(content)
        if 'created' in data:data['created'] = self.date_conversion(data['created'])
        output_content = json.dumps(data)
        writer = OutputStreamWriter(outputStream, "UTF-8")
        writer.write(output_content)
        writer.flush()
        writer.close()
flowfile = session.get()
if flowfile is not None:
    flowfile = session.write(flowfile, SimpleStreamCallback())
    session.transfer(flowfile, REL_SUCCESS)
