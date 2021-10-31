from django.contrib import admin
from django.urls import (
    include,
    path,
)

from github_projects_tracker import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

if settings.DEBUG and settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),