from rest_framework.generics import CreateAPIView
from djangocensus.models.ReligionModel import ReligionModel
from djangocensus.rest_api.serializers import ReligionSerializer


# Create viewset goes here.
class ReligionCreateViewSet(CreateAPIView):
    serializer_class = ReligionSerializer
    queryset = ReligionModel.objects.all()