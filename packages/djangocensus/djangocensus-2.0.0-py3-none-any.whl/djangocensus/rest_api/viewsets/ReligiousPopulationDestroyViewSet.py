from rest_framework.generics import DestroyAPIView
from djangocensus.models.ReligiousPopulationModel import ReligiousPopulationModel
from djangocensus.rest_api.serializers import ReligiousPopulationSerializer


# Create viewset goes here.
class ReligiousPopulationDestroyViewSet(DestroyAPIView):
    serializer_class = ReligiousPopulationSerializer
    queryset = ReligiousPopulationModel.objects.all()
    lookup_field = "slug"
    lookup_url_kwarg = "slug"