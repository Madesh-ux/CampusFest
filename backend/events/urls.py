from django.urls import path
from .views import EventListView,EventDetailView,IndividualRegistrationView,TeamRegistrationView

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('register/individual/',IndividualRegistrationView.as_view(),name='individual-registration'),
    path('register/team/',TeamRegistrationView.as_view(),name='team-registration'),
]