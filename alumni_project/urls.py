from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from alumni import views as alumni_views
from django.contrib.sitemaps.views import sitemap
from alumni.sitemap import StaticViewSitemap, AlumniProfileSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'profiles': AlumniProfileSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', alumni_views.home, name='home'),
    path('register/', alumni_views.register, name='register'),
    path('verify-otp/', alumni_views.verify_otp, name='verify_otp'),
    path('login/', alumni_views.login_view, name='login'),
    path('login/verify-otp/', alumni_views.login_verify_otp, name='login_verify_otp'),
    path('logout/', alumni_views.logout_view, name='logout'),
    path('directory/', alumni_views.directory, name='directory'),
    path('directory/<int:profile_id>/', alumni_views.view_profile, name='view_profile'),
    path('directory/<int:profile_id>/edit/', alumni_views.edit_profile, name='edit_profile'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)