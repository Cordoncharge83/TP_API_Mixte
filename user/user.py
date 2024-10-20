from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from flask import Flask, request, jsonify,make_response

from google.protobuf.json_format import MessageToDict, MessageToJson
import resolvers as r
import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import user_pb2
import user_pb2_grpc
import json
import requests
# CALLING GraphQL requests
type_defs = load_schema_from_path('user.graphql')
query = QueryType()
movie = ObjectType('Movie')
actor = ObjectType('Actor')
query.set_field('get_movies_per_rating', r.get_movies_per_ratings)
#query.set_field('get_movies_available_at_date', r.get_movies_available_at_date)

schema = make_executable_schema(type_defs, movie, query)

app = Flask(__name__)

PORT = 3004
HOST = '0.0.0.0'

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the User service!</h1>",200)

# graphql entry points
@app.route('/graphql', methods=['POST'])
def graphql_server():
    # todo to complete
    data = request.get_json()
    success, result = graphql_sync(
                        schema,
                        data,
                        context_value=None,
                        debug=app.debug
                    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

class UserServicer (user_pb2_grpc.UserServicer):
    
    def __init__(self):
        with open('{}/data/users.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["users"]
            
    def GetBookingForUser(self, request, context):
        """This method returns the bookings made by the user request.id"""
        id = request.id
        with grpc.insecure_channel('localhost:3001') as channel:
            print("Channel loaded")
            stub = booking_pb2_grpc.BookingStub(channel)
            user_id = booking_pb2.UserId(id)
            print("-------------- GetBookingForUser --------------")
            res = get_booking_for_user(stub, user_id)
        return res
    
    def GetMoviesPerRating(self, request, context):
        """This method returns all available movies sorted by their rating"""
        query = """ 
            { 
            movies_sorted_by_rate{
                id
                title
                rating
            }
            } 
            """
        response = requests.post("http://localhost:3000/graphql",json={'query': query})
        print("response status code: ", response.status_code) 
        if response.status_code == 200: 
            print("response : ", response.content) 
    
    def GetMovieAtDate(self, request, context):
        """This method returns all movies available at a chosen date request.date"""
        with grpc.insecure_channel('localhost:3001') as channel:
            print("Channel loaded")
            stub = booking_pb2_grpc.BookingStub(channel)
            date = booking_pb2.DateB(date= request.date)
            res = get_booking_at(stub, date)
        return res
    
    def BookMovie(self, request, context):
        """This method allows the user to book a movie session"""
        with grpc.insecure_channel('localhost:3001') as channel:
                stub = booking_pb2_grpc.BookingStub(channel)
                
                # Create the EntryAddBooking message
                booking_request = booking_pb2.EntryAddBooking(
                    user_id=booking_pb2.UserId(id=request.username),
                    new_movie=booking_pb2.NewMovie(
                        date=request.date,
                        movieid=request.movieid
                    )
                )
                
                # Use the add_booking function
                result = add_booking(stub, booking_request)
                
                # Check if the booking was successful
                if result and 'userid' in result:
                    return user_pb2.Status(booking_status="Booking successful")
                else:
                    return user_pb2.Status(booking_status="Booking failed")
        
        
        
        

def get_booking_for_user(stub, user_id):
    bookings = stub.GetBookingForUser(user_id)
    return MessageToDict(bookings)

def get_all_bookings(stub):
    empty = booking_pb2.Void()
    bookings = stub.GetAllBookings(empty)
    
    print("Bookings : ", MessageToJson(bookings))#bookings.bookings[0].dates[0].movies[0])

def get_booking_at(stub, date):
    bookings = stub.GetMovieAtDate(date)
    return MessageToDict(bookings)

def add_booking(stub, booking_user):
    bookings = stub.AddBookingByUser(booking_user)
    return MessageToDict(bookings)

def run():
    """This was made to test the service booking"""
    print("Run")
    with grpc.insecure_channel('localhost:3001') as channel:
        print("Channel loaded")
        stub = booking_pb2_grpc.BookingStub(channel)

        # user_id = booking_pb2.UserId(id="chris_rivers")
        # print("-------------- GetBookingForUser --------------")
        # get_booking_for_user(stub, user_id)
        print("-------------- GetAllBookings --------------")
        get_all_bookings(stub)
        # print("-------------- GetScheduleDate --------------")
        # date = booking_pb2.DateB(date="20151130")
        # get_booking_at(stub, date)
        # print("-------------- AddBookingByUser --------------")
        # user_booking = booking_pb2.EntryAddBooking(user_id={"id": "chris_rivers"},new_movie={"date":"20151130",
        #                                                                                      "movieid":"39ab85e5-5e8e-4dc5-afea-65dc368bd7ab"})
        # add_booking(stub,user_booking)
        # user_booking1 = booking_pb2.EntryAddBooking(user_id={"id": "chris_rivers"},new_movie={"date" : "20151201",
        #                                                                                      "movieid":"a8034f44-aee4-44cf-b32c-74cf452aaaae"})
        # add_booking(stub,user_booking1)
        # user_booking1 = booking_pb2.EntryAddBooking(user_id={"id": "Test"},new_movie={"date" : "20151201",
        #                                                                                      "movieid":"a8034f44-aee4-44cf-b32c-74cf452aaaae"})
        # add_booking(stub,user_booking1)
        # user_booking1 = booking_pb2.EntryAddBooking(user_id={"id": "chris_rivers"},new_movie={"date" : "141",
        #                                                                                      "movieid":"a8034f44-aee4-44cf-b32c-74cf452aaaae"})
        # add_booking(stub,user_booking1)
    channel.close()
    
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
   #run()