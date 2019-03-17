from django.shortcuts import render, redirect
from .models import *
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
import datetime
from django.conf import settings
import random
import string


host_location = 'http://127.0.0.1:8000/'

# Create your views here.
def index(request):
	ads = Ad.objects.filter(verified = True).order_by('-date')
	return render(request, 'main/index.html',context={
		"ads" : ads,
		})

def about(request):
	return render(request, 'main/about.html')

def establishments(request):
	categories = Category.objects.all()
	locations = Location.objects.all()
	ads = Ad.objects.filter(verified = True).order_by('-date')
	if request.method == 'POST':
		allowed_categories = []
		if 'category' in request.POST:
			for cid in request.POST.getlist('category'):
				allowed_categories.append(Category.objects.get(pk = cid))
			if len(allowed_categories) > 0: 
				ads = Ad.objects.filter(category__in = allowed_categories ).filter(verified = True)
		if request.POST['location'] != "all":
			allowed_location = Location.objects.get(pk = request.POST['location']) 
			ads = ads.filter(location = allowed_location)
		ads = ads.order_by('-date')
		return render(request, 'main/establishments.html', context = {
			"ads" : ads,
			"categories" : categories,
			"allowed_categories" : allowed_categories,
			"locations" : locations
			})
	return render(request, 'main/establishments.html', context={
		"ads" : ads,
		"categories" : categories,
		"locations" : locations,
		})

