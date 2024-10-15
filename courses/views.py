from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Course, Attendee
from django.contrib.auth.decorators import login_required
from django.db.models import F

@login_required
def index(request):
    mess = request.user.username+'さん  希望する講座名、曜日を入力してください。'
    params = {'message': mess , 'finish': 0,}
    return render(request, 'courses/index.html', params)

@login_required
def form(request):
    coutype = request.POST['course']
    if coutype == "begin": couname = '初級' ; appli = '100'
    elif coutype == "middle": couname = '中級'; appli = '010'
    elif coutype == "advance": couname = '上級'; appli = '001'
    weekday = request.POST['weekday']
    course = Course.objects.get(coutype=coutype)

    finish = 0
    attendee = Attendee.objects.get_or_create(user=request.user)[0]
    if request.POST['action'] == 'can':
        finish = 1
        message = '中止しました。'
    elif attendee.applicated != '000'   :
        finish = 1
        message = '申し込み済です。'

    if finish == 0 and attendee.attended == course.coumask:
        if weekday == 'mon':
            weekname = '月曜'
            if course.mon > 0 :
                finish = 1
                message = couname +' の ' + weekname +' に予約しました。'
                Course.objects.filter(coutype=coutype).update(mon=F('mon')-1)
                Attendee.objects.filter(user=request.user).update(applicated=appli)

        elif weekday == 'tue':
            weekname = '火曜'
            if course.tue > 0:
                finish = 1
                message = couname + ' の ' + weekname + ' に予約しました。'
                Course.objects.filter(coutype=coutype).update(tue=F('tue') - 1)
                Attendee.objects.filter(user=request.user).update(applicated=appli)

        elif weekday == 'wed':
            weekname = '水曜'
            if course.wed > 0:
                finish = 1
                message = couname + ' の ' + weekname + ' に予約しました。'
                Course.objects.filter(coutype=coutype).update(wed=F('wed') - 1)
                Attendee.objects.filter(user=request.user).update(applicated=appli)

        if  finish == 0:
            message = couname + ' の ' + weekday + ' は満席です。'

    elif finish == 0:
        message = couname + ' の受講資格はありません '

    params = {'message': message , 'finish': finish}
    return render(request, 'courses/index.html', params)

