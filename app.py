from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_compress import Compress
from gevent.pywsgi import WSGIServer
from resources.Comment import Comment
from resources.CommentList import CommentList
from resources.Key import Key
from resources.Rate import Rate
from resources.User import User
from resources.Verification import Verification
from resources.Course import Course
from resources.Plan import Plan
from resources.CommentStatistic import CommentStatistic
from resources.LearntCourse import LearntCourse
from resources.LearntCourseDetail import LearntCourseDetail
from resources.Major import Major
from resources.PluginPlan import PluginPlan
from resources.RegisterLink import RegisterLink

app = Flask(__name__)
app.config['WTF_CSRF_CHECK_DEFAULT'] = False
CORS(app)
Compress(app)
api = Api(app)
resource_list = [Key, User, Rate, Verification, Course, Comment, Plan, CommentList, CommentStatistic, LearntCourse,
                 LearntCourseDetail, Major, PluginPlan, RegisterLink]
for resource in resource_list:
    api.add_resource(resource, f'/{resource.name}')
if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
