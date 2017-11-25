"""food4all URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from store import views

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^$', views.index, name="index"),
                  url(r'^contact/', views.contact, name="contact"),
                  url(r'^profile/', views.profile, name="profile"),
                  url(r'^shop/(?P<url_name>\w+)/$', views.shop),
                  url(r'^wear/(?P<url_name>\w+)/$', views.wear),
                  url(r'^cart/(?P<url_name>\w+)/$', views.cart),
                  url(r'^checkout/', views.checkout, name="checkout"),
                  url(r'^adminpage/', views.adminpage, name="adminpage"),
                  url(r'^add_product/', views.add_product, name="add_product"),
                  url(r'^show_order/', views.show_order, name="show_order"),
                  url(r'^change/', views.change, name="change"),
                  url(r'^edit/(?P<edit_id>[0-9]+)/$', views.edit, name='edit'),
                  url(r'^prod_del/(?P<del_id>[0-9]+)/$', views.prod_del, name='prod_del'),
                  url(r'^comment/', views.comment, name="comment"),
                  url(r'^Adminreg/', views.Adminreg, name="Adminreg"),
                  url(r'^Adminlog/', views.Adminlog, name="Adminlog"),
                  url(r'^Adminlogout/', views.Adminlogout, name="Adminlogout"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
