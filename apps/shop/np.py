from datetime import datetime, timedelta
from pprint import pprint

import httpx
from rest_framework import exceptions

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

    def get_warehouses(self, settlement_ref: str) -> dict:
        """
        Get warehouse list in the city
        :param settlement_ref: Settlement identifier (REF) getting in get_areas
        :return:
        """
        if settlement_ref in self.warehouses:
            if check_date(self.warehouses[settlement_ref]["created_at"], 1):
                return self.warehouses[settlement_ref]["data"]
        method_properties = {
            "SettlementRef": settlement_ref,
            "Limit": "500",
            "TypeOfWarehouseRef": "841339c7-591a-42e2-8233-7a0a00f0ed6f",
            "Page": 1,
        }
        data = self.send("Address", "getWarehouses", method_properties)
        self.warehouses[settlement_ref] = {"created_at": datetime.now()}
        self.warehouses[settlement_ref]["data"] = data["data"]
        return self.warehouses[settlement_ref]["data"]

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
