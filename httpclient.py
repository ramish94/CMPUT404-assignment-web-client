#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):

    port = 80

    def connect(self, request):
        mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mysock.connect((self.host, self.port))
        mysock.sendall(request)
        connect_socket = self.recvall(mysock)
        return connect_socket


    def disconnect(self, sock):
        try:
            sock.close()
        except:
            print("Socket could not be closed")


    def get_code(self, data):
        code = data.split(" ")[1]
        return int(code)


    def get_body(self, data):
        body = data.split("\r\n\r\n")[1]
        return body


    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)


    def createGET(self, host, port, path):
        GETHeader = "GET %s HTTP/1.1\r\nHost: %s:%s\r\nAccept-Encoding: */*\r\nConnection: close\r\n\r\n"%(path, host, port)
        return GETHeader


    def createPOST(self, host, port, path, args):
        POSTbody = ""
        if args:
            POSTbody = urllib.urlencode(args)
        POSTHeader = "POST %s HTTP/1.1\r\nHost: %s:%s\r\nAccept-Encoding: */*\r\nConnection: close\r\nContent-Length: %s\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n%s\r\n\r\n"%(self.path, self.host, self.port, len(POSTbody), POSTbody)
        return POSTHeader


    def GET(self, url, args=None):

        parsed = urlparse(url)
        self.host = parsed.hostname
        self.path = parsed.path

        if (":" in parsed.netloc):
            self.port = int(parsed.netloc.split(":")[1])

        header = self.createGET(self.host, self.port, self.path)
        recieved_data = self.connect(header)

        code = self.get_code(recieved_data)
        body = self.get_body(recieved_data)

        return HTTPResponse(code, body)


    def POST(self, url, args=None):
        parsed = urlparse(url)
        self.host = parsed.hostname
        self.path = parsed.path

        if (":" in parsed.netloc):
            self.port = int(parsed.netloc.split(":")[1])

        header = self.createPOST(self.host, self.port, self.path, args)
        recieved_data = self.connect(header)

        code = self.get_code(recieved_data)
        body = self.get_body(recieved_data)

        return HTTPResponse(code, body)


    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST(url, args)
        else:
            return self.GET(url, args)
    

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )   
