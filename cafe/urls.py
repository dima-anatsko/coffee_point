from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

from cafe.views import HomePageView, BasketEditView, OrderView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('basket-edit', BasketEditView.as_view(), name='basket-edit'),
    path('order', OrderView.as_view(), name='order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
