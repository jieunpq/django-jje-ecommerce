from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product
# Create your views here.

# dev_1
# dev_5
def home(request):
    products = Product.objects.all()
    return render(request,'store/home.html',{"products":products})

def about(request):
    return render(request,'store/about.html',{})