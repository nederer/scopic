from rest_framework import serializers

from django.utils import timezone

from home_page.models import Product
from api import models, tasks
from scopic_task.settings import HIGHEST_BID


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "current_bid",
            "title",
            "description",
        )


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BidsHistory
        fields = (
            "username",
            "date",
            "bid_amount",
        )

    date = serializers.SerializerMethodField()

    username = serializers.SerializerMethodField()

    @staticmethod
    def get_username(obj):
        return obj.user.username

    @staticmethod
    def get_date(obj):
        return obj.date.strftime('%m-%d-%Y %H:%M:%S')


class CreateBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BidsHistory
        fields = (
            "user",
            "product",
            "bid_amount",
            "auto_bid",
        )

    def validate(self, data):
        if data["bid_amount"] > HIGHEST_BID or data["bid_amount"] <= data["product"].current_bid:
            raise serializers.ValidationError(
                f"Bid amount must be less then {HIGHEST_BID} and more then {data['product'].current_bid}"
            )

        if timezone.now() >= data["product"].close_date:
            raise serializers.ValidationError(f"Bids ends")

        return data

    def create(self, validated_data):
        validated_data["product"].current_bid = validated_data["bid_amount"]
        validated_data["product"].save()

        if validated_data["bid_amount"] != HIGHEST_BID:
            tasks.check_auto_bids.delay(
                validated_data["product"].pk,
                validated_data["user"].pk
            )

        return models.BidsHistory.objects.create(**validated_data)


class UserAutoBidsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserAutoBidding
        fields = (
            "user",
            "max_bids",
        )
