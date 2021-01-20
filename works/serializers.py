from rest_framework import serializers

from works.models import Work


class WorkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Work
        fields = ('id', 'title', 'description', 'created_at')
        read_only_fields = ('id', )
