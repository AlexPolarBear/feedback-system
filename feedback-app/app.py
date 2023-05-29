from flask import Flask
from controller import bp

app = Flask(__name__)
app.register_blueprint(bp)

app.run(host='0.0.0.0')
