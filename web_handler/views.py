# -*- coding: utf-8 -*-                                                                                                                            
#                                                                                                                                                  
# author: frank muthee | mutheefrank@gmail.com                                                                                                      
#

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.shortcuts import render
from files_handler.methods import get_filenames,\
    overall_analysis,csv_download,excel_download


def attached_files(request):
    """                                                                                                                                             
    function view for displaying the attached files                                                                                                 
    """
    files = get_filenames()
    return render(request, 'attached_files.html',{'files':files})


def processed_output(request):
    """                                                                                                                                            
    function view to return paginated average balances on the web page                                                                              
    """
    output = overall_analysis()
    rows = len(output)
    ITEMS_PER_PAGE = 100
    paginator = Paginator(output,ITEMS_PER_PAGE)
    page = request.GET.get('page')

    try:
        output_page = paginator.page(page)
    except PageNotAnInteger:
        output_page = paginator.page(1)
    except EmptyPage:
        output_page = paginator.page(paginator.num_pages)

    return render(request, 'processed_files.html', {'output_page':output_page, 'rows':rows})    
    return render(request,'processed_files.html',{})


def more_actions(request):
    """                                                                                                                                       
    function view for few extra actions on the                                                                                                      
    processed_output                                                                                                                                
    """
    csv_file = csv_download()
    excel_file = excel_download()
    return render(request, 'more_actions.html',{'excel_file':excel_file, 'csv_file':csv_file})
    
def get_analytics(request):
    return render(request, 'analytics.html',{})

