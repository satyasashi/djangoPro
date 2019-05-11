# Forms for our Models
from django import forms
from django.core.exceptions import ValidationError
from .models import Author, Tag, Post, Category, Post, Feedback
from django.template.defaultfilters import slugify

class AuthorForm(forms.ModelForm):
	class Meta:
		model = Author
		fields = '__all__'

	def clean_name(self):
		""" Validating name field not to have 'admin', 'author'
		as the name. If it has, raise ValidationError """
		name = self.cleaned_data['name']
		name_l = name.lower()
		if name_l == "admin" or name_l == "author":
			raise ValidationError("Author name can't be 'admin/author'")
		return name

	def clean_email(self):
		"""Lower the email characters."""
		email = self.cleaned_data['email'].lower()
		

	# Unlike Models, Forms doesn't provide default save() method
	# Solution is to create custom method. Any name to method is ok.
	def save(self):
		new_author = Author.objects.create(
			name = self.cleaned_data['name'],
			email = self.cleaned_data['email'],
			active = self.cleaned_data['active'],
			created_on = self.cleaned_data['created_on'],
			last_logged_in = self.cleaned_data['last_logged_in']
			)
		return new_author

class TagForm(forms.ModelForm):
	class Meta:
		model = Tag
		fields = '__all__'

	def clean_name(self):
		"""Validating Tag name to not have 'tag', 'add', 'update' as their names"""
		n = self.cleaned_data['name']
		if n.lower() == "tag" or n.lower() == "add" or n.lower() == "update":
			raise ValidationError("Tag name can't be {0}".format(n))
		return n

	def clean_slug(self):
		"""Lower the slug characters."""
		return self.cleaned_data['slug'].lower()

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = '__all__'

	def clean_name(self):
		"""Validating Category name to not have 'tag', 'add', 'update' as their names"""
		n = self.cleaned_data['name']
		if n.lower() == "tag" or n.lower() == "add" or n.lower() == "update":
			raise ValidationError("Category name can't be {}".format(n))

	def clean_slug(self):
		return self.cleaned_data['slug'].lower()

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'content', 'author', 'category', 'tags')

	def clean_title(self):
		"""Validating title having 'post', 'add', 'update' as titles."""
		n = self.cleaned_data['title']
		if n.lower() == "post" or n.lower() == "add" or n.lower() == "update":
			raise ValidationError("Post name can't be {}".format(n))
		return n

	def save(self):
		"""Getting access to 'slug' and slugify it and save"""
		a = super(PostForm, self).save(commit=False)
		a.slug = slugify(a.title)
		a.save()
		return a

class FeedbackForm(forms.ModelForm):
	class Meta:
		model = Feedback
		fields = '__all__'