import json

def movie_with_id(_,info,_id):
    """This function return the movie associated with the id _id"""
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie

def update_movie_rate(_,info,_id,_rate):
    """This function update the rate of the movie _id"""
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie

def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        result = [actor for actor in actors['actors'] if movie['id'] in actor['films']]
        return result

def movies_by_title(_,info,_title):
    """This function return the movie with the title _title"""
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['title'] == _title:
                return movie

def add_movie(_,info,movie):
    """This function add a movie to our database"""
    new_movies = {}
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
    movies["movies"].append(movie)
    new_movies = movies
    # json.dump(movies,file) # Regarder si film existe déjà dans la database
    write(new_movies)
    return new_movies["movies"]

def del_a_movie(_,info,_id):
    """This function delete the movie _id of the database"""
    new_movies = {}
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
    for movie in movies["movies"]:
        if movie["id"] == _id:     
            new_movies = movies
            movies["movies"].remove(movie)
            write(movies)
            return movies["movies"]

def movies_sorted_by_rate(_,info):
    """This function return all the movies sorted by decreasing rate"""
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)["movies"]
        sorted_movies = sorted(movies, key=lambda x : x["rating"],reverse=True)
        return sorted_movies

def update_director_movie(_,info,_id,_director):
    """This function update the director of the movie with the id _id"""
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)["movies"]
        for movie in movies:
            if movie["id"] == _id:
                movie["director"] = _director
                write(movies)
                return movie

def write(movies):
    """This function replace the database with the new one"""
    with open('{}/data/movies.json'.format("."), 'w') as f:
        
        json.dump(movies, f)