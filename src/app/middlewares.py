import hmac
import hashlib

from datetime import datetime
from typing import Dict, List, Tuple
from django.conf import settings
from app.utils.errors import error_response


def is_api_call(request):
    return getattr(request, 'path').split('/')[1] == 'api'


class SignatureAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if is_api_call(request):
            if not all([header in request.headers for header in ['X-Signature', 'X-Datetime']]):
                return error_response(
                    'unauthorized',
                    'The request has not been applied because there is no "X-Signature" or "X-Datetime" in the headers',
                    status=403,
                )
            
            url, method, query_params, headers = request.path, request.method, request.GET.dict(), request.headers
            
            request_send_datetime, error = self.__parse_to_datetime(headers['X-Datetime'], template='%Y%m%dT%H%M%S')
            
            if error:
                return error_response(
                    'unauthorized',
                    f'The "X-Datetime" header value can not be converted to datetime: {str(error)}',
                    status=400
                )
            
            if self.__is_expired(request_send_datetime, ttl=10):
                return error_response(
                    'unauthorized',
                    'Your "X-Signature" header expiration date has expired',
                    status=403,
                )
            
            received_signature = headers['X-Signature']
            
            custom_headers = {header: headers[header] for header in headers if header in settings.CUSTOM_HEADERS}
            valid_signature = self.__encrypt_signature(method, url, query_params, custom_headers)
            
            if valid_signature != received_signature:
                return error_response(
                    'unauthorized',
                    'The request has not been applied because it lacks valid authentication credentials for the target resource.',
                    status=403,
                )

        response = self.get_response(request)
        return response

    def __encrypt_signature(self, method: str, url: str, query_params: Dict[str, str], custom_headers: Dict[str, str]) -> str:
        query_for_signature = self.__get_canonical_str(self.__parse_dict_to_list_of_lines(query_params))
        headers_for_signature = self.__get_canonical_str(self.__parse_dict_to_list_of_lines(custom_headers))
        canonical_request = f'{method}\n{url}\n{query_for_signature}\n{headers_for_signature}'
        return hmac.new(str.encode(settings.API_SECRET), canonical_request.encode(), hashlib.sha256).hexdigest()

    @staticmethod
    def __parse_to_datetime(line: str, template: str) -> Tuple[datetime, None] | Tuple[None, ValueError]:
        try:
            return datetime.strptime(line, template), None
        except ValueError as err:
            return None, err

    @staticmethod
    def __is_expired(datetime: datetime, ttl: int) -> bool:
        return abs((datetime.utcnow() - datetime).total_seconds()) > ttl

    @staticmethod
    def __get_canonical_str(elements: List[str]) -> str:
        return '\n'.join(sorted(elements))

    @staticmethod
    def __parse_dict_to_list_of_lines(dict: Dict) -> List[str]:
        return [f'{key}:{value}' for key, value in dict.items()]
