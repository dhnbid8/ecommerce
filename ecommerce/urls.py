from django.contrib import admin
from django.urls import path, include, re_path
from azbankgateways.urls import az_bank_gateways_urls
from django.urls import re_path as url


from ecommerce import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view


schema_view = get_swagger_view(title='Pastebin API',url='/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api/', include('product.urls')),
    path('api/', include('card.urls')),
    path('api/', include('checkout.urls')),
    path('bankgateways/', az_bank_gateways_urls()),
    path('account/', include('account.urls')),
    # re_path(r'doc/', schema_view)
    url('doc/', schema_view),
    # path('docs/', TemplateView.as_view(
    #     template_name='doc.html',
    #     extra_context={'schema_url':'openapi-schema'}
    # ), name='swagger-ui'),
    path('openapi/', get_schema_view(
        title="School Service",
        description="API developers hpoing to use our service"
    ), name='openapi-schema'),
    


]

if settings.DEBUG :
    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    )
