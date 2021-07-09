from rest_framework.response import Response

from home_page.models import Product
from api import models
from api import serializers

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated


class ProductsCurrentInfoView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        ids = self.request.query_params.get('ids', None)
        queryset = Product.objects.all()[:10]
        if ids is not None:
            ids = [int(x) for x in ids.split(',')]
            queryset = Product.objects.filter(pk__in=ids)
        return queryset


class ProductBidHistoryView(generics.ListAPIView):
    serializer_class = serializers.BidSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.BidsHistory.objects.filter(product_id=pk).order_by("-date")[:10]


class ProductBidView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.CreateBidSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserAutoBidView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.UserAutoBidsSerializer

    def get_object(self):
        return models.UserAutoBidding.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        data["user"] = request.user.pk
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
