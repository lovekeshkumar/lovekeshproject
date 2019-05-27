from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login),
    path('signup/', views.signup),
    path('scan/', views.scan_qr),
    path('img-to-text/', views.img_to_text),
]
