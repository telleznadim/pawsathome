from django.urls import path
from . import views
from .views import JobRequestCreateView, JobRequestInboxView, JobRequestOutboxView, JobRequestStatusUpdateView

urlpatterns = [
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/add/', views.add_pet, name='add_pet'),
    path('pets/<int:pk>/edit/', views.edit_pet, name='edit_pet'),
    path('pets/<int:pk>/delete/', views.delete_pet, name='delete_pet'),
    path('sitters/', views.sitter_list, name='sitter_list'),
    path('request-job/<int:sitter_id>/',
         JobRequestCreateView.as_view(), name='request_job'),
    path('jobs/inbox/', JobRequestInboxView.as_view(), name='job_inbox'),
    path('jobs/outbox/', JobRequestOutboxView.as_view(), name='job_outbox'),
    path('job/<int:pk>/update-status/',
         JobRequestStatusUpdateView.as_view(), name='update_job_status'),
]
