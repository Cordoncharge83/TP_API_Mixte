import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import booking_pb2
import booking_pb2_grpc
import json
from google.protobuf.json_format import MessageToDict
import sys

PATH_TIMES:str = 'localhost:3002'
class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]
    
    def GetAllBookings(self, request, context):
        """This method returns all the bookings made by all the users """
        print("self.bd = ", {"bookings" :self.db}, "\n")
        res = booking_pb2.AllBookings(bookings=[]) #{"bookings" :self.db})
        for booking in self.db:
            bookingsUser = booking_pb2.BookingsUser(userid=booking["userid"],dates=[])
            for date in booking["dates"]:
                dateItem = booking_pb2.DateItem(date=date["date"],movies=date["movies"])
                bookingsUser.dates.append(dateItem)
            res.bookings.append(bookingsUser)
        print("res : ", MessageToDict(res), "\n\n")
        return res 
        

    def GetBookingForUser(self, request, context):
        """Return the bookings made by the user request.id"""
        for booking in self.db : 
            if booking["userid"] == request.id :
                print("Booking Found !")
                return booking_pb2.BookingsUser(userid = booking["userid"], dates = booking["dates"] )
        return booking_pb2.BookingsUser(userid = "", dates = "" )

    def GetMovieAtDate(self,request,context):
        """Return the movies available at the date request.date"""
        print("Je suis ici")
        with grpc.insecure_channel(PATH_TIMES) as channel:
            stub = showtime_pb2_grpc.ShowtimeStub(channel)
            date = showtime_pb2.Date(date=request.date)
            schedule = get_schedule_by_date(stub, date)
            print("schedule = ", MessageToDict(schedule))
            return booking_pb2.ScheduleB(date=schedule.date, movies=schedule.movies)

    def AddBookingByUser(self,request,context):
        """Add a booking for the user request.user_id if it is possible"""
        # Firstly we check if the movie is available at the date request.date
        # We get the movies wich will be projected at the date request.date
        with grpc.insecure_channel(PATH_TIMES) as channel:
            stub = showtime_pb2_grpc.ShowtimeStub(channel)
            date = showtime_pb2.Date(date=request.new_movie.date)
            schedule = get_schedule_by_date(stub, date)
        # If the movie is projected at request.date
        if schedule != [] and request.new_movie.movieid in schedule.movies:
            # We can add a booking
            for user in self.db:
                if user["userid"] == request.user_id.id:
                    # We found the good user
                    # We check if the user didn't already book this movie at the date request.date
                    for date in user["dates"]:
                        if date["date"] == request.new_movie.date:
                            if not request.new_movie.movieid in date["movies"]:
                                # We can finally add the booking
                                date["movies"].append(request.new_movie.movieid)
                                # We write in the database
                                print("Booking added")
                                write(self.db)
                                # We return an answer
                                return booking_pb2.BookingsUser(userid=user["userid"],dates=user["dates"])
                    # The user didn't do any booking at the date given
                    user["dates"].append({"date":request.new_movie.date,"movies":[request.new_movie.movieid]})
                    # We write in the database
                    print("Booking added with a new date")
                    write(self.db)
                    # We return an answer
                    return booking_pb2.BookingsUser(userid=user["userid"],dates=user["dates"])
            # The user didn't do any reservation, we need to at him/her/they into our database
            new_user = {
                "userid": request.user_id.id,
                "dates": [{
                    "date":request.new_movie.date,
                    "movies":[request.new_movie.movieid]
                }]}
            self.db.append(new_user)
            # We write in the database
            print("Booking added with a new user")
            write(self.db)
            # We return an answer
            return booking_pb2.BookingsUser(userid=new_user["userid"],dates=new_user["dates"])
        return booking_pb2.BookingsUser(userid="",dates=[{"date":"","movies": [""]}])

def write(movies):
    """This function replace the database with the new one"""
    with open('{}/data/bookings.json'.format("."), 'w') as f:
        
        json.dump({"bookings":movies}, f)

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

def run():
    """Code made to test the showtime service"""
    print("Run")
    with grpc.insecure_channel('localhost:3002') as channel:
        print("Channel loaded")
        stub = showtime_pb2_grpc.ShowtimeStub(channel)

        print("-------------- GetDateSchedule --------------")
        date = showtime_pb2.Date(date="20151131")
        print("date loaded : ", date.date)
        print(get_schedule_by_date(stub, date).movies)
        print("-------------- GetAllSchedule --------------")
        get_all_schedule(stub)

    channel.close()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "docker":
      print("Image loaded with docker")
      PATH_TIMES = "http://showtime:3002"
    serve()
    # run()