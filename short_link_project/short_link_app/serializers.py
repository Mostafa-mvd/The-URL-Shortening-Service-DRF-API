from rest_framework import serializers
from . import models as shorten_link_model
from . import utils as shortening_link_utils


class ShorteningLinkSerializer(serializers.ModelSerializer):
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        formated_created_time = instance.get_formated_created_time_str()
        formated_expiration_time = instance.get_formated_expiration_time_str()
        short_url = shortening_link_utils.concatenate_base_url_with_end_point_path(
            self.context['request'], instance.token)

        data['expiration_time'] = formated_expiration_time
        data['created_time'] = formated_created_time
        data['short_url'] = short_url

        return data

    class Meta:
        model = shorten_link_model.ShortLink
        fields = [
            'original_url',
            'token',
            'expiration_time',
            'is_private',
        ]
