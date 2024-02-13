from os import getenv

from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .np import NovaPoshtaClient
from apps.core.exceptions import ErrorSerializer404


NP_API_KEY = getenv('NP_API_KEY')  # api key for nova poshta
np = NovaPoshtaClient(NP_API_KEY)


class AreasAPI(APIView):
    class OutputSerializer(serializers.Serializer):
        Ref = serializers.UUIDField()
        Description = serializers.CharField(max_length=255)
        RegionType = serializers.CharField(max_length=255)

    @extend_schema(
        tags=["NP"],
        summary="Get list of all Areas",
        description="Get list of all Areas (областей)",
        responses={
            200: OutputSerializer,
            404: ErrorSerializer404,
        },
    )
    def get(self, request):
        areas = np.get_areas()
        serializer = AreasAPI.OutputSerializer(data=areas, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class SettlementsAPI(APIView):
    class InputSerializer(serializers.Serializer):
        Ref = serializers.UUIDField()
        city_name = serializers.CharField(max_length=255, required=False)

    class OutputSettlementsSerializer(serializers.Serializer):
        Ref = serializers.UUIDField()
        Description = serializers.CharField(max_length=255)
        SettlementTypeDescription = serializers.CharField(max_length=255)
        RegionsDescription = serializers.CharField(max_length=255, allow_blank=True)
        AreaDescription = serializers.CharField(max_length=255)

    @extend_schema(
        tags=["NP"],
        summary="Get list of Settlements",
        description="Get the list of Ukrainian cities to which goods are delivered by the 'Nova Poshta' company.",
        parameters=[
            OpenApiParameter(
                name="Ref",
                location=OpenApiParameter.QUERY,
                description="Ref",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="city_name",
                location=OpenApiParameter.QUERY,
                description="City name",
                required=False,
                type=str,
            ),
        ],
        responses={
            200: OutputSettlementsSerializer,
            400: status.HTTP_400_BAD_REQUEST,
            404: ErrorSerializer404,
        },
    )
    def get(self, request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        area_ref = str(serializer.validated_data["Ref"])
        city_name = serializer.validated_data.get("city_name")
        settlements = np.get_settlements(area_ref, city_name)
        output_serializer = self.OutputSettlementsSerializer(
            data=settlements, many=True
        )
        output_serializer.is_valid(raise_exception=True)
        return Response(output_serializer.validated_data)


class WarehousesAPI(APIView):
    class InputSerializer(serializers.Serializer):
        SettlementRef = serializers.UUIDField()

    class OutputWarehousesSerializer(serializers.Serializer):
        Ref = serializers.UUIDField()
        Description = serializers.CharField(max_length=255)
        Number = serializers.CharField(max_length=255, allow_blank=True)

    @extend_schema(
        tags=["NP"],
        summary="Get list of warehouses in city",
        description="Get list of all warehouses in city. Use Ref from '/api/shop/np/settlements/'. ",
        parameters=[
            OpenApiParameter(
                name="SettlementRef",
                location=OpenApiParameter.QUERY,
                description="SettlementRef",
                required=True,
                type=str,
            ),
        ],
        responses={
            200: OutputWarehousesSerializer,
            400: status.HTTP_400_BAD_REQUEST,
            404: ErrorSerializer404,
        },
    )
    def get(self, request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        settlement_ref = str(serializer.validated_data["SettlementRef"])

        warehouses = np.get_warehouses(settlement_ref)
        output_serializer = self.OutputWarehousesSerializer(data=warehouses, many=True)
        output_serializer.is_valid(raise_exception=True)
        return Response(output_serializer.validated_data)

