"""
Definition of urls for Team1010BlockchainCV.
"""

from django.conf.urls import include, url
from BlockChainCv import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', Team1010BlockchainCV.views.home, name='home'),
    # url(r'^Team1010BlockchainCV/', include('Team1010BlockchainCV.Team1010BlockchainCV.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'',views.index,name='home'),
]
