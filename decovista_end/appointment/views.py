from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # Import status
from .models import Consultation
from .serializers import ConsultationSerializer
from django.http import Http404

class ConsultationView(APIView):
    def get(self, request, format=None):
        consultations = Consultation.objects.all()
        serializer = ConsultationSerializer(consultations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ConsultationSerializer(data=request.data)
        if serializer.is_valid():  # Use the serializer to validate
            serializer.save()  # Save the serializer, not the model directly
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     

class ConsultationDetail(APIView):
    def get_object(self, pk):
        try:
            return Consultation.objects.get(pk=pk)
        except Consultation.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ConsultationSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer =ConsultationSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Consultation = self.get_object(pk)
        Consultation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
