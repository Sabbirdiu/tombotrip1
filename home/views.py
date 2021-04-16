from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.http import JsonResponse
from .models import Experience,Supply,Rating,CommentForm,ProductAttribute,Order,Cartypes,OrderSupply
from .forms import OrderForm
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
# def filter_data(request):	  
# 	minPrice=request.GET['minPrice']
# 	maxPrice=request.GET['maxPrice']
#     cartypes=request.GET.getlist('cartype[]') 
#     brands=request.GET.getlist('brand[]')
# 	allProducts=Supply.objects.all().order_by('-id').distinct()
# 	allProducts=allProducts.filter(productattribute__price__gte=minPrice)
# 	allProducts=allProducts.filter(productattribute__price__lte=maxPrice)
#     if len(cartypes)>0:
# 		allProducts=allProducts.filter(cartype__id__in=cartypes).distinct()
# 	t=render_to_string('ajax/supply.html',{'data':allProducts})
# 	return JsonResponse({'data':t})   
def filter_data(request):
	colors=request.GET.getlist('color[]')
	# cartypes=request.GET.getlist('cartypes[]')
	catagories=request.GET.getlist('catagory[]')
	transmissions=request.GET.getlist('transmission[]')
	minPrice=request.GET['minPrice']
	maxPrice=request.GET['maxPrice']
	cartypes=request.GET.getlist('cartype[]') 
	allProducts=Supply.objects.all().order_by('-id').distinct()
	allProducts=allProducts.filter(productattribute__price__gte=minPrice)
	allProducts=allProducts.filter(productattribute__price__lte=maxPrice)
	if len(colors)>0:
		allProducts=allProducts.filter(productattribute__color__id__in=colors).distinct()
	if len(cartypes)>0:
		allProducts=allProducts.filter(cartypes__id__in=cartypes).distinct()
	if len(catagories)>0:
		allProducts=allProducts.filter(productattribute__category__id__in=catagories).distinct()
	if len(transmissions)>0:
		allProducts=allProducts.filter(productattribute__transmission__id__in=transmissions).distinct()
	t=render_to_string('ajax/supply.html',{'data':allProducts})
	return JsonResponse({'data':t})    
def ordersupply(request):
    current_user = request.user
    total=0
    order = Order.objects.filter(user_id=current_user.id)
    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        #return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............
            data = Order()
            data.first_name = form.cleaned_data['first_name'] #get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.start_date = form.cleaned_data['start_date']
            data.end_date = form.cleaned_data['end_date']
            data.location = form.cleaned_data['location']
            data.num_of_traveller = form.cleaned_data['num_of_traveller']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.save() #
            
            for rs in order:
                detail = OrderSupply()
                detail.order_id     = data.id # Order Id
                detail.supply_id   = rs.supply_id
                detail.user_id      = current_user.id
                # detail.quantity     = rs.quantity
                
              
                detail.save()
            # Order.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
            # request.session['cart_items']=0
            return render(request, 'Order_Completed.html')
            messages.success(request, "Your Order has been completed. Thank you ")
        else:
            messages.warning(request, form.errors)
            messages.warning(request,"Submit Error !!")
            return HttpResponseRedirect("/ordersupply")

   
    form= OrderForm()

    context = {
               'form': form,
               
               
               }
    return render(request, 'order_Form.html', context)

@login_required(login_url='/login') # Check login
def user_order_supply(request):
    
    current_user = request.user
    order_product = OrderSupply.objects.filter(user_id=current_user.id).order_by('-id')
    context = {
               'order_product': order_product,
               }
    return render(request, 'user_order_supply.html', context)


@login_required(login_url='/login') # Check login
def user_orders(request):
    
    current_user = request.user
    orders=Order.objects.filter(user_id=current_user.id)
    context = {
               'orders': orders,
               }
    return render(request, 'user_orders.html', context)