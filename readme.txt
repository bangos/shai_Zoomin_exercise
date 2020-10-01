I did this for windows
Set up the django project:

To create a virtual environment:
In shai_Zoomin_exercise-master
py -m venv starWars-Server

To activate the virtual environment run:
starWars-Server\Scripts\activate

Doing this will change your prompt like this:
(starWars-Server) C:\...>

install dependencies:
pip install -r requirements.txt

To run the server:
py manage.py runserver



To test it:
using Postman to create POST and GET requests: 
to get the list of characters and if the user like them or not I did GET:  http://127.0.0.1:8000/characters/?username=emma (if the user does not exist it will create on I did to be able to create without insert manually to DB) 
And to get the movies with the favorite characters of the user I used GET:  http://127.0.0.1:8000/movies/?username=emma
Of course that for the get you can just get to url and see it


to add a list of characters to favorites I did POST:  http://127.0.0.1:8000/characters/  with a body of: 
 key           |  value
--------------------------
username       | emma 
Characterslist | Han Solo,Luke Skywalker,Rey

(there are 2 users emma and shai you can check 
and you can create a new user uning post with new username and his Characterslist)