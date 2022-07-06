from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout


from .forms import UserRegistrationForm, UserAuthenticationForm, AccountUpdationForm

from personal.models import Person

def UserRegistrationView(request) :
    context = {}

    if request.POST :
        form = UserRegistrationForm(request.POST)

        if form.is_valid() :
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')


            account = authenticate(email = email, password = raw_password)

            login(request, account)

            name = request.POST.get('username')
            person = Person.objects.create(name = name)
            person.save()

            return redirect('userHome')

        else : 
            context['registration_form'] = form

    else : # request.GET
        form = UserRegistrationForm
        context['registration_form'] = form

    return render(request, 'account/register.html', context)

def UserAuthenticationView(request) :
    context = {}

    user = request.user

    if user.is_authenticated :
        return redirect('userHome')
    
    if request.POST :
        form = UserAuthenticationForm(request.POST)

        if form.is_valid() :
            email = request.POST['email']
            password = request.POST['password']

            user = user = authenticate(email = email, password = password)

            if user :	# is the user is present in the DB,
                login(request, user)
                return redirect('userHome')

    else :
        form = UserAuthenticationForm(request.POST)

    context['login_form'] = form
    return render(request, 'account/login.html', context)


def logout_view(request) :
    logout(request)
    return redirect('siteHome')


def UserProfileView(request) :
	# if user is not logged in, redirect him to mainHome,
	if not request.user.is_authenticated :
		return redirect('siteHome')

	context = {}

	if request.POST :
		form = AccountUpdationForm(request.POST, instance = request.user)
		if form.is_valid() :
			form.save()

	else :
		form = AccountUpdationForm(
			initial= {
				"email" : request.user.email,
				"username" : request.user.username,
			}
		) 

	context['account_form'] = form
	return render(request, 'account/profile.html', context)

    
def admin_page_view(request) :
    return render(request, 'account/admin_page.html', {})