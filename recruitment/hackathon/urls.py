from django.urls import path, include, re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # PAGES
    path('', views.start_test, name='start'),
    path('fluidai_admin/',views.start_admin, name='start_admin'),
    path("fluidai_admin/admin_check/", views.admin_check, name='admin_check'),
	path("admin_license/key_operation/", views.key_operation, name='add_key'),
	path("admin_license/", views.admin_license, name='admin_license'),
    path("test_instructions/", views.test_instructions, name='test_instructions'),
    path("hello_template/", views.hello_template, name='helloTemplate'),
    path("admin_dash/", views.admin_dash, name='admin_dash'),
	path("admin_data/", views.admin_data, name='admin_data'),
    # catchall path for receiving the hash of the user
    re_path(r"x/.*", views.evaluate_hash),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)