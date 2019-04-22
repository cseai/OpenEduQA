"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('core/', include('core.urls'))
"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from django.views.generic.base import RedirectView

import notifications.urls

from accounts.views import (
    login_view,
    register_view,
    logout_view
)

from mcq.views import index_page, latex_editor, vme_editor, openvme

urlpatterns = [
    path('', index_page, name='index'),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),
    path('admin/', admin.site.urls),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('comments/', include("comments.urls", namespace='comments')),

    path('accounts/', include("accounts.urls", namespace='accounts')),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('posts/', include("posts.urls")),

    path('level/', include("level.urls")),
    path('course/', include("course.urls")),

    path('article/', include("article.urls")),
    path('cq/', include("cq.urls")),
    path('mcq/', include("mcq.urls")),
    path('mcqexam/', include("mcqexam.urls")),
    path('cqexam/', include("cqexam.urls")),
    path('exam/', include("exam.urls")),
    path('teacher/', include("teacher.urls")),
    path('student/', include("student.urls")),
    path('room/', include("room.urls")),
    # path('posts/', "<appname>.views.<function_name>"),
    path('content/', include("mcq.suburls")),

    path('editor/', latex_editor),
    path('vme/', vme_editor),
    path('openvme/', openvme, name='openvme'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.views.generic.base import RedirectView
