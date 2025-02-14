"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from django.urls import include, re_path

from apps.women.views import page_not_found

# from apps.women.views import WomenAPIView
from apps.women.views import WomenAPIList, WomenAPIUpdate, WomenAPIDestroyView

# from apps.women.views import WomenViewSet

# from rest_framework import routers
# # router = routers.SimpleRouter() # создаем обьект класса роутер
# router = routers.DefaultRouter() #
# router.register(r"women", WomenViewSet, basename="woman")  #регистрация класса  вьюсета
# print(router.urls)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("api/v1/drf_auth/", include("rest_framework.urls")),  # подключение маршрутов drf
    path("user/", include("apps.user.urls")),
    path("about/", include("apps.base.urls")),
    path("", include("apps.base.urls_root")),
    path("women/", include("apps.women.urls")),
    path("captcha/", include("captcha.urls")),
    # path("api/v1/", include(router.urls)),
    # path("api/v1/womenlist/", WomenViewSet.as_view({"get": "list"})),
    # path("api/v1/womenlist/<int:pk>/", WomenViewSet.as_view({"put": "update"})),
    path("api/v1/women/", WomenAPIList.as_view()),
    path("api/v1/women/<int:pk>/", WomenAPIUpdate.as_view()),
    path("api/v1/womendelete/<int:pk>/", WomenAPIDestroyView.as_view()),
    path("api/v1/auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

handler404 = page_not_found

if settings.DEBUG:
    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
