from flask import Flask
#from flask_cors import CORS
import views

def create_app():
    app = Flask(__name__)
    #CORS(app)
    views.configure(app)
    return app
