from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views #import this


urlpatterns = [
    path('', Home, name='home'),
    path('votting', VottingPage, name='votting'),
    path('success', SuccessPage, name='success'),
    path('get_id', handleVote, name="get_id"),
    path('results', results, name="results"),
    path('comfirmation', comfirmCode, name="comfirmation"),
    path('password_reset', password_reset_request, name="password_reset"),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='votting/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="votting/password_reset_confirm.html"), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='votting/password_reset_complete.html'), name='password_reset_complete'),      

]
