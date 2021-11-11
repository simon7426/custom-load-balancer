import os
from flask import Flask,jsonify,request
app = Flask(__name__)

@app.route('/')
def sample():
    return jsonify(
        message=f'This is the {os.environ["APP"]} application',
        server=request.base_url,
        custom_header=request.headers.get('MyCustomHeader',None),
        host_header=request.headers.get('Host',request.base_url)
    )
    # return f'This is the {os.environ["APP"]} application'

@app.route('/healthcheck')
def healthcheck():
    return 'OK'

if __name__=='__main__':
    app.run(host='0.0.0.0')
