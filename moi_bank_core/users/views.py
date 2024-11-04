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
			redirect('register-url')
		except CustomUser.DoesNotExist:
			user = CustomUser.objects.create_user(name=name, password=password, first_name=name)
			login(request, user)
			redirect('/profile/')


class ProfileView(TemplateView):
	template_name = 'profile-page.html'

	def get_context_data(self, **kwargs):

		user = self.request.user
		if user.is_authenticated:
			context = {
				'user': user
			}
			return context
		else:
			redirect('login-url')

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
				redirect('profile-url')
			else:
				redirect('login-url')
		else:
			redirect('login-url')

