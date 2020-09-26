from django.http import JsonResponse
from django.shortcuts import render

from .models import User, Character, Movies
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets , status
from rest_framework import permissions
from starWars.quickstart.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChartersApiView(APIView):

    """
    this get function is to get the full list of the characters
    and if they are in the favorite list or not
    """
    def get(self, request):
        # get user name from url
        user_name = request.GET["username"]
        # if this is anew user create one (made this for me to create users)
        if not User.objects.filter(userName=user_name).exists():
            new_user = User(userName=user_name)
            new_user.save()

        # get user from database
        user = User.objects.get(userName=user_name)
        # get a list of the favorite characters for this user
        favorite_characters = user.characters.all()
        # empty list for the response json
        return_val = []

        # for each character in the database
        # check if he is the list of the user or not
        for character in Character.objects.all():
            if character in favorite_characters:
                return_val.append({character.name: True})
            else:
                return_val.append({character.name: False})

        return Response(return_val)

    """
    this is the post method for adding the favorites characters
    for a specific user
    """
    def post(self, request):
        # get user name from body of the request
        user_name = request.POST.get('username')

        # if user does not exists create one
        if not User.objects.filter(userName=user_name).exists():
            new_user = User(userName=user_name)
            new_user.save()

        # get the user from the database
        user = User.objects.get(userName=user_name)

        # get a new characters list to add to favorites from the message body
        characters_in_body = request.POST.get('characterslist')
        characters_list=characters_in_body.split(",")

        # for character name get the record from the database
        # check if the character is not in the linking table for this specific user
        # to add to the linking table

        for character in characters_list:
            character_to_add = Character.objects.get(name=character)
            if character_to_add not in user.characters.all():
                user.characters.add(character_to_add)

        # building json with the favorites characters for this user
        characters = [c.name for c in user.characters.all()]
        return_val = {user.userName: characters}

        return Response(return_val)


class UserChartersApiView(APIView):
    """
    this get function is to get the movies with the release date
    and the characters in this movie
    """
    def get(self, request):
        # get user and if not exists return message user dose not exist
        user_name = request.GET["username"]
        if not User.objects.filter(userName=user_name).exists():
            return JsonResponse({'message': 'user: {} dose not exist'.format(user_name)}, status=status.HTTP_204_NO_CONTENT)

        # get record of the user from the database
        user = User.objects.get(userName=user_name)

        # dictionary for the return jason
        dict_for_return = {}

        # for each character in the user table
        # get the movie he is in from the the database
        # for each movie if his in the dictionary then add to his list of names this character
        # if he is not in the dictionary add him with this character and the year he was released
        for char in user.characters.all():
            for mov in char.movies.all():
                movie_info = dict_for_return.get(mov.movie)
                if movie_info:
                    characters_list = movie_info.get("characters")
                    characters_list.append(char.name)

                    dict_for_return[mov.movie] = {"characters": characters_list,
                                                  "year": mov.year}
                else:
                    dict_for_return[mov.movie] = {"characters": [char.name],
                                                  "year": mov.year}
        return Response(dict_for_return)