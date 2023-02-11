from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'reservations', views.ReservationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path("", views.EventListView.as_view(), name="event_list"),
    path("<int:pk>/", views.event_detail, name="event_detail"),
    path("reservation/<int:pk>/", views.ReservationDetailView.as_view(), name="reservation_detail"),
    path("reservation/delete/", views.delete_reservation, name="delete_reservation"),
    path("deleted/confirm/", views.deleted, name="deleted")
]
