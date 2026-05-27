# transit/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from transit.views.health      import health_check
from transit.views.auth        import RegisterView, LogoutView
from transit.views.user        import UserViewSet
from transit.views.ruta        import RutaViewSet
from transit.views.parada      import ParadaViewSet
from transit.views.viaje       import ViajeViewSet
from transit.views.bus         import BusViewSet
from transit.views.chofer      import ChoferViewSet
from transit.serializers.auth  import CustomTokenView

router = DefaultRouter()
router.register('users',       UserViewSet,     basename='user')
router.register('buses',       BusViewSet,      basename='bus')
router.register('choferes',    ChoferViewSet,   basename='chofer')
router.register('rutas',       RutaViewSet,     basename='ruta')
router.register('paradas',     ParadaViewSet,   basename='parada')
router.register('viajes',      ViajeViewSet,    basename='viaje')

urlpatterns = [
    path('health/',             health_check),
    path('auth/register/',      RegisterView.as_view()),
    path('auth/login/',         CustomTokenView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/token/verify/',  TokenVerifyView.as_view()),
    path('auth/logout/',        LogoutView.as_view()),
    path('', include(router.urls)),
]