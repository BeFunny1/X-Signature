import json
import hmac
import hashlib

from datetime import datetime
from typing import Dict, List


def parse_dict_to_list_of_lines(dict: Dict) -> List[str]:
    return [f'{key}:{value}' for key, value in dict.items()]


def get_canonical_str(elements: List) -> str:
    return '\n'.join(sorted(elements))


def generate_signature(api_secret_key: str, method: str, canonical_url: str, query_params: Dict[str, str], headers: Dict[str, str]) -> str:
    query_for_signature = get_canonical_str(parse_dict_to_list_of_lines(query_params))
    headers_for_signature = get_canonical_str(parse_dict_to_list_of_lines(headers))
    canonical_request = f'{method}\n{canonical_url}\n{query_for_signature}\n{headers_for_signature}'
    return hmac.new(str.encode(api_secret_key), canonical_request.encode(), hashlib.sha256).hexdigest()


if __name__ == '__main__':
    data = {}
    with open('./data.json', 'r') as file:
        data = json.loads(file.read())

    with_x_datetime = data['with_x_datetime']
    x_datetime = datetime.strftime(datetime.utcnow(), '%Y%m%dT%H%M%S') if with_x_datetime else None    
    
    x_signature = generate_signature(
        data['API_SECRET_KEY'],
        data['method'],
        data['canonical_url'],
        data['query_params'],
        data['headers'] if not with_x_datetime else dict(**data['headers'], **{'X-Datetime': x_datetime})
    )

    print(f'X-Datetime: {x_datetime}')
    print(f'X-Signature: {x_signature}')
