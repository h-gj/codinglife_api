from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DDPageNumberPagination(PageNumberPagination):
    max_page_size = 30
    page_size_query_param = 'size'
    last_page_strings = ['last', 'lst']

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('pagination', OrderedDict([
                ('page', self.page.number),
                ('size', self.page.paginator.per_page),
                ('total', self.page.paginator.count),
                ('last', self.page.paginator.num_pages)
            ])),
            ('content', data)
        ]))
