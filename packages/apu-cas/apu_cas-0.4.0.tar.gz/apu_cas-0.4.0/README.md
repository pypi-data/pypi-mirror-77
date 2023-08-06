This is a library for Flask for developers from Centre of Technology and Innovation (CTI) from Asia Pacific University
to be able to simply implement CAS (Central Authentication Service) by annotating their view functions with the
decorators provided in this library.

## Quickstart
```
from flask import Flask
from apu_cas import require_service_ticket 
app = Flask(__name__)

@app.route('/')
@require_service_ticket
def hello_world():
    return 'Hello, World!'
```

This will secure the endpoints with CAS Authentication and consumer of the secured endpoints will have to pass a valid string
of service ticket through as query parameter, 'ticket'.

For example:
```
GET http://localhost:5000?ticket="ST-575303-I0RYRmVuzlRb4cCkD6jYyw3ISV8ip-172-32-13-200"
```

The above method is related to CAS REST Protocol, for more information such as how to authenticate with CAS REST protocol,
please visit the [documentation](https://apereo.github.io/cas/5.3.x/protocol/REST-Protocol.html)
