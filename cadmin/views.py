from django.shortcuts import render, redirect, get_object_or_404, reverse, Http404
from blog.forms import PostForm
from django.contrib import messages # Flash messages to user.
from blog.models import Post, Author, Category, Tag
from django.contrib.auth import views as auth_views

# Preffered way to limit the access to admin page is to use
# login_required decorator '@login_required'. So, import it.
from django.contrib.auth.decorators import login_required

# Importing inbuilt UserCreationForm, messages for User Creation Form
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Custom User Creation Form in 'forms.py'
from .forms import CustomUserCreationForm
from djangoProject2 import helpers
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings


# Create your views here.
def post_add(request):
	# If request is POST, create a bound form
	if request.method=="POST":
		f = PostForm(request.POST)
		
		if f.is_valid():
			# if form is valid, save the data into DB and redirect to add post
			f.save()
			messages.add_message(request, messages.INFO, 'Post added')
			return redirect('post_add')
	else:
		# Show empty form
		f = PostForm()
	return render(request, 'cadmin/post_add.html', {'form': f,})


# Post Update
def post_update(request, pk):
	post = get_object_or_404(Post, pk=pk)

	# if request is POST, create a Bound form
	if request.method == "POST":
		f = PostForm(request.POST, instance=post)

		# Check whether form is valid or not
		# If form is valid, save the data to the database.
		# and redirect the user back to the update post form.
		if f.is_valid():
			f.save()
			messages.add_message(request, messages.INFO, 'Post Updated.')
			return redirect(reverse('post_update', args=[post.id]))

	# if request is GET the show unbound form to the user, along with data
	else:
		f = PostForm(instance=post)
	return render(request, 'cadmin/post_update.html', {'form':f, 'post':post})

# 'cadmin' home. when user logs in he goes here.
@login_required
def home(request):
	if not request.user.is_authenticated():
		return redirect('user_login')

	return render(request, 'cadmin/admin_page.html')

# Customizing the Default Login() function of 'django.contrib.auth'
# Because, After logging in, trying to visit Login page shouldn't show
# Login page. It should show 'adminpage'
def login(request, **kwargs):
	if request.user.is_authenticated():
		return redirect('/')
	else:
		return auth_views.login(request, **kwargs)


# 'User Creation Form' View
def register(request):
	if request.method == "POST":
		f = CustomUserCreationForm(request.POST)
		if f.is_valid():
			# Send Email verification. Generate activationKey by importing from helpers.py
			# Check 'helpers.py' for the code.
			activation_key = helpers.generate_activation_key(username=request.POST['username'])
			subject = "The Django Blog Account Verification"
			message = '''Hello {0},\n You have created an account in our site. \nPlease visit the following link to verify the account \n\n{1}://{2}/cadmin/activate/account/?key={3} \n\n If you did not create any account with us, please ignore this message.'''.format(request.POST['username'], request.scheme, request.get_host(), activation_key)
			error = False

			# Try to send Email. If any errors, show unable to send email error.
			try:
				send_mail(subject, message, settings.SERVER_EMAIL, [request.POST['email']])
				messages.add_message(request, messages.INFO, "Account created! Click on the link sent to your email to activate the account.")
			except:
				error = True
				messages.add_message(request, messages.INFO, "Unable to send email verification. Please try again.")

			if not error:
				# If there are no errors, take all the data and store it in variable.
				u = User.objects.create_user(
					request.POST['username'],
					request.POST['email'],
					request.POST['password1'],
					is_active = 0
					)

				# Now Save the user data into Author() model.
				author = Author()
				author.activation_key = activation_key
				author.user = u
				author.save()

			return redirect('register')
	else:
		f = CustomUserCreationForm()
	return render(request, 'cadmin/register.html', {'form': f,})

# activate account- Job is to set TRUE for is_active, email_validated
def activate_account(request):
	key = request.GET['key']
	if not key:
		raise Http404()

	r = get_object_or_404(Author, activation_key=key, email_validated=False)
	r.user.is_active = True
	r.user.save()
	r.email_validated = True
	r.save()

	return render(request, 'cadmin/activated.html')