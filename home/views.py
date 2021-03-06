from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.http import JsonResponse
from .models import Experience,Supply,Rating,CommentForm,ProductAttribute,Cartypes

from user.models import UserProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from listvehicle.models import About,Agents
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from contact.models import Ownerquote 
from django.db.models import Max,Min,Count
from django.template.loader import render_to_string
from django.db.models import  Q
# Create your views here.
def test(request):
    return render(request,'home/test.html')
@ login_required
def favourite_list(request):
    user = request.user
    favourite_post = user.favourite.all()
    context = {
        'favourite_post' : favourite_post
    }
    return render(request,
                  'home/favourites.html',context)
@ login_required(login_url='/login')
def favourite(request,id):
    supply = get_object_or_404(Supply,id=id)
    if supply.favourite.filter(id=request.user.id).exists():
        supply.favourite.remove(request.user)
    else:
        supply.favourite.add(request.user)
    return HttpResponseRedirect('/favourites')        
def index(request):
    exp = Experience.objects.all()
    supply = Supply.objects.all().order_by('id')[:3]
    user = request.user
    # sup = Supply.objects.all()
    quote = Ownerquote.objects.filter()
    # is_favourite = False
    # if sup.favourite.filter(id=request.user.id).exists():
    #     is_favourite = True

    context = {
        'exp':exp,
        'supply':supply,
        # 'is_favourite':is_favourite,
        'quote':quote
    }
    return render(request,'home/home.html',context)
def supply(request):
    supply = Supply.objects.all()
    # sup = Supply.objects.all().order_by('-id').distinct()
    min_price=ProductAttribute.objects.aggregate(Min('price'))
    max_price=ProductAttribute.objects.aggregate(Max('price'))
    # is_favourite = False
    # if sup.favourite.filter(id=request.user.id).exists():
    #     is_favourite = True
    context = {
        'supply' :supply,
        # 'is_favourite':is_favourite,
        'min_price':min_price,
		'max_price':max_price
    }    
    return render(request,'home/supply.html',context)    
def supply_details(request,slug,id):
    supply = Supply.objects.get(pk=id,slug=slug)
    comments = Rating.objects.filter(supply_id=id,status='True')
    supply_list = Supply.objects.all().order_by('id')[:3]
    is_favourite = False
    if supply.favourite.filter(id=request.user.id).exists():
        is_favourite = True
    context ={
        'supply':supply,
        'comments':comments,
        'is_favourite':is_favourite,
        'supply_list':supply_list
    }
    return render(request,'home/supply_details.html',context)    
def exp_details(request,slug):
    exp = get_object_or_404(Experience,slug=slug) 
    about = About.objects.get()
    agents = Agents.objects.all()  
    context = {
        'exp':exp,
        'about':about,
        'agents':agents,
    }
    return render(request,'home/details.html',context)      
def addcomment(request,id):
   url = request.META.get('HTTP_REFERER')  # get last url
   #return HttpResponse(url)
   if request.method == 'POST':  # check post
      form = CommentForm(request.POST)
      if form.is_valid():
         data = Rating()  # create relation with model
         data.subject = form.cleaned_data['subject']
         data.comment = form.cleaned_data['comment']
         data.rate = form.cleaned_data['rate']
         data.ip = request.META.get('REMOTE_ADDR')
         data.supply_id=id
         current_user= request.user
         data.user_id=current_user.id
         data.save()  # save data to table
         messages.success(request, "Your review has ben sent. Thank you for your interest.")
         return HttpResponseRedirect(url)

   return HttpResponseRedirect(url)  
def supplysearch(request):
    queryset = Supply.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(car_title__icontains=query) |
            Q(city__icontains=query) |
            Q(description__icontains=query)

        ).distinct()
    context = {
        'supply': queryset,
        'query':query
    }
    return render(request, 'home/search_results.html', context)    
   
def filter_data(request):
	
	# cartypes=request.GET.getlist('cartypes[]')
	catagories=request.GET.getlist('catagory[]')
	transmissions=request.GET.getlist('transmission[]')
	minPrice=request.GET['minPrice']
	maxPrice=request.GET['maxPrice']
	cartypes=request.GET.getlist('cartype[]') 
	allProducts=Supply.objects.all().order_by('-id').distinct()
	allProducts=allProducts.filter(productattribute__price__gte=minPrice)
	allProducts=allProducts.filter(productattribute__price__lte=maxPrice)
	
	if len(cartypes)>0:
		allProducts=allProducts.filter(cartypes__id__in=cartypes).distinct()
	if len(catagories)>0:
		allProducts=allProducts.filter(productattribute__category__id__in=catagories).distinct()
	if len(transmissions)>0:
		allProducts=allProducts.filter(productattribute__transmission__id__in=transmissions).distinct()
	t=render_to_string('ajax/supply.html',{'data':allProducts})
	return JsonResponse({'data':t})    

    
   