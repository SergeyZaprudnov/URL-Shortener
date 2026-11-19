from django.core.cache import cache
from django.http import Http404
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ShortLink
from .services import create_short_link


class ShortLinkCreateView(APIView):
    def post(self, request):
        original_url = request.data.get('original_url')
        if not original_url:
            return Response(
                {"error": "original_url is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        link = create_short_link(original_url)
        
        short_url = request.build_absolute_uri(f'/{link.short_code}')
        
        return Response({
            "original_url": link.original_url,
            "short_url": short_url,
            "clicks": link.clicks
        }, status=status.HTTP_201_CREATED)


class ShortLinkRedirectView(APIView):
    def get(self, request, code):
        # 1. Пытаемся взять URL из кеша
        cache_key = f"short_link_{code}"
        original_url = cache.get(cache_key)

        if not original_url:
            # 2. Если в кеше нет — идем в базу
            try:
                link = ShortLink.objects.get(short_code=code)
            except ShortLink.DoesNotExist:
                raise Http404("Link not found")
            
            original_url = link.original_url
            
            # 3. Сохраняем в кеш на 1 час (3600 секунд)
            cache.set(cache_key, original_url, timeout=3600)
        else:
            # Если взяли из кеша, все равно нужно получить объект для обновления счетчика
            link = ShortLink.objects.get(short_code=code)

        # 4. Атомарно увеличиваем счетчик кликов
        ShortLink.objects.filter(pk=link.pk).update(clicks=link.clicks + 1)
        
        return redirect(original_url, permanent=False)