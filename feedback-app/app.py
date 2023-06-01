from flask import Flask
from controller import bp
from logging.config import dictConfig

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
                'filename': './feedback-system/feedback-app/logs.log',
                'formatter': 'default',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
})

app = Flask(__name__)
app.register_blueprint(bp)

app.run(host='0.0.0.0')
