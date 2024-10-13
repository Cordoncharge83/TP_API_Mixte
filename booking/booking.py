import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import booking_pb2
import booking_pb2_grpc
import json
from google.protobuf.json_format import MessageToJson
class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]
    
    def GetBookingForUser(self, request, context):
        req = json.loads(MessageToJson(request))
        for booking in self.db : 
            if booking["userid"] == req.id :
                print("Booking Found !")
                return booking_pb2.BookingData(userid = booking["userid"], dates = booking["dates"] )
        return booking_pb2.BookingData(userid = "", dates = "" )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()

def get_schedule_by_date(stub,date):
    schedule = stub.GetMoviesByDate(date)
    print("schedule : ", schedule.movies)

def get_all_schedule(stub):
    empty = showtime_pb2.Empty()
    schedules = stub.GetSchedule(empty)
    print("schedules : ", schedules.schedules[0].date)

def run():
    print("Run")
    with grpc.insecure_channel('localhost:3002') as channel:
        print("Channel loaded")
        stub = showtime_pb2_grpc.ShowtimeStub(channel)

        print("-------------- GetDateSchedule --------------")
        date = showtime_pb2.Date(date="20151130")
        print("date loaded : ", date.date)
        get_schedule_by_date(stub, date)
        print("-------------- GetAllSchedule --------------")
        get_all_schedule(stub)

    channel.close()

if __name__ == '__main__':
    # serve()
    run()