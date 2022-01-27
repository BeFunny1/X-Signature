import hmac
import hashlib

from datetime import datetime
from typing import Dict, List, Tuple


class XSignatureGenerator:
    def generate_headers(self, api_secret_key: str, method: str, url: str, query_params: Dict[str, str],
                         headers: Dict[str, str], with_x_datetime: bool) -> Tuple[str, str]:
        x_datetime = datetime.strftime(datetime.utcnow(), '%Y%m%dT%H%M%S') if with_x_datetime else None
        x_signature = self._generate_signature(
            api_secret_key,
            method,
            url,
            query_params,
            headers if not with_x_datetime else dict(**headers, **{'X-Datetime': x_datetime})
        )
        return x_datetime, x_signature

    def _generate_signature(self, api_secret_key: str, method: str, canonical_url: str,
                            query_params: Dict[str, str], headers: Dict[str, str]) -> str:
        query_for_signature = self._get_canonical_str(self._parse_dict_to_list_of_lines(query_params))
        headers_for_signature = self._get_canonical_str(self._parse_dict_to_list_of_lines(headers))
        canonical_request = f'{method}\n{canonical_url}\n{query_for_signature}\n{headers_for_signature}'
        return hmac.new(str.encode(api_secret_key), canonical_request.encode(), hashlib.sha256).hexdigest()

    @staticmethod
    def _parse_dict_to_list_of_lines(dict: Dict) -> List[str]:
        return [f'{key}:{value}' for key, value in dict.items()]

    @staticmethod
    def _get_canonical_str(elements: List) -> str:
        return '\n'.join(sorted(elements))


if __name__ == '__main__':
    pass
