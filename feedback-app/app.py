import parsing
from flask import Flask
from controller import bp

app = Flask(__name__)
app.register_blueprint(bp)

# try:
#     parsing.add_lecturers_in_table()
#     parsing.add_courses_in_table()
# except:
#     print("Sorry, without parsing today.")

app.run(host='0.0.0.0')
