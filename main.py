from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

song_post_args = reqparse.RequestParser()
song_post_args.add_argument("name", type=str)
song_post_args.add_argument("artist", type=str)
song_post_args.add_argument("release_year", type=int)

allsongs = {}

class Song(Resource):
    def get(self, song_id):
        if song_id not in allsongs:
            abort(404, message="song doesn't exist")
        return allsongs[song_id]
    
    def post(self, song_id):
        args = song_post_args.parse_args() # 

        allsongs[song_id] = args
        return allsongs[song_id]
    
    def delete(self, song_id):
        if song_id not in allsongs:
            abort(404, message="can't find the song")
        
        else:
            del allsongs[song_id]
            return f'successfully deleted song_id: {song_id}'



api.add_resource(Song, "/song/<int:song_id>")

if __name__ == "__main__":
    app.run(debug=True)