from django.urls import path, include, re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # PAGES
    path('', views.start_test, name='start'),
    path("test_instructions/", views.test_instructions, name='test_instructions'),
    path("hello_template/", views.hello_template, name='helloTemplate'),
    # catchall path for receiving the hash of the user
    re_path(r"x/.*", views.evaluate_hash),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)