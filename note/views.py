from django.shortcuts import render
from django.http import response
from rest_framework import viewsets
from rest_framework import permissions
from note.models import User, Note
from note.serializers import UserSerializer, NoteSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
import requests
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.decorators import api_view
# Create your views here.
from django.contrib.auth.models import User as Users
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

@api_view(['POST'])
def login(request):
     if "username" in request.query_params and "password" in request.query_params:
          print(request.query_params['username']+" "+request.query_params['password'])
          user = authenticate(request=request,username = request.query_params['username'],password = request.query_params['password'])
          print(user)
          if user!=None:
               for user in Users.objects.all():
                    if user.username == request.query_params['username']:
                         print("User aldreay exits!")
                         try:
                              token = Token.objects.create(user = user)
                              print(token +" generated")
                         except:
                              print("Token aldready exists!")
                              token = Token.objects.get(user=user)
                         user.save()
               return Response({"Message":"Success","Token":str(token)})
          else:
               return Response({"Error":"Invalid Credentials!"})
     else:
          return Response({"Error":"Invalid Request!"})
@api_view(['POST'])
def logout(request):
     print(request.headers.get("Authorization"))
     if request.headers.get("Authorization")!=None:
          token = request.headers.get("Authorization")
          user = Token.objects.get(key=token)
          print(user.user)
          current_user = Users.objects.get(username=user.user)
          current_user.save()
          return Response({"Message":"See terminal!"})
     else:
          return Response({"Error":"Invalid Operation!"})
@api_view(['POST'])
def signUp(request):
     if 'email'in request.query_params and'name'in request.query_params and'password'in request.query_params and'ph'in request.query_params and'user_id'in request.query_params :
          try:
               for user in User.objects.all():
                    if user.email == request.query_params['email']:
                         return Response({"Error":"User with this Email ID aldready exist!"})
               user = Users.objects.create(username=request.query_params['user_id'],email=request.query_params['email'],password=request.query_params['password'],is_superuser=True,is_active=False)
               token = Token.objects.create(user=user)
               print(token)
          except:
               return Response({"Error":"The email Id has been taken try with other one!"})
          try:
               User.objects.create(user_id=request.query_params['user_id'],email=request.query_params['email'],name = request.query_params['name'],ph = request.query_params['ph'])
          except:
               return Response({"Error":"Invalid Credentials have been entered! Try with other user_id or email"})
          print("Success!")
          return Response({"Token":str(token)})
     else:
          return Response({"Error":"Not a valid Request!"})
          

class UserViewset (viewsets.ModelViewSet):
     permission_classes=[IsAuthenticated]
     def get_queryset(self):
          print("Queryset is over ridden!")
          print(self.request.query_params)
          if 'id' in self.request.query_params:
               queryset = User.objects.filter(user_id=self.request.query_params['id'])
          else:
               queryset = User.objects.all()
          return queryset
     def create(self, request, *args, **kwargs):
               return Response({"Message":"Please register first!"})
     
     serializer_class = UserSerializer
class NoteViewset(viewsets.ModelViewSet):
     permission_classes=[IsAuthenticated]
     filter_backends = [filters.SearchFilter]
     search_fields = ['note', 'user_id','create_on']
     def get_queryset(self):
          print("Woke up query_Set!")
          request = self.request
          token = request.headers.get("Authorization")
          user_name = Token.objects.get(key=token.split()[1])
          user = User.objects.get(name=user_name.user)
          queryset = Note.objects.filter(user_id=user)
          #Use filter always it really works
          return queryset
     def list(self,request,*args,**kwargs):
          print("Woke up list!")
          notes = self.get_queryset()
          serializer = NoteSerializer(notes,many = True)
          print(serializer.data)
          return Response(serializer.data)
     def retrieve(self, request, *args, **kwargs):
          print("Woke up retrieve!")
          obj = self.get_object()
          serializer = NoteSerializer(obj)
          return Response(serializer.data)
     serializer_class = NoteSerializer
     def create(self,request,*args,**kwargs):
          token = request.headers.get("Authorization")
          print(token.split()[1])
          user_name = Token.objects.get(key=token.split()[1])
          print(user_name.user)
          user = User.objects.get(name=user_name.user)
          note = Note.objects.create(user_id=user,note=request.query_params['note'])
          serializer = NoteSerializer(note)
          return Response(serializer.data)
@api_view(['GET'])
def CovidViewset (request):
     url = "https://www.worldometers.info/coronavirus/?utm_campaign=homeAdvegas1?%22%20%5Cl%20%22countries"
     r = requests.get(url)
     soup = BeautifulSoup(r.content,'html5lib')
     soup.prettify()
     temp = []
     count = 0
     for row in soup.find_all('tr',attrs = {'style': ''})[2:]:
          tds = row.find_all('td')
          if count > 30:
               break
          count+=1
          try:
               temp.append({"country":tds[1].text,"Total Cases":tds[2].text,"Total Deaths":tds[4].text,"Total Recovered":tds[6].text,"Active Cases":tds[8].text})
          except:
               print("Error!")
     print(request.query_params)
     if "country" in request.query_params:
          found = False
          for i in temp:
               if i['country'] == request.query_params['country']:
                    found = True
                    return Response({"list":[i]})
          if found == False:
               return Response({"Error":"Check the query once!"})
     return Response({"list":temp})


