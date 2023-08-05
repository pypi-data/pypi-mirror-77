from rest_framework.generics import RetrieveUpdateAPIView
from djangocensus.models.VillageModel import VillageModel
from djangocensus.rest_api.serializers import VillageSerializer


# Create viewset goes here.
class VillageRetrieveUpdateViewSet(RetrieveUpdateAPIView):
    serializer_class = VillageSerializer
    queryset = VillageModel.objects.all()
    lookup_field = "slug"
    lookup_url_kwarg = "slug"