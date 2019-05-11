from django.contrib import admin
from .models import Post, Author, Category, Tag, Feedback

# class AuthorAdmin(admin.ModelAdmin):
# 	list_display = ('name', 'email', 'created_on')
# 	search_fields = ('name', 'email')
# 	ordering = ["-name"]
# 	list_filter = ['active']
# 	date_hierarchy = 'created_on' # only accepts STRING as value.

class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'pub_date', 'author', 'category')
	search_fields = ('title', 'content')
	ordering = ["-pub_date"]
	list_filter = ['pub_date']
	date_hierarchy = 'pub_date' # only accepts STRING as value.

	#filter_horizontal = ('tags',)
	raw_id_fields = ('tags',)
	#prepopulated_fields = {'slug': ('title',)}
	readonly_fields = ('slug',)
	fields = ('title', 'slug', 'content', 'author', 'category', 'tags')

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	search_fields = ('name',)

class TagAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	search_fields = ('name',)

class FeedbackAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'subject', 'date')
	search_fields = ('name', 'email')
	date_hierarchy = 'date'

# Register your models here.
# admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Feedback, FeedbackAdmin)