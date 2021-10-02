from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from webemploy import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # * Authentication
    path('auth/', include('authentication.urls')),

    # Posts
    path('', include('Posts.urls',)),

    # Question
    path('', include('Questions.urls')),

]
if settings.DEBUG:
    # add media static files
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)