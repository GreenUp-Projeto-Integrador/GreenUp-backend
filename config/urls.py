from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from apps.disposals.views import RankingView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.accounts.auth_urls")),
    path("api/v1/users/", include("apps.accounts.urls")),
    path("api/v1/collection-points/", include("apps.collection_points.urls")),
    path("api/v1/disposals/", include("apps.disposals.urls")),
    path("api/v1/ranking/", RankingView.as_view(), name="ranking"),
    path("api/v1/notifications/", include("apps.notifications.urls")),
    path("api/v1/dashboard/", include("apps.analytics.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
