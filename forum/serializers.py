from rest_framework import serializers
from .models import Tag, Question, Answer, Vote
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ["id", "username", "email", "password"]
        extra_kwargs= {"password": {"write_only": True}}

    def create(self, validated_data):
        user= User(**validated_data)
        user.set_password(validated_data["password"]) 
        user.save()
        return user

class TagSerailzer(serializers.ModelSerializer):
    class Meta:
        model= Tag
        fields= ["id", "tag"]



class AnswerSerializer(serializers.ModelSerializer):
    author= UserSerializer(read_only= True)
    upvotes= serializers.SerializerMethodField(read_only= True)
    downvotes= serializers.SerializerMethodField(read_only= True)

    class Meta:
        model= Answer
        fields= ["id", "body", "author", "upvotes", "downvotes", "created_at", "updated_at"]
        read_only_fields= ["author", "created_at", "updated_at"]

    def get_upvotes(self, obj):
        return Vote.objects.filter(answer= obj, is_upvote= True).count()    

    def get_downvotes(self, obj):
        return Vote.objects.filter(answer= obj, is_upvote= False).count()



class QuestionSerializer(serializers.ModelSerializer):
    tags= TagSerailzer(many= True, read_only= True)
    author= UserSerializer(read_only= True)
    answers= serializers.SerializerMethodField(read_only= True)

    class Meta:
        model= Question
        fields= ["id", "title", "body", "author", "tags", "answers", "created_at", "updated_at"]

    def get_answers(self, obj):
        # print(obj)
        answers= obj.answers.order_by("-created_at")
        return AnswerSerializer(answers, many= True).data
        
    # handle tag creation
    def create(self, validated_data):
        tags_data= self.context["request"].data.get("tags", [])
        validated_data["author"]= self.context["request"].user
        question= Question.objects.create(**validated_data)
        if tags_data:
            for tag_id in tags_data:
                tag = Tag.objects.get(id=tag_id)  # Retrieve the tag instance
                question.tags.add(tag) 
        return question

