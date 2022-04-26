from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import View, UpdateView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserLoginForm, UserUpdateForm, UserCreateForm
from .models import NormalUser, UserProfile

# Create your views here.

class UserView(View):
	template_name = "users/base.html"

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)

class UserLoginView(LoginView):
	template_name = "users/login.html"
	form_class = UserLoginForm
	success_url = "users:profile"

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse_lazy(self.success_url))
		return super(UserLoginView, self).get(request, *args, **kwargs)


class UserProfileView(LoginRequiredMixin, UpdateView):
	model = NormalUser
	template_name = "users/profile.html"
	form_class = UserUpdateForm

	def get(self, request, *args, **kwargs):
		self.object = NormalUser.objects.get(pk=request.user.id)
		context = self.get_context_data(**kwargs)

		# условие для суперюзера, т.к. для него нет соответстующей таблицы
		if not request.user.is_superuser:
			context["rosters_count"] = UserProfile.objects.get(user=request.user.id).rosters_count

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form_class(data=request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse("users:profile"))


class UserRegisterView(CreateView):
	model = NormalUser
	template_name = "users/register.html"
	form_class = UserCreateForm

	def get_success_url(self):
		return reverse_lazy("users:profile")



def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse("users:login"))

def index(request):
	return render(request, "users/index.html")