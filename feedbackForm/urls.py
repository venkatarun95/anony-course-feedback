from django.conf.urls import patterns, url

from feedbackForm import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^login$', views.loginPage, name='login'),
	url(r'^logout$', views.logout_page, name='logout'),
	url(r'^user_home$', views.user_home, name='user_home'),
	url(r'^student_home$', views.student_home, name='student_home'),
	url(r'^student_feedback_form$', views.student_feedback_form, name='student_feedback_form'),    
	url(r'^admin_home$', views.admin_home, name='admin_home'),
	url(r'^professor_home$', views.professor_home, name='professor_home'),
	url(r'^form_creator$', views.form_creator, name='form_creator'),
	url(r'^analytics_page$', views.analytics_page, name='analytics_page'),
	url(r'^professors_private_messages', views.professors_private_messages, name='professors_private_messages'),
	url(r'^prof_commentspage$', views.prof_commentspage, name='prof_commentspage'),
	url(r'^csv_download$', views.csv_download, name='csv_download'),
	url(r'^user_manual$', views.user_manual, name='user_manual'),
	url(r'^feedback_guidelines', views.feedback_guidelines, name='feedback_guidelines'),
) 