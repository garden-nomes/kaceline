from flask import Flask

app = Flask(__name__)
# import placed here to avoid circular references
from app import views