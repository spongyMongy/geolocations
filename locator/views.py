import requests
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.request import Request

from .models import Locations
from .serializers import LocationSerializer, SignUpSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.conf import settings


class ConnectionCreator:
    permission_classes = (IsAuthenticated,)

    def __init__(self, request, **kwargs):
        self.request = request
        self.ip_is = kwargs.get('ip_is')

    def create_connection(self):
        if self.ip_is is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        requested_url = f'http://api.ipstack.com/{self.ip_is}?access_key=' \
                        f'{settings.IP_STACK_KEY}'

        response = requests.get(requested_url)
        geodata = response.json()
        return {'geodata': geodata, 'response_status': response.status_code}


class LocalizationListApiView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LocationSerializer

    def get(self, request, *args, **kwargs):
        ip_is = request.GET.get('ip')
        try:
            # data checking through the db
            query_result = Locations.objects.filter(ip=ip_is)
        except:
            pass

        serializer = LocationSerializer(query_result, many=True)

        if query_result.count() != 0:
            # it means we posted it before, it is already  in our db
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            returned_data = ConnectionCreator(request=request,
                                              ip_is=ip_is) \
                .create_connection()
            if returned_data.get('response_status') != 200:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST)

            serializer = LocationSerializer(returned_data.get('geodata'),
                                            many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        returned_data = ConnectionCreator(request=request,
                                          ip_is=request.data['ip']). \
            create_connection()
        serializer = LocationSerializer(data=returned_data.get('geodata'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        ip_address = request.data.get('ip')
        try:
            unwanted_ip = Locations.objects.get(ip=ip_address)
            unwanted_object = get_object_or_404(Locations,
                                                pk=unwanted_ip.id)
            unwanted_object.delete()
        except:
            pass
        return Response(status=204)


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {"message": "User Created Successfully",
                        "data": serializer.data}
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
