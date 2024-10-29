# Apache Nifi ExecuteScript Process Py Script

Experimental - Executes a script given the flow file and a process session. The script is responsible for handling the incoming flow file (transfer to SUCCESS or remove, e.g.) 
as well as any flow files created by the script. If the handling is incomplete or incorrect, 
the session will be rolled back. Experimental: Impact of sustained usage not yet verified.


Simple PY Script for convertion of a flowfile json object :

```python

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


```
