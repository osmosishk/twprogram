from rest_framework import serializers
from apps.models import MeterData,Params,Meters,FileModel


class MeterDataSerializer(serializers.ModelSerializer):

    building_id = serializers.IntegerField()
    rasp_id = serializers.IntegerField()
    meter_id = serializers.IntegerField()

    class Meta:
        model = MeterData
        fields = ('v1', 'v2', 'v3', 'l1', 'l2', 'l3', 'pf1', 'pf2', 'pf3', 'kwh', 'building_id', 'rasp_id', 'meter_id', 'time')

    #def create(self, validated_data):
    #　　return MeterData.objects.create(building=self.context["building"], **validated_data)

class ParamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Params
        fields = ('paramName', 'paramValue')


class MeterSerializer(serializers.ModelSerializer):

    building_id = serializers.IntegerField()
    rasp_id = serializers.IntegerField()

    class Meta:
        model = Meters
        fields = ('id','name', 'no', 'status', 'building_id', 'rasp_id')


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = '__all__'