from rest_framework import serializers
from . import models as shorten_link_model


class ShortenLinkSerializer(serializers.ModelSerializer):

    result_link = serializers.CharField(
        source="shorten_link",
        required=False
    )

    class Meta:
        model = shorten_link_model.ShortLinkCreator
        fields = [
            'original_url',
            'result_link',
            'expiration_time',
            'is_shorten_url_private',
        ]