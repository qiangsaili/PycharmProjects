#!/usr/bin/env python
# encoding: utf-8
'''
@author: Sally
@time: 2018/5/31 22:32
'''

from django.http import JsonResponse
from sign.models import Event, Guest
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import IntegrityError
import time

# 添加发布会接口
def add_event(request):
	eid = request.POST.get('eid', '')    # 发布会id
	name = request.POST.get('name', '')  # 发布会标题
	limite = request.POST.get('limite', '')  # 限制人数
	status = request.POST.get('stauts', '')  # 状态
	address = request.POST.get('address', '')  # 地址
	start_time = request.POST.get('start_time', '')  # 发布会时间

	if eid == '' or name == '' or limite == '' or start_time == '':
		return JsonResponse({'status': 10021, 'message': 'parameter error'})
		
# 查询发布会接口
def get_event_list(request):
	eid = request.GET.get("eid", "") #发布会id
	name = request.GET.get("name", "") #发布会名称
	if eid != '' and name == '':
		return JsonResponse({'status': 10021, 'message': 'parameter error'})
	
	print("eid is %s, name is %s" % (eid, name))
	if eid != '':
		event = {}
		try:
			result = Event.objects.get(id=eid)
		except ObjectDoesNotExist:
			return JsonResponse({'status':10022, 'message':'query result is empty'})
		else:
			event['name'] = result.name
			event['limite'] = result.limite
			event['status'] = result.status
			event['address']= result.address
			event['start_time'] = result.start_time
			return JsonResponse({'status':200, 'message':'success','data':event})
		if name != '':
			datas = []
			results = Event.objects.filter(name__contains=name)
			if results:
				for r in results:
					event = {}
					event['name'] = r.name
					event['limite'] = r.limite
					event['status'] = r.status
					event['address'] = r.address
					event['start_time'] = r.start_time
					datas.append(event)
				return JsonResponse({'status':200, 'message':'success', 'data':datas})
			else:
				return JsonResponse({'status':10022, 'message':'query result is empty'})
	else:
		print("all...........")
		return JsonResponse({'status': 200, 'message': 'all'})

# 添加嘉宾接口
def add_guest(request):
	eid = request.POST.get('eid', '')
	realname = request.POST.get('realname', '')
	phone = request.POST.get('phone', '')
	email = request.POST.get('email', '')
	
	if eid=='' or realname == '' or phone == '':
		return JsonResponse({'status':10021, 'message':'parameter error'})
	
	result = Event.objects.filter(id=eid)
	if not result:
		return JsonResponse({'status': 10022, 'message': 'event is null'})
	
	result = Event.objects.filter(id=eid).status
	if not result:
		return JsonResponse({'status': 10023, 'message': 'event status is  not available'})
	
	event_limite = Event.objects.get(eid=id).limite  #发布会限制人数
	guest_limite = Guest.objects.filter(event_id=eid) #发布会已添加的嘉宾数
	
	if len(guest_limite) >= event_limite:
		return JsonResponse({'status':10024,'message':'event number is full'})
	
	event_time = Event.objects.get(id=eid).start_time  #发布会时间
	etime =str(event_time).split(".")[0]
	timeArray = time.strptime(etime, "%Y-%m-%d %H:%M:%S")
	e_time = int(time.mktime(timeArray))
	
	now_time = str(time.time())  #当前时间
	ntime = now_time.split(".")[0]
	n_time = int(ntime)

	if n_time >= e_time :
		return JsonResponse({'status':10025, 'message':'event has started'})

	try:
		Guest.objects.create(realname=realname, phone=int(phone), email=email, sign=0,event_id=int(eid))
	except IntegrityError:
		error = 'the event guest phone number is repeat'
		return JsonResponse({'status': 10026, 'message': error})
	return JsonResponse({'status': 200, 'message': 'add guest success'})

#查询嘉宾接口
def get_guest_list(request):
	eid = request.GET.get("eid", "")  # 关联发布会ID
	phone = request.GET.get("phone", "")  # 嘉宾手机号码
	
	if eid == '' :
		return JsonResponse({'status':10021 ,'message': 'eid cannot be empty'})
	
	if eid != '' and phone == '':
		datas = []
		results = Guest.objects.filter(event_id=eid)
		if results:
			for r in results :
				guest ={}
				guest['realname'] = r.realname
				guest['phone'] = r.phone
				guest['email'] = r.email
				guest['sign'] = r.sign
				datas.append()
			return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
		else:
			return ({'status':10022, 'message':'query result is empty'})
	if eid != '' and phone != '' :
		guest = {}
		try:
			result = Guest.objects.get(phone=phone,event_id=eid)
		except ObjectDoesNotExist:
			return JsonResponse({'status':10022, 'message':'query result is empty'})
		else:
			guest['realname'] = result.realname
			guest['phone'] = result.phone
			guest['email'] = result.email
			guest['sign'] = result.sign
			return JsonResponse({'status':200, 'message':'success', 'datas':guest})
		
# 嘉宾签到接口
def user_sign(request):
	eid = request.POST.get("eid", "")  # 发布会ID
	phone = request.POST.get("phone", "")  # 嘉宾手机号码
	if eid != '' and phone == '':
		return JsonResponse({'status': 10021, 'message': 'parameter error'})
	
	result = Event.objects.filter(id=eid)
	if not result:
		return JsonResponse({'status':10022, 'message':'event is null'})
	
	result = Event.objects.get(id=eid).status
	if not result:
		return JsonResponse({'status':10023,'message':'event status is not available'})
	
	event_time = Event.objects.get(id=eid).start_time  # 发布会时间
	etime = str(event_time).split(".")[0]
	timeArray = time.strptime(etime, "%Y-%m-%d %H:%M:%S")
	e_time = int(time.mktime(timeArray))
	
	now_time = str(time.time())  # 当前时间
	ntime = now_time.split(".")[0]
	n_time = int(ntime)
	
	if n_time >= e_time :
		return JsonResponse({'status':10024, 'message':'event has started'})
	
	result = Guest.objects.filter(phone=phone)
	if not result:
		return JsonResponse({'status':10025, 'message':'user phone null'})
	
	result = Guest.objects.filter(event_id=eid, phone=phone)
	if not result:
		return JsonResponse({'status':10026, 'message':'user did not participate in the conference'})
	
	result = Guest.objects.get(event_id=eid, phone=phone).sign
	if result:
		return JsonResponse({'status':10027, 'message':'user has sign in'})
	else:
		Guest.objects.filter(event_id=eid, phone=phone).update(sign='1')
		return JsonResponse({'status':200, 'message':'sign success'})