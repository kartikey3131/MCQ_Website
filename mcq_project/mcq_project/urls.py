"""mcq_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.home,name='home'),
    url(r'^register/',views.register,name='signup'),
    url(r'^sigin/',views.signin,name='signin'),
    url(r'^signout/',views.signout,name='signout'),
    url(r'^dashboard/',views.dashboard,name='dashboard'),
    url(r'^createquiz/',views.createquiz,name='createquiz'),
    url(r'^teacher/',views.teacher,name='teacher'),
    url(r'^student/',views.student,name='student'),
    url(r'^attemptquiz/',views.attemptquiz,name='attemptquiz'),
    path('addquestions/<int:s>/<int:q_no>/',views.addquestions,name='addquestions'),
    url(r'^view_quiz/',views.viewquizzes,name='view_quiz'),
    path('editquiz/<int:s>/<int:q_no>/',views.editquiz,name='edit_quiz'),
    path('seequiz/<int:s>/',views.seequizzes,name='seequiz'),
    url(r'^seeteachers/',views.seeteachers,name='seeteachers'),
    path('takequiz/<int:s>/<int:q_no>/',views.takequiz,name='takequiz'),
    url(r'^see_results/',views.see_results,name='see_results'),
    path('see_standings/<int:s>/',views.see_standings,name='see_standings'),
    url(r'^google_signin/',views.google_signin,name='google_signin'),
]
