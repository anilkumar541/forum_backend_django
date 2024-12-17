from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Tag(models.Model):
    tag= models.CharField(max_length= 50)
    created_at= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.tag


class Question(models.Model):
    title= models.CharField(max_length= 300)
    body= models.TextField()
    author= models.ForeignKey(User, on_delete= models.CASCADE)
    tags= models.ManyToManyField(Tag)    
    created_at= models.DateTimeField(auto_now_add= True)    
    updated_at=  models.DateTimeField(auto_now= True) 

    def __str__(self):
        return self.title


class Answer(models.Model):
    question= models.ForeignKey(Question, related_name= "answers", on_delete= models.CASCADE)
    body= models.TextField()
    author= models.ForeignKey(User, on_delete= models.CASCADE)
    created_at= models.DateTimeField(auto_now_add= True)    
    updated_at=  models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.body[:50]
    

class Vote(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()

    class Meta:
        unique_together= ["user", "answer"]
        




