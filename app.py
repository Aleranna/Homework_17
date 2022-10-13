from flask import request
from flask_restx import Api, Resource
from config import app, db
from models import Movie, Director, Genre
from schemas import MovieSchema, DirectorSchema, GenreSchema

api = Api(app)

movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genres_ns = api.namespace('genres')

movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()
#directors_schema = DirectorSchema(many=True)
#director_schema = DirectorSchema()
#genres_schema = GenreSchema(many=True)
#genre_schema = GenreSchema()


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        page = request.args.get('page')
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        movies = Movie.query
        if page:
            movies = movies.paginate(int(page), 3).items
        if director_id:
            movies = movies.filter(Movie.director_id == director_id).all()
        if genre_id:
            movies = movies.filter(Movie.genre_id == genre_id).all()
        if director_id and genre_id:
            movies = movies.filter(Movie.director_id == director_id, Movie.genre_id == genre_id).all()
        all_movies = movies_schema.dump(movies)
        return all_movies, 200


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        movie = Movie.query.get(mid)
        if not movie:
            return 'Not Found', 404
        return movie_schema.dump(movie), 200


@director_ns.route('/')
class DirectorsView(Resource):
    def post(self):
        req_json = request.json
        try:
            new_director = Director(**req_json)
            with db.session.begin():
                db.session.add(new_director)
                return 'New info added', 201
        except Exception as e:
            print(e)


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def put(self, did):
        req_json = request.json
        try:
            director = Director.query.get(did)
            director.name = req_json.get('name')
            db.session.add(director)
            db.session.commit()
            return 'info updated', 204
        except Exception as e:
            print(e)

    def delete(self, did):
        try:
            director = Director.query.get(did)
            db.session.delete(director)
            db.session.commit()
            return 'info deleted', 204
        except Exception as e:
            print(e)


@genres_ns.route('/')
class GenresView(Resource):
    def post(self):
        req_json = request.json
        try:
            new_genre = Genre(**req_json)
            with db.session.begin():
                db.session.add(new_genre)
                return 'New info added', 201
        except Exception as e:
            print(e)


@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    def put(self, gid):
        req_json = request.json
        try:
            genre = Genre.query.get(gid)
            genre.name = req_json.get('name')
            db.session.add(genre)
            db.session.commit()
            return 'info updated', 204
        except Exception as e:
            print(e)

    def delete(self, gid):
        try:
            genre = Genre.query.get(gid)
            db.session.delete(genre)
            db.session.commit()
            return 'info deleted', 204
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app.run(debug=True)


