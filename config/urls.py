from django.contrib import admin
from django.urls import path, include
from courses import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('course_applicated', views.CourseApplicatedView.as_view(), name='course_applicated'),
    path('accounts/', include('allauth.urls')),
    path("logout/", views.LogoutView.as_view(), name="logout"),

]
