import json
import requests

MOVIE_PATH = "http://localhost:3001"
BOOKING_PATH = "http://localhost:3002"

with open('{}/data/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

body_movies_per_rating = """{
    movies_sorted_by_rate {
        id
        title
        director
        rating
    }
}"""
def get_movies_per_ratings(_,info):
   """This function will get all the movies available sorted by rating"""
   req = requests.request("POST", MOVIE_PATH +"/graphql",json={"query": body_movies_per_rating})
   if req.status_code == 200:
      data = json.loads(req.content.decode('utf_8'))
      list_movies = data["data"]['movies_sorted_by_rate']
      return list_movies


# def get_movies_available_at_date(_,info,date):   
#    """This function shows what are the movies (their name) available at the date date"""
#    # We get the ids of the movies available
#    req = requests.request("GET", BOOKING_PATH + f"/movies_at_the_date/{date}")
#    if req.status_code==200:
#       list_name = []
#       for movieid in req.json()["movies"]:
#          list_name.append(movieid)
#       print(list_name)
#       return(list_name)
   
# def book_the_movie(): 
#    ## TO DO : Voir si ça marche si l'utilisateur n'est pas dans la base de données initialisement 
#    if request.args:
#       """This function books the movie name moviename for the user username"""
#       # We get the informations we want
#       request_json = request.get_json()
#       moviename, date, username = request_json["moviename"], request_json["date"],request_json["username"]
#       # We need to convert the moviename into a movie_id
#       req = requests.request("GET", MOVIE_PATH + "/movieid_linked_movietitle")
#       if req.status_code == 200:
#          dict_id_to_name = req.json()
#          # We seek the id corresponding to the title moviename
#          for key in dict_id_to_name.keys():
#             if moviename == dict_id_to_name[key]:
#                # The id of the movie is key
#                new_movie = {"date":date,"movieid":key}
#                req2 = requests.request("POST",BOOKING_PATH + f"/bookings/{convert_username_id(username)}",
#                                        params=new_movie)
#                if req2.status_code==200:
#                   return make_response(render_template('booking_made.html',bodytext=moviename,username=username),200)
#                else: 
#                   return make_response({"message":"We couldn't book the date, Sadge :'("},205)
#       return make_response({"error": "Bad argument"},400)
#    return make_response({"error":"Bad argument"},400)