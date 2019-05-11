from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^today-is/$', views.today_is, name="today_is"),
	url(r'^$', views.post_list, name="post_list"),
	url(r'^(?P<pk>\d+)/(?P<post_slug>[\w\d-]+)/$', views.post_detail, name="post_detail"),
	url(r'^category/(?P<category_slug>[\w-]+)/$', views.post_by_category, name="post_by_category"),
	url(r'^tag/(?P<tag_slug>[\w-]+)/$', views.post_by_tag, name="post_by_tag"),
	url(r'^author/(?P<author_name>[\w]+)/$', views.post_by_author, name="post_by_author"),
	url(r'^blog/$', views.test_redirect, name="test_redirect"),
	url(r'^feedback/$', views.feedback, name="feedback"),
	url(r'^cookie/$', views.cookie_test, name="cookie_test"),
	url(r'^track-user/$', views.track_user, name="track_user"),
	url(r'^stop-tracking/$', views.stop_tracking, name='stop_tracking'),
	url(r'^start-session/$', views.test_session, name="test_session"),
	url(r'^delete-session/$', views.delete_session, name="delete_session"),
	url(r'^lousy-login/$', views.lousy_login, name="lousy_login"),
	url(r'^lousy-secret/$', views.lousy_secret, name="lousy_secret"),
	url(r'^lousy-logout/$', views.lousy_logout, name="lousy_logout"),
	url(r'^login/$', views.login, name='blog_login'),
    url(r'^logout/$', views.logout, name='blog_logout'),
    url(r'^admin_page/$', views.admin_page, name='admin_page'),
]