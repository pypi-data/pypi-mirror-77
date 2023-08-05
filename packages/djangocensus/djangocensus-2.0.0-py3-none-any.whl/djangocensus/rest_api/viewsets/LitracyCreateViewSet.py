from rest_framework.generics import CreateAPIView
from djangocensus.models.LitracyModel import LitracyModel
from djangocensus.rest_api.serializers import LitracySerializer


# Create viewset goes here.
class LitracyCreateViewSet(CreateAPIView):
    serializer_class = LitracySerializer
    queryset = LitracyModel.objects.all()