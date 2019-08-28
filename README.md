# Anwar - Secberus Homework Solution

Solution uses Python version 3.7.4

libraries used: aiohttp, asyncio, pytest(for testing)
requirements.txt file is included

The program will attempt to initiate a connection with
the server, if the connection is refused then the program
will exit.

ClientSession is used for the POST request in order to get the
bearer token and the GET request for the secret messages.

I've handled for 401 cases when accessing the secret messages and for when attempting to access a bearer Token

The output will be as follows:
status:
"Secret message" / Unauthorized Token
