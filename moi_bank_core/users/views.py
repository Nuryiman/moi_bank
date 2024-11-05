from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout
from django.views import View
from users.models import CustomUser


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
			return redirect('/profile/')


class ProfileView(TemplateView):
	template_name = 'profile-page.html'

	def get_context_data(self, **kwargs):

		user = self.request.user

		context = {
			'user': user
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
		user.balance += 1
		user.save()
		return render(request=request, template_name='add-money-page.html', context={'user': user})


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
			return redirect('transaction-page-url')

		amount = data['amount']
		amount = int(amount)
		if amount <= sender.balance and amount < 0:
			with transaction.atomic():
				sender.balance -= amount
				received_user.balance += amount
				sender.save()
				received_user.save()
				return redirect('profile-url')
		else:
			return redirect('transaction-page-url')