def loginView(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.method == 'POST':
		required = ['email', 'password']
		for item in required:
			if item not in request.POST:
				messages.error(request, "Incomplete Information.")
				return redirect('/login/')
		mail = request.POST['email'].strip()
		mail = mail.lower()
		user = authenticate(username=mail, password=request.POST['password'])
		if user is None:
			try:
				user = User.objects.get(username=mail)
			except:
				user = None
			if user is None:
				messages.error(request, "This Email Is Not Registered.") 
				return redirect("/register/")
			messages.error(request, "Invalid Credentials.")
			return redirect("/register/")
		try:
			client = Client.objects.get(user = user)
		except:
			messages.error(request, "Invalid Cerdentials.")
			return redirect('/login/')
		if not client.verified:
			messages.error(request, "Email Id not verified. <a href='/register/resend_validation?uid=%s'>Resend Email?</a>" % (client.id),extra_tags='safe')
			return redirect("/login/")      
		messages.success(request, "Successfully logged in.")
		login(request, user)
		return redirect('/')
	return render(request, 'main/login.html')

def logoutView(request):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue.")
		return redirect('/login/')
	logout(request)
	messages.success(request, "Successfully Logged out.")
	return redirect('/login/')

def register(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.method == 'POST':
		required = ['email','password','password-again','address','phone','website','fb']
		for item in required:
			if item not in request.POST:
				messages.error(request, "Incomplete Information.")
				return redirect("/student/register")
		mail=request.POST['email'].strip()
		mail=mail.lower()
		try:
			player = Client.objects.get(user = User.objects.get(username = mail))
			messages.error(request, "Email ID has already been registered.")
			return redirect("/login/")
		except:
			pass
		if request.POST['password'] != request.POST['password-again']:
			messages.error(request, "Paasword do not match.")
			return redirect("/register/")
		pswd = request.POST['password']
		user = User.objects.create_user(username = mail, password = pswd, email = mail)
		user.save()
		client = Client(user = user, address = request.POST['address'], phone = request.POST['phone'], website = request.POST['website'], fb = request.POST['fb'])
		client.save()
		global host_location
		activation = Activation(profile_ref = client)
		activation_code = activation.getActivationCode(client.user.username)
		activation.activation_code = activation_code
		activation.expiry = datetime.datetime.today().date() + datetime.timedelta(2)
		activation.save()
		send_mail(
				'Activation Link - Indian Community Center',
				'Hello,\n\nYour account was successfully created on Indian Community Center Advertisement Website.\n\nPlease verify your Email ID by clicking this link:\n %scheckmail/?ac=%s \n\nRegards,\nTeam Indian Community Center'%(host_location,activation_code),
				settings.DEFAULT_FROM_EMAIL,
				[client.user.username],
				fail_silently=False,
			)
		messages.success(request,"Account successfully created. Please check your mail box for verification link. Please verify your mail.")
		return redirect('/login/')

	return render(request, 'main/register.html')

def dashboard(request):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue.")
		return redirect('/login/')
	try:
		admin = Admin.objects.get(user = request.user)
		isadmin = True
	except:
		isadmin = False
	if isadmin:
		ads = Ad.objects.all()
		events = Event.objects.all()
		client = None
		ad_count = 0
		approvedad_count = 0
		event_count = 0
		approvedevent_count = 0
	else:
		client = Client.objects.get(user = request.user)
		ads = Ad.objects.filter(client = client)
		events = Event.objects.filter(client = client)
		ad_count = len(ads)
		event_count = len(events)
		approvedad_count = len(Ad.objects.filter(client = client).filter(verified = True))
		approvedevent_count = len(Event.objects.filter(client = client).filter(verified = True))
	categories = Category.objects.all()
	locations = Location.objects.all()
	return render(request, 'main/dashboard.html', context = {
		"isadmin" : isadmin,
		"ads" : ads,
		"events" : events,
		"client" : client,
		"categories" : categories,
		"locations" : locations,
		"ad_count" : ad_count,
		"approvedad_count" : approvedad_count,
		"event_count" : event_count,
		"approvedevent_count" : approvedevent_count,
		})

def deleteAd(request, adid):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue.")
		return redirect('/login/')
	flag = False
	try:
		admin = Admin.objects.get(user = request.user)
		flag = True
	except:
		pass
	try:
		ad = Ad.objects.get(pk = adid)
	except:
		messages.error(request, "No such ad exists.")
		return redirect('/dashboard/')
	if ad.client.user == request.user:
		flag = True
	if flag:
		ad.delete()
	else:
		messages.error(request, "You are not authorized to perform this action.")
		return redirect('/dashboard/')
	return redirect('/dashboard/')

def approveAd(request, adid):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue.")
		return redirect('/login/')
	try:
		admin = Admin.objects.get(user = request.user)
	except:
		messages.error(request, "You are not authorized to perform this action.")
		return redirect('/dashboard/')
	try:
		ad = Ad.objects.get(pk = adid)
	except:
		messages.error(request, "No such ad exists.")
		return redirect('/dashboard/')
	ad.verified = True
	ad.save()
	return redirect('/dashboard/')

def checkMail(request):
	if(request.method == "GET" and 'ac' in request.GET):
		try:
			activation = Activation.objects.get(activation_code = request.GET['ac'])
		except:
			activation = None
			messages.error(request, "Email ID not registered.")
			return redirect("/register/")
		if activation.profile_ref.verified:
			messages.error(request, "Email ID already verified.")
			return redirect("/login/")
		if(datetime.datetime.today().date() > activation.expiry):
			messages.error(request, "Verification code expired. <a href='/register/resend_validation?uid=%s'>Resend Email?</a>" % (activation.profile_ref.id),extra_tags='safe')
			return redirect("student/login/")
		activation.profile_ref.verified = True
		activation.profile_ref.save()
		messages.success(request, "Email ID successfully verified. Log in to continue.")
		return redirect('/login/')
	messages.error(request, "Unknown error occurred. Please try again.")
	return render(request, '/login/')

def resendMail(request):
	if(request.user.is_authenticated):
		return redirect('/', permanent=True)
	if('err' in request.GET):
		messages.error(request, "Unknown error occured.")
		return redirect('/login/')
	if('uid' not in request.GET):
		messages.error(request, "Unknown error occured.")
		return redirect('/login/')
	else:
		try:
			client = Client.objects.get(pk = request.GET['uid'])
		except:
			messages.error(request, "Unknown error occured.")
			return redirect('/login/')
		if client is not None:
			if client.verified:
				messages.success(request, "Email id is already verified.")
				return redirect('/login/')
			global host_location
			try:
				activation = Activation.objects.get(profile_ref = client)
				activation_code = activation.activation_code
				activation.expiry = datetime.datetime.today().date() + datetime.timedelta(2)
				activation.save()
			except:
				activation = Activation(profile_ref = client)
				activation_code = activation.getActivationCode(client.user.username)
				activation.activation_code = activation_code
				activation.expiry = datetime.datetime.today().date() + datetime.timedelta(2)
				activation.save()
			send_mail(
				'Activation Link - Indian Community Center',
				'Hello,\n\nYour account was successfully created on Indian Community Center Advertisement Website.\n\nPlease verify your Email ID by clicking this link:\n %scheckmail/?ac=%s \n\nRegards,\nTeam Indian Community Center'%(host_location,activation_code),
				settings.DEFAULT_FROM_EMAIL,
				[client.user.username],
				fail_silently=False,
			)
			messages.success(request, "Activation mail has been sent again. Please verify your Email ID.")
			return redirect("/login/")
	return redirect('/login/')

def forgotPass(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.method == 'POST':
		if 'email' not in request.POST:
			messages.error(request, "Incomplete Information.")
			return redirect('/forgotpassword/')
		try:
			mail = request.POST['email'].strip()
			mail = mail.lower()
			client = Client.objects.get(user = User.objects.get(username = mail))
		except:
			messages.error(request, "Email id is not registered.")
			return redirect('/register/')
		if not client.verified:
			messages.error(request, "Email Id not verified. <a href='/register/resend_validation?uid=%s'>Resend Email?</a>" % (client.id),extra_tags='safe')
			return redirect("/login/")      
		pswd = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
		matter = 'Your password has been reset.\n'
		matter += 'You can change your password later under Dashboard.\n\n'
		matter += 'Password - ' + pswd
		matter += '\n\n\n'
		matter += 'Regards\n Indian Community'
		user = User.objects.get(pk = client.user.id)
		user.set_password(pswd)
		user.save()
		send_mail(
				'Reset Password for Advertisement Website',
				matter,
				settings.DEFAULT_FROM_EMAIL,
				[mail],
				fail_silently=False,
			)
		messages.success(request, "Password has been reset successfully. Please check your mail.")
		return redirect('/login/')
	return render(request, 'main/forgotpass.html')

def changePass(request):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue")
		return redirect('/student/login/')
	try:
		admin = Admin.objects.get(user = request.user)
		messages.error(request, "You are not authorized to perform this action.")
		return redirect('/dashboard/')
	except:
		required = ['oldpass', 'newpass', 'confirmnewpass']
		for item in required:
			if item not in request.POST:
				messages.error(request, 'Unknown error occurred.')
				return redirect('/dashboard/')
		if not request.user.check_password(request.POST['oldpass']):
			messages.error(request, 'Incorrect password.')
			return redirect('/dashboard/')
		print(request.POST)
		if request.POST['newpass'] != request.POST['confirmnewpass']:
			messages.error(request, 'Password do not match.')
			return redirect('/dashboard/')
		request.user.set_password(request.POST['newpass'])
		request.user.save()
		user = authenticate(username=request.user.username, password=request.POST['newpass'])
		login(request, user)
		messages.success(request, "Password changed successfully.")
		return redirect('/dashboard/')

def uploadAd(request):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue.")
		return redirect('/login/')
	required = ['title', 'category', 'location','desc','services']
	for item in required:
		if item not in request.POST:
			messages.error(request, 'Incomplete Information.')
			return redirect('/dashboard/')
	print(request.FILES)
	if 'img' not in request.FILES:
		messages.error(request, 'Invalid image.')
		return redirect('/dashboard/')
	ad = Ad()
	ad.title = request.POST['title']
	ad.description = request.POST['desc']
	ad.services = request.POST['services']
	ad.image = request.FILES['img']
	ad.client = Client.objects.get(user = request.user)
	try:
		ad.category = Category.objects.get(pk = request.POST['category'])
	except:
		messages.error(request, 'Invalid category.')
		return redirect('/dashboard/')
	try:
		ad.location = Location.objects.get(pk = request.POST['category'])
	except:
		messages.error(request, 'Invalid location.')
		return redirect('/dashboard/')
	ad.save()
	messages.success(request, 'Your Advertisement was successfully uploaded.')
	return redirect('/dashboard/')

def events(request):
	categories = Category.objects.all()
	locations = Location.objects.all()
	events = Event.objects.filter(verified = True).order_by('-time')
	if request.method == 'POST':
		allowed_categories = []
		if 'category' in request.POST:
			for cid in request.POST.getlist('category'):
				allowed_categories.append(Category.objects.get(pk = cid))
			if len(allowed_categories) > 0: 
				events = Ad.objects.filter(category__in = allowed_categories ).filter(verified = True)
		if request.POST['location'] != "all":
			allowed_location = Location.objects.get(pk = request.POST['location']) 
			events = events.filter(location = allowed_location)
		events = events.order_by('-date')
		return render(request, 'main/events.html', context = {
			"events" : events,
			"categories" : categories,
			"allowed_categories" : allowed_categories,
			"locations" : locations
			})
	return render(request, 'main/events.html', context={
		"events" : events,
		"categories" : categories,
		"locations" : locations,
		})

def uploadEvent(request):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue.")
		return redirect('/login/')
	required = ['title', 'desc', 'venue','time','fees', 'category', 'location']
	for item in required:
		if item not in request.POST:
			messages.error(request, 'Incomplete Information.')
			return redirect('/dashboard/')
	if 'img' not in request.FILES:
		messages.error(request, 'Invalid image.')
		return redirect('/dashboard/')
	event = Event()
	event.title = request.POST['title']
	event.description = request.POST['desc']
	event.venue = request.POST['venue']
	event.time = request.POST['time']
	event.fees = request.POST['fees']
	event.image = request.FILES['img']
	event.client = Client.objects.get(user = request.user)
	try:
		event.category = Category.objects.get(pk = request.POST['category'])
	except:
		messages.error(request, 'Invalid category.')
		return redirect('/dashboard/')
	try:
		event.location = Location.objects.get(pk = request.POST['category'])
	except:
		messages.error(request, 'Invalid location.')
		return redirect('/dashboard/')
	event.save()
	messages.success(request, 'Your Advertisement was successfully uploaded.')
	return redirect('/dashboard/')

def deleteEvent(request, adid):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue.")
		return redirect('/login/')
	flag = False
	try:
		admin = Admin.objects.get(user = request.user)
		flag = True
	except:
		pass
	try:
		event = Event.objects.get(pk = adid)
	except:
		messages.error(request, "No such ad exists.")
		return redirect('/dashboard/')
	if event.client.user == request.user:
		flag = True
	if flag:
		event.delete()
	else:
		messages.error(request, "You are not authorized to perform this action.")
		return redirect('/dashboard/')
	return redirect('/dashboard/')

def approveEvent(request, adid):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue.")
		return redirect('/login/')
	try:
		admin = Admin.objects.get(user = request.user)
	except:
		messages.error(request, "You are not authorized to perform this action.")
		return redirect('/dashboard/')
	try:
		event = Event.objects.get(pk = adid)
	except:
		messages.error(request, "No such ad exists.")
		return redirect('/dashboard/')
	event.verified = True
	event.save()
	return redirect('/dashboard/')
