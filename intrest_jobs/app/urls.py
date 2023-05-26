from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about , name='about'),
    path('jobs/', views.jobs, name='jobs'),
    path('job_details/', views.job_details, name='job_details'),
    path('blog/', views.blog,name='blog'),
    path('contact/', views.contact,name='contact'),
    path('login/', views.login_request,name='login'),
    path('register/', views.register,name='register'),
    path('logout/', views.logout_request,name='logout'),
    path('profile/', views.profile,name='profile'),
    path('skills/', views.skills,name='skills'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
