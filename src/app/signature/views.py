from django.http import JsonResponse
from django.views import View


class Handler(View):
    def post(self, request):
        return JsonResponse(data={'message': 'success'})
