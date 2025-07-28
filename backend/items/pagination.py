from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_page_size(self, request):
        screen_width = request.query_params.get("screen_width")
        if screen_width:
            screen_width = int(screen_width)
            if screen_width < 600:
                return 10
            elif screen_width < 1200:
                return 20
            else:
                return 30
        return super().get_page_size(request)

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "page_size": self.get_page_size(self.request),
                "results": data,
            }
        )
