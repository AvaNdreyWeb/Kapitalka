from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/wallet/', permanent=True)),
    path('wallet/', views.user_wallet, name='user_wallet'),
    path('wallet/<slug:slug>', views.group_wallet, name='group_wallet'),
    path('groups/', views.groups, name='groups'),
    path('debts/', views.debts, name='debts'),
    path('settings/', views.settings, name='settings'),
    path('sing-up/', views.create_user, name='sing_up'),
]
