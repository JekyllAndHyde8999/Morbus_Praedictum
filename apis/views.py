
from Doctor.models import *
from Patient.models import *
from Patient.utils import *
from .serializer import *

from rest_framework import filters, generics, status, views
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])


class scheduleApiView(generics.ListCreateAPIView):
    search_fields = ['Doctor_ID']
    filter_backends = (DynamicSearchFilter,)
    queryset = doctorSchedule.objects.filter()
    serializer_class = scheduleSerializer


class timeSlotsApiView(views.APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if str(user) != "AnonymousUser":
            docID = Doctor.objects.get(user=user)
            try:
                ts = TimeSlots.objects.get(Doctor_ID=docID)
            except:
                return Response('{Response:"No data"}')
            ts_list = list(ts)
            serializer = TimeSlotsSerializer
            return Response(serializer.data)
        return Response('{Response:"Please login first"}')
        #
        # search_fields = ['Doctor_ID']
        # filter_backends = (DynamicSearchFilter,)
        # queryset = TimeSlots.objects.filter()
        # serializer_class = TimeSlotsSerializer


class DoctorApi(generics.ListCreateAPIView):
    search_fields = ['Doctor_Gender', 'Doctor_Qualifications', 'Doctor_Specialization']
    filter_backends = (DynamicSearchFilter,)
    queryset = Doctor.objects.filter()
    serializer_class = DoctorSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


# #PATIENT APIS
class DonorList(generics.ListCreateAPIView):
    search_fields = ['Patient_Blood_Group']
    filter_backends = (DynamicSearchFilter,)
    queryset = Profile.objects.filter(Patient_Blood_Donation=0)
    serializer_class = BdSerializer



class DiseasePredictor(views.APIView):
    def post(self, request):
        raw_data = request.data
        data = raw_data['data'].split(",")
        data = [x.strip() for x in data]
        result_dict = predict(data)
        print(result_dict)
        results = [[x[0], str(round(x[1] * 100, 2)) + '%'] for x in
                   sorted(list(result_dict.items()), key=lambda x: -x[1])]
        return Response(result_dict, status=status.HTTP_200_OK)
