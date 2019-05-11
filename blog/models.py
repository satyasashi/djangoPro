from django.db import models
from django.urls import reverse
# Extending User model
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
class Author(models.Model):
	# required to associate Author model with User model (Important)
	user = models.OneToOneField(User, null=True, blank=True)

	# Additional Fields after Associating with User Model
	activation_key = models.CharField(max_length=255, default=1)
	email_validated = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

	
class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(max_length=100, unique=True)
	author = models.ForeignKey(Author)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('post_by_category', args=[self.slug])

	class Meta:
		verbose_name_plural = "categories"

class Tag(models.Model):
	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(max_length=100, unique=True)
	author = models.ForeignKey(Author)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('post_by_tag', args=[self.slug])

class Post(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(unique=True, help_text="Slug will be automatically generated.")
	content = models.TextField()
	pub_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(Author)
	category = models.ForeignKey(Category)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post_detail', args=[self.id, self.slug])

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Post, self).save(*args, **kwargs)


class Feedback(models.Model):
	name = models.CharField(max_length=200, help_text="Name of the sender")
	email = models.EmailField(max_length=200)
	subject = models.CharField(max_length=200)
	message = models.TextField()
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "Feedback"

	def __str__(self):
		return self.name + "-" + self.email