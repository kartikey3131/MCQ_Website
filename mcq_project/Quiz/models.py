from django.db import models
from django.contrib.auth.models import User
from enum import Enum

class Type(Enum):
    Teacher = "Teacher"
    Student = "Student"

class Usertype(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key = True) 
    user_type = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in Type])

    def __str__(self):
        return self.user.username 

class Quiz(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    number = models.IntegerField(default = 1)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete= models.CASCADE)
    name = models.CharField(max_length=30)
    choice1 = models.CharField(max_length=30)
    choice2 = models.CharField(max_length=30)
    choice3 = models.CharField(max_length=30)
    choice4 = models.CharField(max_length=30)
    correct_choice = models.CharField(max_length=30)
    correct_ans = models.IntegerField(default=1)
    incorrect_ans = models.IntegerField(default=-1)
    unanswered = models.IntegerField(default=0)

    def __str(self):
        return self.name
    
class Marks_scored(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    marks =models.IntegerField(default = 0)
    total_marks =models.IntegerField(default=0)

    def __str__(self):
        return self.user.username +'-' + self.quiz.title

 
