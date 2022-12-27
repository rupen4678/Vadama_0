from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

app_name = 'home'

urlpatterns = [
    path('', home_page, name='home'),
    path('login/', Login_form, name="login"),
    path('logout/', logout_form, name="logout"),
    path('register/', register_form, name="register"),
    path('product/<int:pk>/', productDetail, name='pdetail'),
    path('product/delete/<int:pk>/', productDelete, name='ddetail'),
    path('addproduct/', addProduct, name='padd'),
    path('profile/', profile, name='users-profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT
                          )
