from rest_framework import serializers


DEFAULT_400_EXCEPTION_DETAIL = ""
DEFAULT_401_EXCEPTION_DETAIL = ""
DEFAULT_403_EXCEPTION_DETAIL = ""
DEFAULT_404_EXCEPTION_DETAIL = "Not Found"
DEFAULT_429_EXCEPTION_DETAIL = ""


class ErrorSerializer404(serializers.Serializer):
    detail = serializers.CharField(default=DEFAULT_404_EXCEPTION_DETAIL)
