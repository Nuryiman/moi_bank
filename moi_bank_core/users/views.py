import requests
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout
from django.views import View
from users.models import CustomUser, TransActionsHistory


class RegistrationView(TemplateView):
	template_name = 'registration-page.html'

	def get_context_data(self, **kwargs):
		context = {
			'correct': True,
			'exists': True,
		}
		return context


class MakeRegistrationView(View):

	def post(self, request, **kwargs):
		data = request.POST
		name = data['name']
		phone_number = data['phone']
		password = data['password']

		try:
			CustomUser.objects.get(phone_number=phone_number)
			return redirect('register-url')
		except CustomUser.DoesNotExist:
			user = CustomUser.objects.create_user(password=password, first_name=name, phone_number=phone_number)
			login(request, user)
			return redirect('profile-url')


class ProfileView(TemplateView):
	template_name = 'profile-page.html'

	def get_context_data(self, **kwargs):
		user = self.request.user

		API_KEY = '3d71e3792343ef04f3cfd570'
		url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/KGS'
		response = requests.get(url)
		if response.status_code == 200:
			data = response.json()
			currencies = data['conversion_rates']
			USD = currencies['USD']
			user_dollar_balance = USD * user.balance if user.is_authenticated else 0
		context = {
			'user': user,
			'dollar_balance': round(user_dollar_balance, 1)
		}
		return context


class LoginView(TemplateView):
	template_name = 'login-page.html'


class MakeLoginView(View):

	def post(self, request, *args, **kwargs):

		data = request.POST

		phone_number = data['phone']
		password = data['password']

		user = CustomUser.objects.get(phone_number=phone_number)
		if user:
			correct = user.check_password(password)
			if correct:
				login(request, user)
				return redirect('profile-url')
			else:
				return redirect('login-url')
		else:
			return redirect('login-url')


class MakeLogoutView(View):
	def post(self, request, *args, **kwargs):
		logout(request)
		return render(request, 'login-page.html', {})


class AddMoneyPageView(TemplateView):
	template_name = 'add-money-page.html'

	def get_context_data(self, **kwargs):
		user = self.request.user
		context = {
			'user': user
		}
		return context


class AddMoneyView(View):
	def post(self, request, *args, **kwargs):
		user = request.user

		if user.is_authenticated:
			user.balance += 1
			user.save()
			return render(request=request, template_name='add-money-page.html', context={'user': user})
		else:
			return redirect('login-url')


class TransactionView(TemplateView):
	template_name = 'transaction-page.html'

	def get_context_data(self, **kwargs):

		context = {
			'user': self.request.user,
		}
		return context


class MakeTransactionView(View):

	def post(self, request, *args, **kwargs):
		sender = request.user
		data = request.POST
		to_phone_number = data['phone']
		try:
			received_user = CustomUser.objects.get(phone_number=to_phone_number)
		except CustomUser.DoesNotExist:
			error = 'Такого номера не существует'
			context = {
				'has_errors': error
			}
			return render(request, 'transaction-page.html', context)
		amount = data['amount']
		amount = int(amount)
		if sender.phone_number == to_phone_number:
			error = 'Невозможно перевести деньги самому себе'
			context = {
				'has_errors': error
			}
			return render(request, 'transaction-page.html', context)
		if amount <= sender.balance:
			if amount <= 0:
				error = 'Сумма транзакции должна быть больше нуля'
				context = {
					'has_errors': error
				}
				return render(request, 'transaction-page.html', context)
			with transaction.atomic():
				sender.balance -= amount
				received_user.balance += amount
				TransActionsHistory.objects.create(user=sender, amount=-amount)
				TransActionsHistory.objects.create(user=received_user, amount=amount)
				sender.save()
				received_user.save()
				return redirect('profile-url')

		else:
			error = 'Недостаточно баланса на счете'
			context = {
				'has_errors': error
			}
			return render(request, 'transaction-page.html', context)
