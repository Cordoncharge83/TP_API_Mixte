import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import booking_pb2
import booking_pb2_grpc
import json
from google.protobuf.json_format import MessageToDict

class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]
    
    def GetAllBookings(self, request, context):
        """This method returns all the bookings made by all the users """
        print("self.bd = ", self.db)
        return booking_pb2.AllBookings(bookings=self.db) # Marche une fois sur deux ?
        

    def GetBookingForUser(self, request, context):
        req = json.loads(MessageToJson(request))
        for booking in self.db : 
            if booking["userid"] == req.id :
                print("Booking Found !")
                return booking_pb2.BookingsUser(userid = booking["userid"], dates = booking["dates"] )
        return booking_pb2.BookingsUser(userid = "", dates = "" )

    def GetMovieAtDate(self,request,context):
        with grpc.insecure_channel('localhost:3002') as channel:
            stub = showtime_pb2_grpc.ShowtimeStub(channel)
            date = showtime_pb2.Date(date=request.date)
            schedule = get_schedule_by_date(stub, date)
            print("schedule = ", MessageToDict(schedule))
            return booking_pb2.ScheduleB(date=schedule.date, movies=schedule.movies)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3001')
    server.start()
    server.wait_for_termination()

def get_schedule_by_date(stub,date):
    """return the schedule at the date date"""
    schedule = stub.GetMoviesByDate(date)
    return schedule

def get_all_schedule(stub):
    """Return all the schedule"""
    empty = showtime_pb2.Empty()
    schedules = stub.GetSchedule(empty)
    print("schedules : ", schedules.schedules[0].movies)

# def run():
#     print("Run")
#     with grpc.insecure_channel('localhost:3002') as channel:
#         print("Channel loaded")
#         stub = showtime_pb2_grpc.ShowtimeStub(channel)

#         print("-------------- GetDateSchedule --------------")
#         date = showtime_pb2.Date(date="20151130")
#         print("date loaded : ", date.date)
#         print(get_schedule_by_date(stub, date).movies)
#         print("-------------- GetAllSchedule --------------")
#         get_all_schedule(stub)

#     channel.close()

if __name__ == '__main__':
    serve()
    # run()