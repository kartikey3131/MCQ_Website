from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render,redirect
from .import forms
from Quiz import models


def home(request):
    return render(request,'home.html')

def dashboard(request):
    return render(request,'dashboard.html')
    
def teacher(request):
    return render(request,'teacher.html')
    
def student(request):
    return render(request,'student.html')

def attemptquiz(request):
    return render(request,'attemptquiz.html')

def google_signin(request):
    return render(request,'google_signin.html')
    
def is_teacher(user):
    if user.usertype.user_type=='Teacher':
        return True
    else:
        return False

def is_student(user):
    if user.usertype.user_type=='Student':
        return True
    else:
        return False

@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def register(request):
    form =forms.registerform()
    type_form =forms.Usertypeform()
    if request.method == 'POST':
        form = forms.registerform(data=request.POST)
        type_form =forms.Usertypeform(data=request.POST)
        if form.is_valid() and type_form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            user_type = type_form.save(commit=False)
            user_type.user = user
            user_type.save()
            messages.add_message(request,messages.SUCCESS,'THANK YOU FOR Regsitration Please login to continue')
            return HttpResponseRedirect(reverse('signin'))
        else:
            forms.registerform()
    return render(request,'signup.html',{'form':form, 'type_form':type_form})            

def signin(request):
    form = forms.loginform()
    if request.method == 'POST':
        form=forms.loginform(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = authenticate(username = username,password = password)
            if user:
                if user.is_active:
                    login(request,user)
                    if user.usertype.user_type == "Teacher":
                        return HttpResponseRedirect(reverse('teacher'))
                    else:
                        return HttpResponseRedirect(reverse('student'))   
            else:
                return HttpResponse("INVALID CREDENTIALS")
        else:
            return HttpResponseRedirect(reverse('sigin'))    
    return render(request,'signin.html',{'form':form})                         

@login_required
@user_passes_test(is_teacher)
def createquiz(request):
    form = forms.Quizform()
    if request.method =='POST':
        form=forms.Quizform(data=request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.user = request.user
            quiz.save()
            return redirect('../addquestions/'+str(quiz.pk)+'/1/')
    return render(request,'createquiz.html',{'form':form})        

@login_required
@user_passes_test(is_teacher)
def addquestions(request,s,q_no):
    form = forms.Questionform()
    quiz_object = models.Quiz.objects.get(pk=s)
    total=quiz_object.number
    if request.method =='POST':
        form =forms.Questionform(data=request.POST)
        if form.is_valid():
            question =form.save(commit=False)
            question.quiz=quiz_object
            question.save()
            if q_no == total:
                messages.success(request,'Quiz - '+str(quiz_object.title)+'created succesfully')
                return redirect('teacher')
            else:
                return redirect('../' + str(q_no + 1))
    return render(request, 'addquestions.html',{'form': form, 'i': q_no, 's': s, 'total': total})

@login_required
@user_passes_test(is_teacher)
def viewquizzes(request):
    quiz = models.Quiz.objects.all().filter(user=request.user)
    return render(request,'view_quiz.html',{'quiz':quiz})

@login_required
@user_passes_test(is_student)
def seeteachers(request):
    teacher = models.Usertype.objects.all().filter(user_type = "Teacher")
    return render(request,'seeteachers.html',{'teacher':teacher})

@login_required
@user_passes_test(is_student)
def seequizzes(request,s):
    teacher = models.User.objects.get(pk=s)
    quiz = models.Quiz.objects.all().filter(user = teacher)
    return render(request,'seequiz.html',{'quiz':quiz})

@login_required
@user_passes_test(is_teacher)
def editquiz(request,s,q_no):
    quiz=models.Quiz.objects.get(pk=s)
    total=quiz.number
    quiz_object = models.Question.objects.all().filter(quiz=quiz)  
    key = quiz_object.first().id -1 + q_no
    question = models.Question.objects.get(pk=key)
    questionform = forms.Questionform(instance=question)
    if request.method == 'POST':
        questionform = forms.Questionform(request.POST,instance=question)
        questionform.save()
        if q_no == total:
            return redirect('view_quiz')
        else:
            return redirect('../'+str(q_no+1))
    return render(request, 'edit_quiz.html',{'form': questionform,'question' : question, 'i': q_no, 's': s, 'total': total})

@login_required
@user_passes_test(is_teacher)
def delete_quiz(request,s):
    if request.method =='POST':
        models.Quiz.objects.get(pk=s).delete()
@login_required
@user_passes_test(is_student)
def takequiz(request,s,q_no):
    quiz = models.Quiz.objects.get(pk=s)
    question = models.Question.objects.all().filter(quiz = quiz)
    key = question.first().id -1+q_no
    total =quiz.number
    q = models.Question.objects.get(pk =key)
    if q_no == 1:
        if models.Marks_scored.objects.all().filter(user=request.user,quiz = quiz):
            print(models.Marks_scored.objects.all().filter(user=request.user,quiz = quiz))
            messages.warning(request,'You have already given this Quiz')
            return redirect('seeteachers')
        else:
            marks=models.Marks_scored()
            marks.quiz=quiz
            marks.user=request.user
    else:
        marks=models.Marks_scored.objects.get(user=request.user,quiz = quiz)
        
    marks.total_marks+=q.correct_ans
    if request.method =='POST':
        if request.POST['choices']==q.correct_choice:
            marks.marks+=q.correct_ans
        else:
            marks.marks+=q.incorrect_ans
        marks.save()    
        if q_no ==total:
            messages.success(request, 'You have completed Quiz ' + str(quiz.title)+'scoring'+str(marks.marks) +'out of' + str(marks.total_marks))
            return redirect('seeteachers')
        else:
            return redirect('../'+str(q_no+1))
    return render(request,'takequiz.html',{'quiz':quiz,'i':q_no,'s':s,'total':total,'q':q})

@login_required
@user_passes_test(is_student)
def see_results(request):
    quiz=models.Marks_scored.objects.all().filter(user=request.user)
    return render(request,'see_results.html',{'quiz':quiz})

@login_required
def see_standings(request,s):
    quiz=models.Quiz.objects.get(pk=s)
    marks=models.Marks_scored.objects.all().filter(quiz=quiz)
    marks = marks.order_by('-marks')
    return render(request,'see_standings.html',{'quiz':quiz,'marks':marks})
