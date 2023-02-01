from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from App import views

#admin
urlpatterns = [
    path('admin/', admin.site.urls),
]

# redirecciones a el corredor
urlpatterns += [
    path('el-corredor/', include('App.urls')),
    path('', RedirectView.as_view(url='/el-corredor/', permanent = True)),
    path('accounts/', include('django.contrib.auth.urls')),
]

# gestión de usuarios
urlpatterns += [
    url(r'^user/create/$', views.UserCreate.as_view(), name = 'user_create'),
    url(r'^user/created/$', views.CreateUser.as_view(), name = 'create_user'),
    url(r'^user/profile/$', views.UserProfile.as_view(), name = 'user_profile'),
    url(r'^user/profile/email_update/$', views.EmailUpdateRequest.as_view(), name = 'email_update_request'),
    url(r'^user/profile/email_update/requested/$', views.EmailUpdateRequested.as_view(), name = 'email_update_requested'),
    url(r'^user/(?P<pk>\d+)/update/$', views.UserUpdate.as_view(), name = 'user_update'),
    url(r'^user/(?P<pk>\d+)/delete/$', views.UserDelete.as_view(), name = 'user_delete'),
    url(r'^user/deleted/$', views.UserDeleted.as_view(), name = 'user_deleted'),
    url(r'^user/unverified/$', views.UserUnverified.as_view(), name = 'user_unverified'),
    url(r'^accounts/logged_in/$', views.LoggedIn.as_view(), name = 'logged_in'),
    url(r'^accounts/logged_out/$', views.LoggedOut.as_view(), name = 'logged_out'),
    url(r'^accounts/password_reset/request/$', views.PasswordResetRequest.as_view(), name = 'password_reset_request'),
    url(r'^accounts/password_reset/(?P<token>.+)/$', views.PasswordResetConfirm.as_view(), name = 'password_reset_confirm_token'),
    url(r'^accounts/email_verification/$', views.EmailVerificationRequest.as_view(), name = 'email_verification_request'),
    url(r'^accounts/email_verification/requested/$', views.EmailVerificationRequested.as_view(), name = 'email_verification_requested'),
    url(r'^accounts/verify_email/(?P<token>.+)/$', views.VerifyEmail.as_view(), name = 'verify_email'),
    url(r'^accounts/email_verified/$', views.EmailVerified.as_view(), name = 'email_verified'),
]

# static urls
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

