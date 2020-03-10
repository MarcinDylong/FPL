from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.



class IndexView(View):

    def get(self,request):

        return HttpResponse("Działa?")