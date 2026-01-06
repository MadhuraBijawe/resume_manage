from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import profile
from .views import dashboard  # ✅ fixed import


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('dashboard/', dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='resume/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/apply/<int:job_id>/', views.apply_job, name='apply_job'),  # ✅ use this or the shorter one
    path('my-applications/', views.my_applications, name='my_applications'),
    path('submit/', views.submit_resume, name='submit_resume'),  # ✅ This is what you need
    # Add your edit and delete URLs as well:
    path('edit/<int:id>/', views.edit_resume, name='edit_resume'),
    path('delete/<int:id>/', views.delete_resume, name='delete_resume')

]
