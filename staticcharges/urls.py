from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/static_charge/', views.create_static_charge, name='create-static-charge'),
    path('success/', views.success, name='success'),
    path('static_charge/<id>/', views.view_static_charge, name='detail-static-charge'),
    path('callback/', csrf_exempt(views.callback), name="callback"),
    path('edit/<id>/', views.edit_static_charge, name='edit-static-charge'),
    path('.well-known/lnurlp/<username>', views.get_lightning_address, name='user_lightning_address')
]
