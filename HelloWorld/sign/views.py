from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

# Create your views here.
def index(request):
	# return HttpResponse('Hello Django!!!')
	return render(request, "index.html")
# 登录动作
def login_action(request):
	if request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')  # 获取输入的用户名密码
		user = auth.authenticate(username=username, password=password)  # 认证用户名密码：通过返回对象，不通过返回None
		if user is not None:
			auth.login(request, user) #登录
			# response.set_cookie('user', username, 3600)  # 添加浏览器的cookies
			request.session['user'] = username  # 将session的信息记录到浏览器
			response = HttpResponseRedirect('/event_manage/')
			return response
		else:
			return render(request, 'index.html', {'error': 'username or password error!!!'})
#发布会管理
@login_required
def event_manage(request):
	# username = request.COOKIES.get('user', '')  # 读取浏览器的cookies
	event_list = Event.objects.all()
	username = request.session.get('user', '')  # 读取浏览器的session
	paginator_event = Paginator(event_list, 2)
	page = request.GET.get('page')
	try:
		contacts_event = paginator_event.page(page)
	except PageNotAnInteger:  # 如果page不是整数，取第一页面数据
		contacts_event = paginator_event.page(1)
	except EmptyPage:  # 如果page不在范围，取最后一页
		contacts_event = paginator_event.page(paginator_event.num_pages)
	return render(request, 'event_manage.html', {'user': username, 'events': contacts_event})

# 发布会名称搜索
@login_required
def search_name(request):
	username = request.session.get('user', '')
	search_name = request.GET.get('name', '')
	event_list = Event.objects.filter(name__contains=search_name)
	return render(request, "event_manage.html", {"user": username, "events": event_list})

# 嘉宾管理
@login_required
def guest_manage(request):
	username = request.session.get('user', '')
	guest_list = Guest.objects.all()
	paginator_guest = Paginator(guest_list, 5)
	page = request.GET.get('page')
	try:
		contacts_guest = paginator_guest.page(page)
	except PageNotAnInteger:  # 如果page不是整数，取第一页面数据
		contacts_guest = paginator_guest.page(1)
	except EmptyPage:  # 如果page不在范围，取最后一页
		contacts_guest = paginator_guest.page(paginator_guest.num_pages)
	return render(request, 'guest_manage.html', {'user': username, 'guests': contacts_guest})

#嘉宾名称搜索
@login_required
def search_name_guest(request):
	username = request.session.get('user', '')
	search_name = request.GET.get('realname', '')
	guest_list = Guest.objects.filter(realname__contains=search_name)
	return render(request, "guest_manage.html", {"user": username, "guests": guest_list})

#签到页面
@login_required
def sign_index(request, eid):
	event = get_object_or_404(Event, id=eid)
	return  render(request, 'sign_index.html', {'event': event})

#签到动作
@login_required
def sign_index_action(request, eid):
	event = get_object_or_404(Event, id=eid)
	phone = request.POST.get('phone', '')
	print(phone)
	result = Guest.objects.filter(phone=phone)
	if not result:
		return render(request, 'sign_index.html', {'event':event, 'hint': 'phone error.'})
	result = Guest.objects.filter(phone=phone, event_id=eid)
	if not result:
		return render(request, 'sign_index.html', {'event': event, 'hint': 'event id or phone error.'})
	result = Guest.objects.get(phone=phone, event_id=eid)
	if result.sign:
		return render(request,'sign_index.html', {'event': event, 'hint': 'user has sign in.'})
	else:
		Guest.objects.filter(phone=phone,event_id=eid).update(sign='1')
		return render(request, 'sign_index.html', {'event': event, 'hint': 'sign in success', 'guest': result})
	
# 退出登录
@login_required
def logout(request):
	auth.logout(request)  # 退出登录
	response = HttpResponseRedirect('/index/')
	return  response