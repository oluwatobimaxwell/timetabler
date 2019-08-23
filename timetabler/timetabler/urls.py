"""timetabler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views
from timetabler.forms import LoginForm
from django.conf import settings
from django.views.static import serve
from django.views.generic import RedirectView
# from books.views import about, get_all_books, get_one_book, get_old_books

urlpatterns = [
    path('login/', views.LoginView.as_view(
                authentication_form=LoginForm,
                redirect_authenticated_user=True,
                template_name='registration/login.html'),
                name='login',
                ),
    path('enrollment/', include("enrollment.urls"), name='enrollment'),
    path('faculty_mgt/', include("faculty_mgt.urls"), name='faculty'),
    path('lecturers_mgt/', include("lecturers_mgt.urls"), name='lecturers'),
    path('department_mgt/', include("departments_mgt.urls"), name='departments'),
    path('venues_mgt/', include("venues_mgt.urls"), name='venues'),
    path('courses_mgt/', include("courses_mgt.urls"), name='courses'),
    path('logout/', views.LogoutView.as_view(next_page = '/login'), name="login"),
    path('dashboard/', admin.site.urls),
    path('', RedirectView.as_view(url='/tablegenerator/generator', permanent=True), name="dashboard"),
    # path('', RedirectView.as_view(url='/dashboard', permanent=True), name="dashboard"),
    path('constraints/', include("constraints.urls"), name='constraints'),
    path('appsettings/', include("appsettings.urls"), name='appsettings'),
    path('tablegenerator/', include("tablegenerator.urls"), name='tablegenerator'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root':settings.MEDIA_ROOT,
        }),
    ]
