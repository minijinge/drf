"""drf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
# from rest_framework_swagger.views import get_swagger_view

from drf.settings import MEDIA_ROOT


# schema_view = get_swagger_view(title='Pastebin API')
schema_view = get_schema_view(
   openapi.Info(
      title="DRF框架API接口文档",
      default_version='v1.0',
      description="DRF框架API接口文档",
      terms_of_service="127.0.0.1:8000/redoc",
      contact=openapi.Contact(email="kdhy@163.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # apps
    path('users/', include('users.urls')),

    # media资源路由配置
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # rest_framework 自带登录/登出 路由,Session Authentication,你可以访问：http://127.0.0.1:8000/api-auth/login/
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # jwt的认证接口 适用于前后端分离 不要携带敏感信息
    # 获取jwt token（这里用到了django的api-auth认证，也就是用户名密码认证）
    re_path(r'^jwt/login/$', obtain_jwt_token),

    # swagger
    # re_path(r'^swagger', schema_view),

    # 配置drf-yasg路由
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # docs文档
    path(r'docs/', include_docs_urls(title='DRF接口API')),

    path('admin/', admin.site.urls),
]
