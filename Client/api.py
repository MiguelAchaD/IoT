from flask import Flask
from flask_restful import Resource, Api
import sys

# Custom libraries imports
#sys.path.append("/modules")
#import accelerometer

app = Flask(__name__)
api = Api(app)
port = 5000

if sys.argv.__len__() > 1:
    port = sys.argv[1]
print(f"Api running on port : {port} ")

class topic_tags(Resource):
    def get(self):
        return {'hello': 'world world'}

api.add_resource(topic_tags, '/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)