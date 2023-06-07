from flask import Flask, render_template, send_from_directory
from controller import bp
from logging.config import dictConfig
# from apiflask import APIFlask

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            'datefmt': '%B %d, %Y %H:%M:%S',
        }
    },
    'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                "stream": "ext://sys.stdout",
                'formatter': 'default',
        },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': './logs.log',
                'formatter': 'default',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
})

# app = APIFlask(__name__, spec_path='/')
app = Flask(__name__)
# app.config['OPENAPI_SWAGGER_UI_PATH'] = 'openapi.yaml'
app.register_blueprint(bp)


@app.route('/')
def swagger_ui():
    return render_template('swagger_ui.html')


@app.route('/spec')
def get_spec():
    return send_from_directory(app.root_path, 'openapi.yaml')

app.run(host='0.0.0.0')
