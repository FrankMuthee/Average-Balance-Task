# -*- coding: utf-8 -*-                                                                                                                             
#                                                                                                                                                   
# author: frank muthee | mutheefrank@gmail.com                                                                                                      
#                                                                                                                                                   
from django.conf.urls import url
from views import *

"""                                                                                                                                                 
urls for the web_handler pages                                                                                                                      
"""
urlpatterns = [

    url(r'^$', attached_files, name="attached_files"),

    url(r'^processed_output', processed_output, name="processed_files"),

    url(r'^more_actions', more_actions, name="more_actions"),

    url(r'^analytics', get_analytics, name="analytics"),
]
