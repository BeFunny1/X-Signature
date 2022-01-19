from django.http import JsonResponse


def error_response(code, message, status=400):
    return JsonResponse(
        {
            'errors': [
                {
                    'code': code,
                    'message': message,
                }
            ]
        },
        status=status,
    )
