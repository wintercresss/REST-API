from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)



class SongModel(db.Model):
    song_id = db.Column(db.Integer, primary_key=True) # primary key to ensure unique identifier for the song
    song_name = db.Column(db.String(100))
    artist_name = db.Column(db.String(100))
    release_year = db.Column(db.Integer)
    album_name = db.Column(db.String(100))
    streams = db.Column(db.Integer)

db.create_all()

song_post_args = reqparse.RequestParser()
song_post_args.add_argument("song_name", type=str)
song_post_args.add_argument("artist_name", type=str)
song_post_args.add_argument("release_year", type=int)
song_post_args.add_argument("album_name", type=str)


add_streams_args = reqparse.RequestParser()
add_streams_args.add_argument("streams", type=int)


resource_fields = {
    'song_id': fields.Integer,
    'song_name': fields.String,
    'artist_name': fields.String,
    'release_year': fields.Integer,
    'album_name': fields.String,
    'streams': fields.Integer
}



class Song(Resource):
    @marshal_with(resource_fields)
    def get(self, song_id): # gets the information about the song given the song ID
        result = SongModel.query.filter_by(song_id=song_id).first()

        if not result: # error message if song isn't in the database
            abort(404, message="song doesn't exist")

        return result
    
    @marshal_with(resource_fields)
    def post(self, song_id): # adds new song to the database
        args = song_post_args.parse_args()

        song = SongModel(song_id=song_id, song_name=args['song_name'], artist_name=args['artist_name'], release_year=args['release_year'], album_name=args['album_name'],
                        streams=0)

        db.session.add(song)
        db.session.commit()
        return song
    

    def delete(self, song_id): # deletes song from database
        result = SongModel.query.filter_by(song_id=song_id).first()
        if not result: # if the song isn't in the database
            abort(404, message="Can't find the song")
        
        db.session.delete(result)
        db.session.commit()
        return f"deleted song: {result.song_name} by {result.artist_name}"


    def patch(self, song_id): # increases the number of streams for song
        result = SongModel.query.filter_by(song_id=song_id).first()
        if not result:
            abort(404, message="Can't find the song")

        newstreams = add_streams_args.parse_args()
        newstream_amount = newstreams['streams']

        result.streams += newstream_amount
        db.session.commit()
        return f'streams increased by {newstream_amount}! New stream count for {result.song_name} is {result.streams}'



api.add_resource(Song, "/song/<int:song_id>")

if __name__ == "__main__":
    app.run(debug=True)