from rest_framework.serializers import ModelSerializer
from .models import Consultation


class ConsultationSerializer(ModelSerializer):
    
    class Meta:
        model = Consultation
        felids = "__all__"
        