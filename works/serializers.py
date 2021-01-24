from datetime import datetime

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from works.models import Work


class WorkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Work
        fields = ('id', 'title', 'description', 'status', 'created_at')
        read_only_fields = ('id', 'status')

    def create(self, validated_data):
        created_at = validated_data.get('created_at')
        if created_at < datetime.today().date():
            raise serializers.ValidationError(_('Invalid date'))

        if created_at == datetime.today().date():
            validated_data['status'] = Work.STATUS_IN_PROGRESS
        else:
            validated_data['status'] = Work.STATUS_NOT_STARTED

        return super().create(validated_data)
