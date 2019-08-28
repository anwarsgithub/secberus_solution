'''
Secberus Homework
-------------------------------------------------------------
Programmer: Anwar Numa
-------------------------------------------------------------
Python verison: 3.7.4
Description:
The program uses aiohttp to create the HTTP client.
I seperated the program into different functions to allow for
easier testing. The two main functions are the acquire_token
and the get_secret.

The acquire token will get a token using
the username and password provided, and terminate the program
if the username and passwords are incorrect.

The get_secret fucntion  will use the first token acquired
to attempt to get the message (this was done to avoid getting a
 new token every time the function is called). If the token has expired
 then it will call the acquire_token function once more to attempt
 to get the secret message again.


'''
import asyncio
import aiohttp


# Auth data to aquire bear token
JSON_PAYLOAD = {
    "username": "guest",
    "password": "guest"
}
#URL to aquire bearer token
AUTH_URL = 'http://localhost:5000/api/login'
#Base URL for secret Messages
SECRET_URL = 'http://localhost:5000/api/secret'
FIRST_TOKEN = ''


#This function aquires a bearer token
#using the authentication payload provided
async def aquire_token(payload):
    '''
    This function initiates a session and attempts to send a POST request
    to the api in order to get an Authorized bearer token.
    It takes in an authentication payload in the form of a dictionary.
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(AUTH_URL, json=payload) as resp:
            status = resp.status
            if status == 200:
                token = await resp.text()
                #response gets returned as a string and needs to be trimmed
                token = token.split("\"")[3]
                return token
            if status == 401:
                return 0

# This function will attempt to get the secret message
# with a requested bearer token if the status returned is
# 401 then it will close the session and initiate a new one with
# a new bearer token
async def get_secret(secret_num, token):
    '''
    This fucntion uses the base URL and a 1,2,3 is passed in as a string
    to complete the url. The second parameter is the bearer token. If the Bearer
    token is no longer active then the function will close the existing Client session,
    request a new bearer token, and attempt to get the secret message once again.
    '''
    header = new_auth_header(token)
    async with aiohttp.ClientSession() as session:
        async with session.get(SECRET_URL + secret_num, headers=header) as resp:
            status = resp.status
            if status == 200:
                print("status:"+ str(status))
                secret = await resp.text()
                secret = secret.split("\"")[3]
                print(secret)
            if status == 401:
                print("status: "+ str(status))
                await session.close()
                print("Unauthorized Bearer Token.. Reathenticaing..\n")
                token = await aquire_token(JSON_PAYLOAD)
                header = new_auth_header(token)
                async with aiohttp.ClientSession() as session:
                    async with session.get(SECRET_URL + secret_num, headers=header) as resp:
                        if resp.status == 200:
                            print("status: "+ str(resp.status))
                            secret = await resp.text()
                            secret = secret.split("\"")[3]
                            print(secret)
                        if resp.status == 401:
                            print("status: "+ str(resp.status))
                            print("The Secret message could not be acquired..")
            if status == 404:
                print("status: "+ str(status))
                print("The Page was not found!")


def new_auth_header(token):
    '''
    This function simply returns a dictionary that conforms to the
    Authorization Bearer token header.
    '''
    header = {"Authorization" : "Bearer " + token}
    return header

# the First token

# aquire the three secret messages
LOOP = asyncio.get_event_loop()
try:
    FIRST_TOKEN = LOOP.run_until_complete(aquire_token(JSON_PAYLOAD))
    if FIRST_TOKEN == 0:
        print("Incorrect Username and password for bearer token")
        exit(0)

    LOOP.run_until_complete(get_secret("1", FIRST_TOKEN))
    LOOP.run_until_complete(get_secret("2", FIRST_TOKEN))
    LOOP.run_until_complete(get_secret("3", FIRST_TOKEN))
except OSError:
    print("Connection could not be establsihed")
    print("Restart server and try again")
