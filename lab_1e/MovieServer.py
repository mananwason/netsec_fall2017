from asyncio import Protocol
from asyncio import *
import asyncio

from lab_1b.submission import RequestMovieInfo, RequestedInfoPacket, RequestAllDataPacket, AllDataPacket


class MoviesServer(Protocol):
    str = ''
    def __init__(self):
        self.deserializer = RequestMovieInfo.Deserializer()
        self.transport = None

    def connection_made(self, transport):
        print("Received a connection from {}".format(transport.get_extra_info("peername")))
        self.transport = transport

    def connection_lost(self, reason=None):
        print("Lost connection to client. Cleaning up.")

    def data_received(self, data):
        self.deserializer.update(data)
        for echoPacket in self.deserializer.nextPackets():
            print("Got '{}' from client.".format(echoPacket.movie_name))
            if isinstance(echoPacket, RequestMovieInfo):
                print("1")
                MoviesServer.str = echoPacket.parameter_name
                print(echoPacket.parameter_name)
                responsePacket = RequestedInfoPacket()
                responsePacket.parameter_info = "Comedy"
                responsePacket.parameter_name = echoPacket.parameter_name
                print(responsePacket.parameter_name)
                self.transport.write(responsePacket.__serialize__())

            elif isinstance(echoPacket, RequestAllDataPacket):
                print("2")

                print(echoPacket.movie_name)
                responsePacket = AllDataPacket()
                responsePacket.all_info_colon_separated = ""
            else:
                print("3")

                responsePacket = None
            print(responsePacket.version)


