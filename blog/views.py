from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .models import Post, Author, Category, Tag, Feedback
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages, auth # for Flash Messages
from .forms import FeedbackForm
from django.core.mail import mail_admins # Feedback form sending Emails
from djangoProject2 import helpers
import datetime


# Create your views here.
def today_is(request):
	now = datetime.datetime.now()
	return render(request, 'blog/time.html', {'now': now,})

# view to list all the posts
def post_list(request):
	authors = Author.objects.all()
	categories = Category.objects.all()
	tags = Tag.objects.all()
	posts_list = Post.objects.all().order_by("-id")
	posts = helpers.pg_records(request, posts_list, 3)
	context = {
		'authors':authors,
		'categories':categories,
		'tags': tags,
		'posts':posts,
	}
	return render(request, 'blog/post_list.html', context)

# view to post in detail
def post_detail(request, pk, post_slug):
	# try:
	# 	post = Post.objects.get(pk=pk)
	# except Post.DoesNotExist:
	# 	return HttpResponseNotFound("Page Not Found")
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post,})

# view posts by category
def post_by_category(request, category_slug):
	# category = Category.objects.get(slug=category_slug)
	# posts = Post.objects.filter(category__slug=category_slug)
	category = get_object_or_404(Category, slug=category_slug)
	posts = get_list_or_404(Post.objects.order_by("-id"), category=category)
	# for side box categories, tags
	authors = Author.objects.all()
	categories = Category.objects.all()
	tags = Tag.objects.all()

	context = {
		'category': category,
		'posts': posts,
		'authors':authors,
		'categories':categories,
		'tags': tags,
	}
	return render(request, 'blog/post_by_category.html', context)

# view posts by tag
def post_by_tag(request, tag_slug):
	# tag = Tag.objects.get(slug=tag_slug)
	# posts = Post.objects.filter(tags__name=tag)
	tag = get_object_or_404(Tag, slug=tag_slug)
	posts = get_list_or_404(Post.objects.order_by("-id"), tags=tag)
	# for side box categories, tags
	authors = Author.objects.all()
	categories = Category.objects.all()
	tags = Tag.objects.all()
	

	context = {
		'tag': tag,
		'posts': posts,
		'authors':authors,
		'categories':categories,
		'tags': tags,
	}

	return render(request, 'blog/post_by_tag.html', context)

# Posts by authors
def post_by_author(request, author_name):
	author = get_object_or_404(Author, name=author_name)
	posts = get_list_or_404(Post.objects.order_by("-id"), author=author)
	# for side box categories, tags
	authors = Author.objects.all()
	categories = Category.objects.all()
	tags = Tag.objects.all()

	context = {
		'authorname':author,
		'posts': posts,
		'authors':authors,
		'categories': categories,
		'tags':tags,
	}
	return render(request, 'blog/post_by_author.html', context)

# Redirect view
def test_redirect(request):
	#return HttpResponseRedirect(reverse("post_list"))
	c = Category.objects.get(name="Python")
	return redirect(c)

# COOKIE TEST
def cookie_test(request):
	if not request.COOKIES.get('color'):
		response = HttpResponse("Cookie set")
		# secs in hr * 24hrs * 365Days * 2 => 2 Years
		response.set_cookie('color', 'Blue', 3600*24*365*2)
		return response
	else:
		return HttpResponse("Your favorite color is {}".format(request.COOKIES['color']))


# Count number of views
def track_user(request):
	if not request.COOKIES.get('visits'):
		response = HttpResponse("This is your first visit")
		response.set_cookie('visits', '1', 3600*24*365*2)
	else:
		visits = int(request.COOKIES.get('visits')) + 1
		response = HttpResponse("This is your {0} visit.".format(visits))
		response.set_cookie('visits', str(visits), 3600*24*365*2)
	return render(request, 'blog/track_user.html', {'response':response,})

# Stop tracking the user visits
def stop_tracking(request):
	if request.COOKIES.get('visits'):
		response = HttpResponse("Cookies Cleared")
		response.delete_cookie('visits')
	else:
		response = HttpResponse("We are not tracking you.")
	return response

# SESSIONS IN DJANGO
def test_session(request):
	request.session.set_test_cookie()
	return HttpResponse("Testing Session cookie")

# SESSION DELETE
def delete_session(request):
	# if there is a session cookie, kill it.
	if request.session.test_cookie_worked():
		request.session.delete_test_cookie()
		response = HttpResponse("Session Killed")
	else:
		# else, say something is wrong
		response = HttpResponse("Session test failed")
	return response

# Feedback form view
def feedback(request):
	if request.method == "POST":
		f = FeedbackForm(request.POST)

		if f.is_valid():
			name = f.cleaned_data['name']
			sender = f.cleaned_data['email']
			subject = "You have new Feedback from {}:{}".format(name, sender)
			message = "Subject: {}\n\nMessage: {}".format(f.cleaned_data['subject'], f.cleaned_data['message'])
			mail_admins(subject, message)

			f.save()
			messages.add_message(request, messages.INFO, "Feedback Submitted")
			return redirect('feedback')
	else:
		f = FeedbackForm()
	return render(request, 'blog/feedback.html', {'form':f,})


#====================================================	
# Lousy Login Using SESSIONS
def lousy_login(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		if username == "root" and password == "pass":
			request.session['logged_in'] = True
			return redirect('lousy_secret')
		else:
			messages.error(request, 'Error wrong username/password')
	return render(request, 'blog/lousy_login.html')

# Lousy secret
def lousy_secret(request):
	if not request.session.get('logged_in'):
		return redirect('lousy_login')
	return render(request, 'blog/lousy_secret.html')

# Lousy logout
def lousy_logout(request):
	try:
		del request.session['logged_in']
	except KeyError:
		return redirect('lousy_login')
	return render(request, 'blog/lousy_logout.html')

#=====================================================
# LOGIN System using Authentication Framework
def login(request):
	"""If the requested user is already authenticated(logged in),
		redirect him to 'admin' page.

		If he is requesting with credentials, take them and
		'authenticate()' them. If authenticated, redirect him
		to 'admin' page, else show error."""
	if request.user.is_authenticated():
		return redirect('admin_page')

	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = auth.authenticate(username=username, password=password)

		if user is not None:
			# Correct Username and Password, login the user
			auth.login(request, user)
			return redirect('admin_page')
		else:
			messages.error(request, 'Error wrong username/password')

	return render(request, 'blog/login.html')

def logout(request):
	# Take request object and use logout() method to kill session
	auth.logout(request)
	return render(request, 'blog/logout.html')

def admin_page(request):
	# If user is not authenticated and trying to access 'admin' page,
	# redirect that asshole to 'login' page, else just load the 'admin'
	# page for that good guy.
	if not request.user.is_authenticated():
		return redirect('blog_login')
	return render(request, 'blog/admin_page.html')