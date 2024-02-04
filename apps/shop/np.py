from datetime import datetime, timedelta
from pprint import pprint

import httpx

HEADERS = {"Content-Type": "application/json"}


def check_date(date: datetime, days: int) -> bool:
    """
    Checking the expiration date
    :param date: Datetime of creation information
    :param days: expiration date in days
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
        self.cities = {}
        self.warehouses = {}

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
            response = _client.post(**request)
        return response.json()

    def get_areas(self) -> dict:
        """
        Gets all the available areas
        :return:
        """
        if check_date(self.areas["created_at"], 30):
            return self.areas["data"]
        print("send api request get_areas")
        self.areas["data"] = self.send("Address", "getSettlementAreas", {})["data"]
        self.areas["created_at"] = datetime.now()
        return self.areas["data"]

    def get_settlements(self, area_ref: str, name: str) -> dict:  # for get_warehouses
        """
        Return list of settlements in the Area for getting list get_warehouses
        :param area_ref: Area identifier (REF)
        :return: list of settlements
        """
        # checking availability in the cache and returning settlements if the expiration date has not expired
        if area_ref in self.settlements:
            if check_date(self.settlements[area_ref]["created_at"], 30):
                return self.settlements[area_ref]["data"]
        # create or update settlements in the cache
        # get first part of settlements
        method_properties = {
            "AreaRef": area_ref,
            "FindByString": name,
            "Warehouse": "1",
            "Limit": "150",
            "Page": 1,
        }
        data = self.send("Address", "getSettlements", method_properties)

        self.settlements[area_ref] = {"created_at": datetime.now()}
        self.settlements[area_ref]["data"] = data["data"]
        # calculate count iteration to get all settlements
        iterations = data["info"]["totalCount"] // 150
        for i in range(2, int(iterations) + 2):
            method_properties["Page"] = i
            data = self.send("Address", "getSettlements", method_properties)
            self.settlements[area_ref]["data"].extend(data["data"])

        return self.settlements[area_ref]["data"]

    def get_warehouses(self, city_ref):
        if city_ref in self.warehouses:
            if check_date(self.warehouses[city_ref]["created_at"], 1):
                return self.warehouses[city_ref]["data"]
        method_properties = {
            "SettlementRef": city_ref,
            "Limit": "500",
            "TypeOfWarehouseRef": "841339c7-591a-42e2-8233-7a0a00f0ed6f",
            "Page": 1,
        }
        data = self.send("Address", "getWarehouses", method_properties)
        self.warehouses[city_ref] = {"created_at": datetime.now()}
        self.warehouses[city_ref]["data"] = data["data"]
        return self.warehouses[city_ref]["data"]

    def getWarehouseTypes(self):
        method_properties = {}
        data = self.send("Address", "getWarehouseTypes", method_properties)
        return data["data"]

    def get_cities(self, CityName: str) -> dict:  # for get_streets
        """
        Return list of settlements in the Area for getting list get_street
        :param area_ref: Area identifier (REF)
        :return: list of cities
        """
        # checking availability in the cache and returning settlements if the expiration date has not expired

        method_properties = {"CityName": CityName, "Limit": "50", "Page": 1}
        data = self.send("Address", "searchSettlements", method_properties)
        return data

    def get_streets(self, SettlementRef, StreetName):
        method_properties = {
            "StreetName": StreetName,
            "SettlementRef": SettlementRef,
        }
        return self.send("Address", "searchSettlementStreets", method_properties)

    def get_regions(self, area_ref):
        method_properties = {
            "AreaRef": area_ref,
        }
        return self.send("Address", "getSettlementCountryRegion", method_properties)
