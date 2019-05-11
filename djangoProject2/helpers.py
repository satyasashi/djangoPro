from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# getting random string for generating activation key
from django.utils.crypto import get_random_string
# import hashlib to generate Hash from Chars a-z0-9@#$%^&*()_-+=, secret_key
import hashlib


def pg_records(request, lists, num):
	print(request)
	paginator = Paginator(lists, num)
	page = request.GET.get('page')
	try:
		page_object = paginator.page(page)
	except PageNotAnInteger:
		page_object = paginator.page(1)
	except EmptyPage:
		page_object = paginator.page(paginator.num_pages)
	return page_object


# Generating Activation key for User Registeration
def generate_activation_key(username):
	chars="abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(+-_=)"
	secret_key = get_random_string(20, chars)
	# take 20 Chars from Chars, add username and encode it and use SHA256() on them.
	return hashlib.sha256((secret_key + username).encode('utf-8')).hexdigest()