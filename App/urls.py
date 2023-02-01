from django.conf.urls import url
from . import views

urlpatterns = [
    url('catastro', views.Catastro.as_view(), name = 'catastro'),
    url(r'^$', views.Index.as_view(), name = 'index'),
]

# gestión de propiedades
urlpatterns += [
    url(r'^property/create/$', views.PropertyCreate.as_view(), name = 'property_create'),
    url(r'^property/created/$', views.CreateProperty.as_view(), name = 'create_property'),
    url(r'^property/(?P<pk>\d+)/delete/$', views.PropertyDelete.as_view(), name = 'property_delete'),
    url(r'^property/deleted/$', views.PropertyDeleted.as_view(), name = 'property_deleted'),
    url(r'^properties/unverified/$', views.UnverifiedProperties.as_view(), name = 'unverified_properties'),
    url(r'^property/verify/$', views.VerifyProperty.as_view(), name = 'verify_property'),
    url(r'^property/verified/$', views.PropertyVerified.as_view(), name = 'property_verified'),
    url(r'^property/(?P<catastral_reference>.+)/contact/$', views.PropertyContact.as_view(), name = 'property_contact'),
    url(r'^property/contacted/$', views.PropertyContacted.as_view(), name = 'property_contacted'),
]
