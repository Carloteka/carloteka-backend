from datetime import datetime, timedelta
from pprint import pprint

import httpx
from rest_framework import exceptions

from apps.shop.models import ShopContactsModel

HEADERS = {"Content-Type": "application/json"}


def check_date(date: datetime, days: int) -> bool:
    """
    Checking the expiration date
    :param date: Datetime of creation information
    :param days: expiration date in days (after that days should update date)
    :return:
    """
    if date:
        return True if date + timedelta(days=days) > datetime.now() else False


class NovaPoshtaClient:
    def __init__(
        self,
        api_key,
        api_endpoint="https://api.novaposhta.ua/v2.0/json/",
        timeout=10,
    ):
        self.http_client = httpx.Client
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.timeout = timeout
        # to cache in memory
        self.areas = {"created_at": datetime(2000, 1, 1), "data": {}}
        self.settlements = {}
        self.warehouses = {}

        self.sender_address = ""  # Ref Ідентифікатор відділення
        self.sender_warehouse_index = ""  # WarehouseIndex
        self.sender_phone = ""
        self.recipient = ""
        self.sender = ""
        self.contact_sender = ""

    def fill_info_about_sender(
        self,
        sender_address=None,
        sender_warehouse_index=None,
    ):
        """
        Fills in the necessary information to create an InternetDocument
        :param sender_address:  Ref Ідентифікатор відділення
        :param sender_warehouse_index: Цифрова адреса складу НП, де дані до слеша - це індекс населеного пункту,
                                        а після номер відділення/поштомату
        :return: None
        """
        contacts = ShopContactsModel.objects.all().first()

        if sender_address:
            contacts.sender_address = sender_address
            contacts.save()
        if sender_warehouse_index:
            contacts.sender_warehouse_index = sender_warehouse_index
            contacts.save()

        # if address is in DB - using it, else using default address to avoid errors
        if contacts.sender_address:
            self.sender_address = str(contacts.sender_address)
        else:
            self.sender_address = "731a002c-3ed2-11e6-a9f2-005056887b8d"
        if contacts.sender_warehouse_index:
            self.sender_warehouse_index = str(contacts.sender_warehouse_index)
        else:
            self.sender_warehouse_index = "11/12"

        properties = {"CounterpartyProperty": "Sender", "Page": "1"}
        sender = self.send("Counterparty", "getCounterparties", properties)
        self.sender = sender["data"][0]["Ref"]

        properties = {"CounterpartyProperty": "Recipient"}
        recipient = self.send("Counterparty", "getCounterparties", properties)
        self.recipient = recipient["data"][0]["Ref"]

        properties = {"Ref": self.sender, "Page": "1"}
        contact_sender = self.send(
            "Counterparty", "getCounterpartyContactPersons", properties
        )
        self.contact_sender = contact_sender["data"][0]["Ref"]
        self.sender_phone = contact_sender["data"][0]["Phones"]

    def send(
        self,
        model_name: str,
        called_method: str,
        method_props,
    ):
        """
        Sends request to the API.

        :param model_name: name of the model to use.
        :param called_method: name of the method to call.
        :param method_props: properties to pass to the method.
        :return: response dict.
        """
        data = {
            "apiKey": self.api_key,
            "modelName": model_name,
            "calledMethod": called_method,
            "methodProperties": method_props,
        }
        request = {
            "url": self.api_endpoint,
            "headers": HEADERS,
            "json": data,
            "timeout": self.timeout,
        }
        with self.http_client() as _client:
            pprint(request)
            response = _client.post(**request).json()
        if response["success"]:
            return response
        raise exceptions.NotFound({"detail": response["errors"]})

    def get_areas(self) -> dict:
        """
        Gets all the available areas
        :return:
        """
        if check_date(self.areas["created_at"], 30):
            return self.areas["data"]
        self.areas["data"] = self.send("Address", "getSettlementAreas", {})["data"]
        self.areas["created_at"] = datetime.now()
        return self.areas["data"]

    def get_settlements(
        self, area_ref: str, city_name: str | None = None
    ) -> list:  # for get_warehouses
        """
        Return list of settlements in the Area for getting list get_warehouses
        :param area_ref: Area identifier (REF) getting in get_areas
        :param city_name: City name or part of it
        :return: list of settlements
        """
        # checking availability in the cache and returning settlements if the expiration date has not expired
        if area_ref in self.settlements and not city_name:
            if check_date(self.settlements[area_ref]["created_at"], 30):
                return self.settlements[area_ref]["data"]

        # create or update settlements in the cache
        # get first part of settlements
        method_properties = {
            "AreaRef": area_ref,
            "FindByString": city_name,
            "Warehouse": "1",
            "Limit": "150",
            "Page": 1,
        }
        data = self.send("Address", "getSettlements", method_properties)
        _settlements: list = data["data"]

        # calculate count iteration to get all settlements
        iterations = data["info"]["totalCount"] // 150
        # get all date sending api requests if count of settlements > 150
        for i in range(2, int(iterations) + 2):
            method_properties["Page"] = i
            data = self.send("Address", "getSettlements", method_properties)
            _settlements.extend(data["data"])

        if not city_name:
            # save request to memory
            self.settlements[area_ref] = {"created_at": datetime.now()}
            self.settlements[area_ref]["data"] = _settlements
        return _settlements

    def get_warehouses(self, settlement_ref: str) -> list:
        """
        Get warehouse list in the city
        :param settlement_ref: Settlement identifier (REF) getting in get_areas
        :return:
        """
        if settlement_ref in self.warehouses:
            if check_date(self.warehouses[settlement_ref]["created_at"], 1):
                return self.warehouses[settlement_ref]["data"]

        # Поштове відділення
        method_properties = {
            "SettlementRef": settlement_ref,
            "Limit": "500",
            "TypeOfWarehouseRef": "841339c7-591a-42e2-8233-7a0a00f0ed6f",  # Поштове відділення
            "Page": 1,
        }
        data_post: dict = self.send("Address", "getWarehouses", method_properties)
        # Вантажне відділення
        method_properties = {
            "SettlementRef": settlement_ref,
            "Limit": "500",
            "TypeOfWarehouseRef": "9a68df70-0267-42a8-bb5c-37f427e36ee4",  # Вантажне відділення
            "Page": 1,
        }

        data_cargo: dict = self.send("Address", "getWarehouses", method_properties)
        data: list = data_post["data"] + data_cargo["data"]
        self.warehouses[settlement_ref] = {"created_at": datetime.now()}
        self.warehouses[settlement_ref]["data"] = data
        return self.warehouses[settlement_ref]["data"]

    def create_contact(
        self, first_name: str, middle_name: str, last_name: str, phone: str, email: str
    ) -> dict:
        """
        Create a new contact to send a package

        :return: dict with Ref and other contact information
        """
        method_properties = {
            "FirstName": first_name.capitalize(),
            "MiddleName": middle_name.capitalize(),
            "LastName": last_name.capitalize(),
            "Phone": str(phone),
            "Email": email,
            "CounterpartyType": "PrivatePerson",
            "CounterpartyProperty": "Recipient",
        }
        data = self.send("Counterparty", "save", method_properties)

        return data["data"][0]["ContactPerson"]["data"][0]

    def list_contacts(self):
        method_properties = {"Ref": "4188a0a8-1e1c-11e9-8b24-005056881c6b", "Page": "1"}
        data = self.send(
            "Counterparty", "getCounterpartyContactPersons", method_properties
        )
        return data["data"]

    def create_waybill(
        self,
        description,
        cost,
        volume_general,
        weight,
        recipient_contact,
        recipient_address,
        recipient_warehouse_index,
        recipient_phone,
    ):
        """
        Create Express-Waybill.

        :param description: description of the cargo
        :param cost: The cost of the cargo in UAH
        :param volume_general: Cargo volume in m^3
        :param weight: Cargo weight
        :param recipient_contact: Ref receiver from create_contact
        :param recipient_address: Ref warehouse from get_warehouses
        :param recipient_warehouse_index: index warehouse from get_warehouses
        :param recipient_phone: phone number receiver
        :return:
        """
        if not self.sender:
            self.fill_info_about_sender()  # fills sender attribute

        method_properties = {
            "Description": description,
            "Cost": str(cost),
            "VolumeGeneral": str(volume_general),
            "Weight": str(weight),
            "DateTime": (datetime.now() + timedelta(days=1)).strftime(
                "%d.%m.%Y"
            ),  # "18.02.2024",
            "PayerType": "Recipient",
            "PaymentMethod": "Cash",
            "CargoType": "Parcel",
            "ServiceType": "WarehouseWarehouse",
            "SeatsAmount": "1",
            "Sender": self.sender,
            "SenderAddress": self.sender_address,
            "SenderWarehouseIndex": self.sender_warehouse_index,
            "ContactSender": self.contact_sender,
            "SendersPhone": self.sender_phone,
            "Recipient": self.recipient,
            "RecipientAddress": str(recipient_address),
            "RecipientWarehouseIndex": recipient_warehouse_index,
            "ContactRecipient": str(recipient_contact),
            "RecipientsPhone": recipient_phone,
        }
        data = self.send("InternetDocument", "save", method_properties)
        return data["data"][0]

    def _get_warehouse_types(self):
        """Not used but may be needed"""
        method_properties = {}
        data = self.send("Address", "getWarehouseTypes", method_properties)
        return data["data"]

    def _get_cities(self, city_name: str) -> dict:  # for get_streets
        """Not used but may be needed"""
        """
        Return list of settlements in the Area for getting list get_street
        :param area_ref: Area identifier (REF)
        :return: list of cities
        """
        # checking availability in the cache and returning settlements if the expiration date has not expired

        method_properties = {"CityName": city_name, "Limit": "50", "Page": 1}
        data = self.send("Address", "searchSettlements", method_properties)
        return data

    def _get_streets(self, settlement_ref, street_name):
        """Not used but may be needed"""
        method_properties = {
            "StreetName": street_name,
            "SettlementRef": settlement_ref,
        }
        return self.send("Address", "searchSettlementStreets", method_properties)

    def _get_regions(self, area_ref):
        """Not used but may be needed"""
        method_properties = {
            "AreaRef": area_ref,
        }
        return self.send("Address", "getSettlementCountryRegion", method_properties)


