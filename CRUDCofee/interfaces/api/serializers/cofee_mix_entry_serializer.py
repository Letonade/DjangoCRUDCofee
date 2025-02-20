from rest_framework import serializers
from CRUDCofee.models import CofeeMixModel, CofeeMixEntryModel, CofeeBeanModel
from .cofee_bean_serializer import CofeeBeanSerializer

class CofeeMixEntrySerializer(serializers.ModelSerializer):
    bean = CofeeBeanSerializer(read_only=True)
    bean_id = serializers.PrimaryKeyRelatedField(queryset=CofeeBeanModel.objects.all(), source="bean", write_only=True)

    class Meta:
        model = CofeeMixEntryModel
        fields = ['id', 'bean', 'bean_id', 'quantity']

class CofeeMixSerializer(serializers.ModelSerializer):
    beans = CofeeMixEntrySerializer(source='cofeemixentrymodel_set', many=True)

    class Meta:
        model = CofeeMixModel
        fields = ['id', 'name', 'description', 'beans']

    def create(self, validated_data):
        entries_data = validated_data.pop('cofeemixentrymodel_set', [])
        mix = CofeeMixModel.objects.create(**validated_data)
        for entry_data in entries_data:
            CofeeMixEntryModel.objects.create(mix=mix, **entry_data)
        return mix

    def update(self, instance, validated_data):
        entries_data = validated_data.pop('cofeemixentrymodel_set', None)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        if entries_data is not None:
            instance.cofeemixentrymodel_set.all().delete()
            for entry_data in entries_data:
                CofeeMixEntryModel.objects.create(mix=instance, **entry_data)
        return instance
