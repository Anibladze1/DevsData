from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from django.views.generic import (ListView, DeleteView, DetailView)

from .forms import ReservationForm
from .models import Event, Reservation
from .serializers import EventSerializer, ReservationSerializer


# Administration Interface for Events
# Admins can delete events that start in more than two days
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        if (event.start_date - timezone.now()).days > 2:
            return Response({"message": "Cannot delete event that starts in more than two days."}, status=400)
        event.delete()
        return Response({"message": "Event deleted successfully."}, status=204)


# Administration Interface for Reservations
# Admins can delete reservations for events that start in more than two days
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def destroy(self, request, *args, **kwargs):
        reservation = self.get_object()
        event = reservation.event
        if (event.start_date - timezone.now()).days > 2:
            return Response({"message": "Cannot delete reservation for an event that starts in more than two days."},
                            status=400)
        reservation.delete()
        return Response({"message": "Reservation deleted successfully."}, status=204)


# User Interface for Events
# Users can see all events
class EventListView(ListView):
    model = Event
    template_name = "event/event_list.html"
    context_object_name = "events"


# Users can see details of an event
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.event = event
            reservation.save()
            return redirect('reservation_detail', pk=reservation.pk)

    else:
        form = ReservationForm()
    return render(request, 'event/event_detail.html', {'event': event, 'form': form})


# Users can see details of a reservation
class ReservationDetailView(DetailView):
    model = Reservation
    template_name = "event/reservation_detail.html"
    context_object_name = "reservation"


# Users can delete their reservations
def delete_reservation(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        reservation = get_object_or_404(Reservation, code=code)
        reservation.delete()
        return redirect('deleted')
    return render(request, 'event/delete_reservation.html')


def deleted(request):
    return render(request, 'event/deleted.html')
