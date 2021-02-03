from rest_framework import serializers
from note.models import User, Note# TokenUser

class UserSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ['user_id','name','email','ph']
class NoteSerializer(serializers.ModelSerializer):
     class Meta:
          model = Note
          fields = ['user_id','create_on','note']
# class TokenSerializer(serializers.ModelSerializer):
#      class Meta:
#           model = TokenUser
#           fields = ['user_id','token']