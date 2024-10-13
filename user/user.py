from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from flask import Flask, request, jsonify,make_response

from google.protobuf.json_format import MessageToDict
import resolvers as r
import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json
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

def get_booking_for_user(stub, user_id):
    bookings = stub.GetBookingForUser(user_id)
    print("Bookings : ", MessageToDict(bookings))

def get_all_bookings(stub):
    empty = booking_pb2.Void()
    bookings = stub.GetAllBookings(empty)
    print("Bookings : ", MessageToDict(bookings))

def get_booking_at(stub, date):
    bookings = stub.GetMovieAtDate(date)
    print("Bookings : ", MessageToDict(bookings))

def run():
    print("Run")
    with grpc.insecure_channel('localhost:3001') as channel:
        print("Channel loaded")
        stub = booking_pb2_grpc.BookingStub(channel)

        user_id = booking_pb2.UserId(id="chris_rivers")
        # print("-------------- GetBookingForUser --------------")
        # get_booking_for_user(stub, user_id)
        # print("-------------- GetAllBookings --------------")
        # get_all_bookings(stub)
        print("-------------- GetScheduleDate --------------")
        date = booking_pb2.DateB(date="20151130")
        get_booking_at(stub, date)

    channel.close()
    
if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   # app.run(host=HOST, port=PORT)
   run()
