from rest_framework import serializers
from .models import *
# from rest_framework import viewsets

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class BloodDonorSerializer(serializers.ModelSerializer):
    # City = serializers.SerializerMethodField(city)
    # address = AddressSerializer(many=True)
    Patient_ID__Patient_Blood_Group = serializers.IntegerField()
    Patient_ID__Patient_First_Name = serializers.CharField()
    Patient_ID__Patient_Last_Name = serializers.CharField()
    Patient_ID__Patient_Phone_Number = serializers.CharField()
    Patient_ID__Patient_Gender = serializers.IntegerField()
    Patient_ID__Patient_DOB = serializers.DateField()
    Patient_ID__Patient_Email = serializers.EmailField()
    city = serializers.CharField()

    class Meta:
        model = Address
        fields = ('Patient_ID__Patient_Blood_Group','Patient_ID__Patient_First_Name','Patient_ID__Patient_Last_Name','Patient_ID__Patient_Phone_Number','Patient_ID__Patient_Gender','Patient_ID__Patient_DOB','Patient_ID__Patient_Email','city')


#
# class BloodDonorViewSet(viewsets.ModelViewSet):
#
#     queryset = Profile.objects.all()
#     serializer_class = BloodDonorSerializer
#


# class PredictDisease(serializers.Serializer):
#     symptoms = serializers.ListSerializer(child=None)
#
#     def create(self, validated_data):
#         print(validated_data)



class BdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'