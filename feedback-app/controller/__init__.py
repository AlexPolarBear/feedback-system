from flask import Blueprint

bp = Blueprint('controller', __name__)

from controller import (course_controller, feedback_controller, 
                        lecturer_controller, user_controller, 
                        metric_controller, score_controller)
