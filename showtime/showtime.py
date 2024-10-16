import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json
from google.protobuf.json_format import MessageToDict
import sys

class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]
    
    def GetSchedule(self,request,context):
        """Return the list of the schedule """
        print("Return Schedule")
        return showtime_pb2.AllSchedule(schedules=self.db)
    
    def GetMoviesByDate(self,request,context):
        """Return the schhedule available at the date request.date"""
        for schedule in self.db:
            if schedule["date"] == request.date:
                print("Movies found")
                var = showtime_pb2.Schedule(date=schedule["date"],movies=schedule["movies"])
                return var
        return showtime_pb2.Schedule(date="",movies=[])
    

def serve():
    """Launch the server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    print("Bonjout\n")
    print(sys.argv)
    serve()
