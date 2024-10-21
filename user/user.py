from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from flask import Flask, request, jsonify,make_response

from google.protobuf.json_format import MessageToDict, MessageToJson
import resolvers as r
import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json
import requests
import sys

# CALLING GraphQL requests
type_defs = load_schema_from_path('user.graphql')
query = QueryType()
mutation = MutationType()
movie = ObjectType('Movie')
actor = ObjectType('Actor')
query.set_field('get_movies_per_rating', r.get_movies_per_ratings)
query.set_field('get_movies_available_at_date',r.get_movies_available_at_date)
query.set_field('get_booking_made',r.get_booking_made)

mutation.set_field('book_the_movie', r.book_the_movie)
schema = make_executable_schema(type_defs, movie, query,mutation)

app = Flask(__name__)

PORT = 3003
HOST = '0.0.0.0'

BOOKING_PATH="http://localhost:3001"
MOVIE_PATH="http://localhost:3000"

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
    with grpc.insecure_channel(BOOKING_PATH) as channel:
        print("Channel loaded")
        stub = booking_pb2_grpc.BookingStub(channel)

        # user_id = booking_pb2.UserId(id="chris_rivers")
        # print("-------------- GetBookingForUser --------------")
        # get_booking_for_user(stub, user_id)
        # print("-------------- GetAllBookings --------------")
        # get_all_bookings(stub)
        print("-------------- GetScheduleDate --------------")
        date = booking_pb2.DateB(date="20151130")
        get_booking_at(stub, date)
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
#    run()
   if len(sys.argv) > 1 and sys.argv[1] == "docker":
      print("Image loaded with docker")
      BOOKING_PATH = "booking:3001"
      MOVIE_PATH = "http://movie:3000"
      r.MOVIE_PATH = "http://movie:3000"
      r.BOOKING_PATH = "booking:3001"
   app.run(host=HOST, port=PORT)