"""
base_url = "https://api-stage.novapost.pl/v.1.0/"
params = {
            "apiKey": api,
        }
response = httpx.get(base_url+"clients/authorization/", params=params).json()
print (response['jwt'])
params = {
        "token": response['jwt'],
         "countryCodes[]": ["PL"],
        "limit": 1 # max 100 ?
        }
HEADERS = {"Content-Type": "application/json",  "Accept-language":"uk", "authorization": f"{response['jwt']}"}
response2  = httpx.get(base_url+"divisions/", params=params, headers=HEADERS).json()
{'current_page': 1,
 'from': None,
  'last_page': 24477,
 'per_page': 1,
 'to': None,
 'total': 24477,
 'items': [{'address': '50-231, Polska, Województwo dolnośląskie, Wrocław '
                       'County, Wrocław, Trzebnicka, 50/1A',
            'countryCode': 'PL',
            'createdAt': '2022-09-29T12:40:39.000000Z',
            'customerServiceAvailable': True,
            'deletedAt': None,
            'distance': None,
            'divisionCategory': 'PostBranch',
            'externalId': 'cf909742-1bee-4c97-8d0e-16de519c3220',
            'fullAddress': {'building': '50/1A',
                            'country': 'Poland',
                            'note': '',
                            'settlement': 'Wrocław',
                            'street': 'Trzebnicka',
                            'zipcode': '50-231'},
            'id': 1,
            'internalPhones': [],
            'latitude': 51.1271131131,
            'longitude': 17.0360840848,
            'maxCostPlace': 999999,
            'maxDeclaredCostPlace': 999999,
            'maxHeightPlaceRecipient': 1700,
            'maxHeightPlaceSender': 1700,
            'maxLengthPlaceRecipient': 3000,
            'maxLengthPlaceSender': 3000,
            'maxWeightPlaceRecipient': 200000,
            'maxWeightPlaceSender': 200000,
            'maxWidthPlaceRecipient': 1700,
            'maxWidthPlaceSender': 1700,
            'name': 'WROCŁAW 1',
            'number': '50/1',
            'ownerDivision': None,
            'partner': None,
            'prohibitedIssuance': False,
            'prohibitedSending': False,
            'publicPhones': [],
            'responsiblePerson': 'Dzhemesiuk Yaroslav',
            'settings': [{'createdAt': '2022-09-29T12:40:39.000000Z',
                          'deletedAt': None,
                          'divisionId': 1,
                          'from': '2024-01-18T13:43:16.000000Z',
                          'id': 52478,
                          'name': 'divisionsWithinOneLocation',
                          'to': '3023-01-18T13:43:16.000000Z',
                          'updatedAt': '2024-01-18T13:43:19.194386Z',
                          'value': '1860229'}],
            'settlement': {'id': 26061,
                           'name': 'Вроцлав',
                           'region': {'id': 344,
                                      'name': 'Wrocław County',
                                      'parent': {'id': 2,
                                                 'name': 'Нижньосілезьке '
                                                         'воєводство'}}},
            'shortName': 'WROCŁAW 1',
            'source': 'NPAX',
            'status': 'Working',
            'updatedAt': '2024-01-18T13:43:19.194386Z',
            'workSchedule': [{'breakFrom': None,
                              'breakTo': None,
                              'day': 'sunday',
                              'from': '09:00',
                              'to': '18:00'},
                             {'breakFrom': None,
                              'breakTo': None,
                              'day': 'monday',
                              'from': '08:00',
                              'to': '20:00'},
                             {'breakFrom': None,
                              'breakTo': None,
                              'day': 'tuesday',
                              'from': '08:00',
                              'to': '20:00'},
                             {'breakFrom': None,
                              'breakTo': None,
                              'day': 'wednesday',
                              'from': '08:00',
                              'to': '20:00'},
                             {'breakFrom': None,
                              'breakTo': None,
                              'day': 'thursday',
                              'from': '08:00',
                              'to': '20:00'},
                             {'breakFrom': None,
                              'breakTo': None,
                              'day': 'friday',
                              'from': '08:00',
                              'to': '20:00'},
                             {'breakFrom': None,
                              'breakTo': None,
                              'day': 'saturday',
                              'from': '09:00',
                              'to': '18:00'}]}]
}


"""
