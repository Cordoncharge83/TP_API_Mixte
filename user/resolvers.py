import json
import requests
import grpc
import booking_pb2
import booking_pb2_grpc
from google.protobuf.json_format import MessageToDict
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

def get_movies_by_id(_id): 
    """This function gives the movie associated at the id _id"""
    req = requests.request("POST", MOVIE_PATH +"/graphql",json={"query":
f"""
{{
    movie_with_id(_id: "{_id}") {{
        id
        title
        director
        rating
    }}
}}
"""})
    if req.status_code == 200:
      data = json.loads(req.content.decode('utf_8'))
      return data["data"]["movie_with_id"]

def get_movies_available_at_date(_,info,_date):
    """This method returns all movies available at a chosen date request.date"""
    with grpc.insecure_channel(BOOKING_PATH) as channel:
            print("Channel loaded")
            stub = booking_pb2_grpc.BookingStub(channel)
            date = booking_pb2.DateB(date= _date)
            bookings = stub.GetMovieAtDate(date)
            # We get all the ids, now we need the other parameters
            res = MessageToDict(bookings)
            list_movies = []
            for id in res["movies"]:
                list_movies.append(get_movies_by_id(id))
    return list_movies

def get_booking_made(_,info,_userid):
    """This method returns the bookings made by the user request.id"""
    with grpc.insecure_channel(BOOKING_PATH) as channel:
            print("Channel loaded")
            stub = booking_pb2_grpc.BookingStub(channel)
            userid = booking_pb2.UserId(id = _userid)
            print("-------------- GetBookingForUser --------------")
            bookings = stub.GetBookingForUser(userid)
            res=  MessageToDict(bookings)
            print("res : ", res)
    return res


def book_the_movie(_,info,_userid,_date,_movieid):
   """This method allows the user to book a movie session"""
   with grpc.insecure_channel(BOOKING_PATH) as channel:
            stub = booking_pb2_grpc.BookingStub(channel)
                
            # Create the EntryAddBooking message
            booking_request = booking_pb2.EntryAddBooking(
            user_id=booking_pb2.UserId(id=_userid),
            new_movie=booking_pb2.NewMovie(
                        date=_date,
                        movieid=_movieid
                    )
                )
                
            bookings = stub.AddBookingByUser(booking_request)
            result =  MessageToDict(bookings)
        
            
            return result