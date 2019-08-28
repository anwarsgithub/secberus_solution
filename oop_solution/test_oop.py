'''
Secberus Homework Testing Solutions
------------------------------------------
Programmer: Anwar Numa
------------------------------------------

Description:
This is a simple testing of the acquire_token function
in the solution file. The function should return a 0 if
the token was not acquired and return the token if it was acquired.
This testing checks for both those cases and both cases should
pass. The case with the INCORRECT_PAYLOAD should return 0 and
the case with the correct PAYLOAD will return the token which is a string.

'''
import pytest
import oop_solution

PAYLOAD = {
    "username": "guest",
    "password": "guest"
}
INCORRECT_PAYLOAD = {
    "username": "No Guest",
    "password": "guest"
}

@pytest.mark.asyncio
async def test_aquire_token():
    '''
    This tests whether the acquire token function returns
    the correct response when giving correct and incorrect
    usernames and passwords.

    Both tests should pass
    '''
    client = oop_solution.Client()
    #test using incorrect username/password
    resp = await client.aquire_token(INCORRECT_PAYLOAD)
    assert resp == 0
    #Test using correct username/password
    resp = await client.aquire_token(PAYLOAD)
    assert resp != 0
