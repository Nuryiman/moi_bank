"""
URL configuration for moi_bank_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import (RegistrationView, MakeRegistrationView, MakeLogoutView, TransactionView,
                         ProfileView, LoginView, MakeLoginView, AddMoneyPageView, AddMoneyView, MakeTransactionView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegistrationView.as_view(), name='register-url'),
    path('', ProfileView.as_view(), name='profile-url'),
    path('make-register/', MakeRegistrationView.as_view(), name='make-register-url'),
    path('make-login/', MakeLoginView.as_view(), name='make-login-url'),
    path('make-logout/', MakeLogoutView.as_view(), name='make-logout-url'),
    path('login/', LoginView.as_view(), name='login-url'),
    path('add-money-page/', AddMoneyPageView.as_view(), name='add-money-page-url'),
    path('add-money/', AddMoneyView.as_view(), name='add-money-url'),
    path('transfer/', TransactionView.as_view(), name='transaction-page-url'),
    path('make-transfer/', MakeTransactionView.as_view(), name='make-transaction-url'),

]
