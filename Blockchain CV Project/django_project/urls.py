"""django_project URL Configuration

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
from django.contrib.auth.views import LoginView
from django.urls import path, include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('blog', include('blog.urls')),
    path('', user_views.login, name="login"),
    path('logout/',user_views.logout,name='logout'),
    path('search',user_views.search,name='search'),
    path('edit_experience', user_views.edit_experience, name='edit_experience'),
    path('confirmation',user_views.confirmation,name='confirmation'),
    path('confirmation/<int:id>',user_views.confirmation,name='confirmationSelect'),
    # path('employer', user_views.employer, name='employer'),

    path('candidate/<int:id>',user_views.displayCandidate,name='displayCandidate'),
    path('added/<int:id>',user_views.saveEntry,name='saveEntry'),
    path('displayblock',user_views.displayBlock,name='displayBlock'),
    path('resume',user_views.loadResume,name='loadResume')



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)