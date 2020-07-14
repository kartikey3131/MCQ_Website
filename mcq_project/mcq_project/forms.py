from django import forms
from django.core import validators
from django.contrib.auth.models import User
from Quiz import models

def must_be_empty(value):
    if value:
        raise forms.ValidationError('BAD BOT')

class registerform(forms.ModelForm):
    re_password = forms.CharField(max_length=240,widget = forms.PasswordInput)
    hibot=forms.CharField(required = False,widget=forms.HiddenInput,label="Leave empty",validators=[must_be_empty])
    class Meta():
        model=User
        fields = ['username','email','password']
        widgets ={
            'password': forms.PasswordInput
        }
    def clean(self):
        cleaned_data= super().clean()
        password=cleaned_data.get('password')
        re_password=cleaned_data.get('re_password')

        if password!=re_password:
            raise forms.ValidationError('Please Enter same Password')


class Usertypeform(forms.ModelForm):
    class Meta:
        model =models.Usertype
        fields = ['user_type']

class Quizform(forms.ModelForm):
    class Meta:
        model=models.Quiz
        fields =['title','number']
    
    def clean(self):
        cleaned_data=super().clean()
        number = cleaned_data.get('number')
        if number<1:
            raise forms.ValidationError('Minimum 1 question required')
            
class Questionform(forms.ModelForm):
    class Meta:
        model = models.Question
        exclude = ['quiz']
    def clean(self):
        cleaned_data = super().clean()
        correct_choice = cleaned_data.get('correct_choice')
        choices = [cleaned_data.get('choice4'),cleaned_data.get('choice3'),cleaned_data.get('choice2'),cleaned_data.get('choice1')]

        if correct_choice not in choices:
            raise forms.ValidationError('Correct answer not in choices')


class loginform(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(max_length=240,widget=forms.PasswordInput)

