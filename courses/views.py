from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import CustomUser,Attendee,Course
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'courses/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = self.request.user.username +  'さん  希望する講座名、曜日を入力してください。' 
        context['finish'] = 0
        return context


class CourseApplicatedView(LoginRequiredMixin,TemplateView):
    template_name = 'courses/index.html'

    def post(self, request, *args, **kwargs):

        coursetype = request.POST['course']
        if coursetype == "begin": coursename = '初級' ; appli = '100'
        elif coursetype == "middle": coursename = '中級'; appli = '010'
        elif coursetype == "advance": coursename = '上級'; appli = '001'
        weekday = request.POST['weekday']

        finish = 0
        customuser = CustomUser.objects.get(username = self.request.user.username)

        #allattendee = Attendee.objects.all()
        #print('==allattendee', allattendee.count())
        #for item in allattendee:
        #    print(item, item.username, item.attended, item.applicated) 
        #print('==allattendee')
        #allcourses = Course.objects.all()
        #print('==allcourses', allcourses.count())
        #for item in allcourses:
        #    print(item, item.coursetype, item.requisite, item.mon, item.tue, item.wed )
        #print('==allcourses')
        #print('==customuser', customuser.id, customuser.username ,coursetype, weekday)

        attendee, created = Attendee.objects.get_or_create(username = customuser) # タプル result,created が返る

        #  testユーザの設定  ユーザが名fuga....なら　初級講座受講済にする
        #  ユーザ名がpiyo....なら　初級講座・中級講座受講済にする

        if customuser.username[:4] == 'fuga':
            Attendee.objects.filter(username=customuser).update(attended='100')
        if customuser.username[:4] == 'piyo':
            Attendee.objects.filter(username=customuser).update(attended='110')

        attendee = Attendee.objects.get_or_create(username = customuser)[0] 

        if request.POST['action'] == 'can':
            finish = 1
            message = '中止しました。'
        elif attendee.applicated != '000'   :
            finish = 1
            message = '申し込み済です。'

        if Course.objects.all().count() != 3:
            finish = 1
            message = '講座ファイルに講座がありません。'
        else:
            course = Course.objects.get(coursetype=coursetype)

        if finish == 0 and attendee.attended == course.requisite:
            if weekday == 'mon':
                weekname = '月曜'
                if course.mon > 0 :
                    finish = 1
                    message = coursename +' の ' + weekname +' に予約しました。'
                    Course.objects.filter(coursetype=coursetype).update(mon=F('mon')-1)
                    Attendee.objects.filter(username=customuser).update(applicated=appli)
    
            elif weekday == 'tue':
                weekname = '火曜'
                if course.tue > 0:
                    finish = 1
                    message = coursename + ' の ' + weekname + ' に予約しました。'
                    Course.objects.filter(coursetype=coursetype).update(tue=F('tue') - 1)
                    Attendee.objects.filter(username=customuser).update(applicated=appli)
    
            elif weekday == 'wed':
                weekname = '水曜'
                if course.wed > 0:
                    finish = 1
                    message = coursename + ' の ' + weekname + ' に予約しました。'
                    Course.objects.filter(coursetype=coursetype).update(wed=F('wed') - 1)
                    Attendee.objects.filter(username=customuser).update(applicated=appli)
    
            if  finish == 0:
                message = coursename + ' の ' + weekname + ' は満席です。'
    
        elif finish == 0:
            message = coursename + ' の受講資格はありません '


        #allattendee = Attendee.objects.all()
        #print('\n==allattendee', allattendee.count())
        #for item in allattendee:
        #    print(item, item.username, item.attended, item.applicated) 
        #print('==allattendee')
        #allcourses = Course.objects.all()
        #print('==allcourses', allcourses.count())
        #for item in allcourses:
        #    print(item, item.coursetype, item.requisite, item.mon, item.tue, item.wed )
        #print('==allcourses')


        ##post処理
        self.kwargs["message"] = message
        self.kwargs["finish"] = finish
        return render(request, self.template_name, context=self.kwargs)


class LogoutView(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    http_method_names = ['get']
    template_name = "account/logout.html"

