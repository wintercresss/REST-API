from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

class Song(Resource):
    def get(self):
        return {"song": "welcome to new york"}
    



api.add_resource(Song, "/song")

if __name__ == "__main__":
    app.run(debug=True)