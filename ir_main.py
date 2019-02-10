import sys
from common import commonPages
from flask import Flask, session
from flask_session import Session


#-----------------Initialization---------------------------------
app = Flask(__name__)
app.secret_key = "316tiantuan"
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SESSION_TYPE'] = 'filesystem'
#waiting to be changed to suit firebase
Session(app)

#ssl_context = ('./ssl/server.crt', './ssl/server.key')

#-----------------Page Registration---------------------------------
app.register_blueprint(commonPages)
#-----------------Running---------------------------------
#app.run(host = "0.0.0.0", port = 8080, debug = True, threaded = True, ssl_context=ssl_context)
app.run(host = "0.0.0.0", port = 8080, debug = True, threaded = True)
