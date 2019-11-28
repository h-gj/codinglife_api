from rest_framework.response import Response


class DDListModelMixin:
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        queryset = self.list_serializer_class(self.queryset)

        serializer = self.list_serializer_class(queryset, many=True)
        return Response(serializer.data)