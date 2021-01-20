from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from works.serializers import WorkSerializer
from works.models import Work


class WorkViewSet(ModelViewSet):
    """Work viewset Definition"""
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        """ Create a new recipe """
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(user=self.request.user)
