from django.conf.urls import url
from django.urls import path
from django.conf import settings
from first import views
from django.conf.urls.static import static
from django.views.generic import RedirectView

# SET THE NAMESPACE!
app_name = 'first'


urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    path('', views.home, name='home'),
    path('<int:note_id>/', views.detail, name='detail'),
    path('add_note/',views.add_note_button, name='add_note_button'),
    path('post/new/', views.post_new, name='post_new'),
    path('<int:note_id>/remove/', views.delete_note, name='delete_note'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicons/favicon.ico', permanent=True), name='favicon'),

    url(r'^get_notes/(?P<username>\w+)/$',views.NoteList.as_view()),

    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    path('calendar/', views.calendar_button, name='calendar_button'),
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),

    #path('upload/<username>/', views.upload, name='upload'),
    #path('files/', views.book_list, name='book_list'),
    path('files/', views.book_list, name='book_list'),
    path('files/upload/', views.upload_book, name='upload_book'),
    path('files/<int:pk>/', views.delete_book, name='delete_book'),

    path('about/', views.about_us, name='about_us'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
