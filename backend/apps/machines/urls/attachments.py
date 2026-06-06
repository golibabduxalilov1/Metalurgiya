from django.urls import path
from rest_framework.generics import DestroyAPIView
from apps.machines.models import MachineAttachment
from utils.permissions import IsAdminOrMaster

class AttachmentDeleteView(DestroyAPIView):
    queryset = MachineAttachment.objects.all()
    permission_classes = [IsAdminOrMaster]

urlpatterns = [
    path('<int:pk>/', AttachmentDeleteView.as_view(), name='attachment-delete'),
]
