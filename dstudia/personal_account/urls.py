from django.urls import path, include
from django.views.generic import RedirectView
from .views import *

application_control_urlpatterns = [
    path('', show_application_info, name='show_application_info'),
    path('delete/', delete_application, name='delete_application'),
    path('edit/', edit_application, name='edit_application')
]

application_urlpatterns = [
    path('create/', create_application, name='create_application'),
    path('list/', show_applications, name='show_applications'),
    path('<int:application_pk>/', include(application_control_urlpatterns)),
    path('management/', applications_management, name='applications_management'),
]

category_urlpatterns = [
    path('', category_page, name='category_page'),
    path('delete/<int:category_pk>/', delete_category, name='delete_category'),
]

account_urlpatterns = [
    path('', account_page, name='account_page'),
    path('logout/', logout_handler, name='logout_page'),
    path('application/', include(application_urlpatterns)),
    path('category/', include(category_urlpatterns)),
    path('no-access/', show_no_access, name='no_access'),
]

urlpatterns = [
    path('', main_page, name='main_page'),
    path('registration/', registration_handler, name='registration_page'),
    path('login/', login_handler, name='login_page'),
    path('account/', include(account_urlpatterns)),
]
