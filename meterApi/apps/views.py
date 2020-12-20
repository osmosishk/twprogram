from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from apps.models import MeterData, Params,Meters,FileModel
from .serializers import MeterDataSerializer, ParamSerializer,MeterSerializer,FileSerializer
from rest_framework.response import Response
from django.db.models import Q
import datetime
# Create your views here.
class MeterDataViewSet(ModelViewSet):
    queryset = MeterData.objects.all()
    #add new
    def create(self, request):
        serializer_class = MeterDataSerializer(data=request.data)
        '''today = datetime.datetime.now().strftime("%Y%m%d")
        try:
            mds = apps.get_model('__main__', 'meter_data_%s' % today)
        except LookupError:
            mds = get_meterdata_model(today)

        if not mds.is_exists():
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(mds)
        '''
        tm=request.data['time']
        mid=request.data['meter_id']
        uptime=datetime.datetime.strptime(tm,'%Y-%m-%d %H:%M:%S')
        query=MeterData.objects.filter(Q(meter_id=mid) & Q(time=tm))#.order_by('-time').first()
        if query.count() == 0:
            serializer_class.is_valid(raise_exception=True)
            result=serializer_class.save()
            return Response({'code':'1'})
        else:
            print("not insert")
            return Response({'code':'-1'})

class ParamViewSet(ModelViewSet):
    queryset = Params.objects.all()
    serializer_class = ParamSerializer

class MeterViewSet(ModelViewSet):
    queryset = Meters.objects.all()
    serializer_class = MeterSerializer

    def list(self, request):
        meter=request.data['meter']
        rasp=request.data['rasp']
        query=Meters.objects.filter(name=meter).first()
        if query!=None:
            return Response({'bid':query.building_id,'rid':query.rasp_id,'mid':query.id})
        else:
            return Response({'bid':0,'rid':0,'mid':0})

#upload file
class FileViewSet(viewsets.ModelViewSet):
    queryset = FileModel.objects.all()
    def list(self, request):
        mid=request.data['mid']
        query=FileModel.objects.filter(meter_id=mid).order_by('-record_date').first()
        if query!=None:
            return Response({'tm':query.record_date})
        else:
            return Response({'tm':''})
    def create(self,request):
        serializer_class = FileSerializer(data=request.data)
        name=request.data['name']
        query=FileModel.objects.filter(Q(name=name))#.order_by('-time').first()
        if query.count() > 0:
            return Response(1)
        serializer_class.is_valid(raise_exception=True)
        try:
            serializer_class.save()
            return Response(1)
        except:
            return Response(0)

class FileUploadView(APIView):
    parser_classes = [FileUploadParser, ]

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        with open(filename, 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        return Response(f'{filename} uploaded',status=204)