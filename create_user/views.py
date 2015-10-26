from django.shortcuts import render_to_response
from django.template import RequestContext



def create_user(request):
    context = {}
    return render_to_response('create_user/create_user.html',
                              RequestContext(request, context))