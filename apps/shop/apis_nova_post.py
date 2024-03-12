import urllib.request
from os import getenv

from django.http import FileResponse
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.exceptions import ErrorSerializer404

from .np import NovaPoshtaClient

NP_API_KEY = getenv("NP_API_KEY")  # api key for nova poshta
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
        WarehouseIndex = serializers.CharField(max_length=255, allow_blank=True)

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


class CreateContactAPI(APIView):
    class InputCreateContactSerializer(serializers.Serializer):
        first_name = serializers.CharField(max_length=255)
        last_name = serializers.CharField(max_length=255)
        phone = serializers.CharField(max_length=12)
        email = serializers.EmailField()

        def validate_phone(self, phone):
            if (
                len(phone) != len("380685280269")
                or not phone.startswith("380")
                or not phone.isdigit()
            ):
                raise serializers.ValidationError(
                    "phone number must be like 380985280211"
                )
            return phone

    class OutputCreateContactSerializer(serializers.Serializer):
        Ref = serializers.UUIDField()
        Description = serializers.CharField(max_length=255)
        LastName = serializers.CharField(max_length=255)
        FirstName = serializers.CharField(max_length=255)

    @extend_schema(
        tags=["NP"],
        summary="Create contact",
        description="Прізвище, імїя, побатькові виключно українською мовою.",
        request=InputCreateContactSerializer,
        responses={
            201: OutputCreateContactSerializer,
            400: status.HTTP_400_BAD_REQUEST,
            404: ErrorSerializer404,
        },
    )
    def post(self, request):
        serializer = self.InputCreateContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = np.create_contact(**serializer.validated_data)
        return Response(contact, status=status.HTTP_201_CREATED)


class ListContactsAPI(APIView):
    @extend_schema(
        tags=["NP"],
        summary="List all contacts",
        description="List all contacts.",
        responses={
            # 201: OutputCreateContactSerializer,
            400: status.HTTP_400_BAD_REQUEST,
            404: ErrorSerializer404,
        },
    )
    def get(self, request):
        contacts = np.list_contacts()
        return Response(contacts)


class CreateWaybillAPI(APIView):
    class InputCreateWaybillSerializer(serializers.Serializer):
        description = serializers.CharField(max_length=255)
        cost = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=0.01)
        volume_general = serializers.DecimalField(
            max_digits=6, decimal_places=5, min_value=0.00001
        )
        weight = serializers.DecimalField(
            max_digits=7, decimal_places=5, min_value=0.00001
        )
        recipient_contact = serializers.UUIDField()
        recipient_address = serializers.UUIDField()
        recipient_warehouse_index = serializers.CharField(max_length=255)
        recipient_phone = serializers.CharField(max_length=12)

        def validate_cost(self, cost):
            if cost <= 0:
                raise serializers.ValidationError("cost must be positive")
            return cost

        def validate_recipient_phone(self, recipient_phone):
            if (
                len(recipient_phone) != len("380965280211")
                or not recipient_phone.startswith("380")
                or not recipient_phone.isdigit()
            ):
                raise serializers.ValidationError(
                    "phone number must be like 380985280211"
                )
            return recipient_phone

    class OutputCreateWaybillSerializer(serializers.Serializer):
        int_doc_number = serializers.IntegerField(min_value=1)
        cost_on_site = serializers.IntegerField()
        estimated_delivery_date = serializers.DateField(format="%d.%m.%Y")
        ref = serializers.UUIDField()


    @extend_schema(
        tags=["NP"],
        summary="Create waybill",
        description="create waybill. volume_general - Об'єм вантажу в м^3, weight - Вага вантажу",
        request=InputCreateWaybillSerializer,
        responses={
            201: OutputCreateWaybillSerializer,
            400: status.HTTP_400_BAD_REQUEST,
            404: ErrorSerializer404,
        },
    )
    def post(self, request):
        serializer = self.InputCreateWaybillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        waybill = np.create_waybill(**serializer.validated_data)
        data = {
            "ref": waybill["Ref"],
            "int_doc_number": waybill["IntDocNumber"],
            "cost_on_site": waybill["CostOnSite"],
            "estimated_delivery_date": waybill["EstimatedDeliveryDate"]
        }
        return Response(data, status=status.HTTP_201_CREATED)


class PrintWaybillAPI(APIView):
    @extend_schema(
        tags=["NP"],
        summary="print waybill",
        description="print waybill",
        responses={
            200: OpenApiResponse(description="Pdf file"),
        },
    )
    def get(self, request, waybill_number):
        url = f"https://my.novaposhta.ua/orders/printDocument/orders[]/{waybill_number}/type/pdf/apiKey/{NP_API_KEY}"
        file = urllib.request.urlopen(url)
        return FileResponse(file, as_attachment=True, filename=f"{waybill_number}.pdf")


class SetSenderAdressAPI(APIView):
    class InputSetSenderAdressSerializer(serializers.Serializer):
        sender_address = serializers.UUIDField()
        sender_warehouse_index = serializers.CharField(max_length=255)

    @extend_schema(
        tags=["NP"],
        summary="Set sender address",
        description="Set sender address(Ref and Index warehouse)",
        request=InputSetSenderAdressSerializer,
        responses={
            200: OpenApiResponse(),
            404: ErrorSerializer404,
        },
    )
    def post(self, request):
        serializer = self.InputSetSenderAdressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        np.fill_info_about_sender(**serializer.validated_data)
        return Response(status=status.HTTP_200_OK)
