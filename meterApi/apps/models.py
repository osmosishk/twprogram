from django.db import models

class Buildings(models.Model):
    name = models.CharField(max_length=50, verbose_name='大廈名稱')
    status = models.CharField(max_length=10, default='using', choices=(("using", "using"), ("stoping", "stoping")), verbose_name='狀態')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')

    class Meta:
        db_table = 'm_buildings'
        verbose_name = "大廈"
        verbose_name_plural = verbose_name
        ordering = ['-createTime']
        unique_together=(("name"),)

    def __str__(self):

        return self.name


class Rasps(models.Model):
    name = models.CharField(max_length=50, verbose_name='名稱')
    no = models.CharField(max_length=50, verbose_name='編號')
    location = models.CharField(max_length=20, verbose_name='樓棟-層數-房號')
    status = models.CharField(max_length=10, default='1', choices=(("1", "online"), ("0", "offline")), verbose_name='狀態')
    isTest = models.CharField(max_length=10, default='1', choices=(("1", "yes"), ("0", "no")), verbose_name='是否測試設備')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    remark = models.CharField(max_length=100, verbose_name='備註',blank=True,null=True)
    building = models.ForeignKey(Buildings,verbose_name='大廈名稱', on_delete=models.CASCADE,default='') 

    class Meta:
        db_table = 'm_rasps'
        verbose_name = "樹莓派"
        verbose_name_plural = verbose_name
        ordering = ['no']
        unique_together=(("name"),)

    def __str__(self):

        return self.name


class Meters(models.Model):
    name = models.CharField(max_length=50, verbose_name='電錶名稱')
    no = models.CharField(max_length=50, verbose_name='電錶編號')
    currentNumber = models.CharField(max_length=10, verbose_name='當前電錶讀數')
    location = models.CharField(max_length=20, verbose_name='樓棟-層數-房號')
    status = models.CharField(max_length=10, default='1', choices=(("1", "online"), ("0", "offline")), verbose_name='狀態')
    isTest = models.CharField(max_length=10, default='1', choices=(("1", "yes"), ("0", "no")), verbose_name='是否測試電錶')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    lastUpTime = models.DateTimeField(auto_now_add=True, verbose_name='最後上傳數據時間')
    lastMinuteTime = models.DateTimeField(auto_now_add=True, verbose_name='最後分鐘統計時間')
    lastHourTime = models.DateTimeField(auto_now_add=True, verbose_name='最後小時統計時間')
    lastDayTime = models.DateTimeField(auto_now_add=True, verbose_name='最後日統計時間')
    lastMonthTime = models.DateTimeField(auto_now_add=True, verbose_name='最後月統計時間')
    remark = models.CharField(max_length=100, verbose_name='備註',blank=True,null=True)
    building = models.ForeignKey(Buildings,verbose_name='大廈名稱', on_delete=models.CASCADE,default='') 
    rasp = models.ForeignKey(Rasps,verbose_name='樹莓派名稱', on_delete=models.CASCADE,default='')

    class Meta:
        db_table = 'm_meters'
        verbose_name = "電錶"
        verbose_name_plural = verbose_name
        ordering = ['no']
        unique_together=(("name"),)

    def __str__(self):

        return self.name

class MeterData(models.Model):
    id= models.AutoField(primary_key=True)
    v1 = models.IntegerField(verbose_name='V1')
    v2 = models.IntegerField(verbose_name='V2')
    v3 = models.IntegerField(verbose_name='V3')
    l1 = models.IntegerField(verbose_name='L1')
    l2 = models.IntegerField(verbose_name='L2')
    l3 = models.IntegerField(verbose_name='L3')
    pf1 = models.IntegerField(verbose_name='PF1')
    pf2 = models.IntegerField(verbose_name='PF2')
    pf3 = models.IntegerField(verbose_name='PF3')
    kwh = models.IntegerField(verbose_name='KWH')
    time = models.DateTimeField(verbose_name='time',default='2019-1-1 00:00:00')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')

    building = models.ForeignKey(Buildings, verbose_name='大廈名稱', on_delete=models.CASCADE, default='') 
    rasp = models.ForeignKey(Rasps, verbose_name='樹莓派名稱', on_delete=models.CASCADE, default='')
    meter = models.ForeignKey(Meters, verbose_name='電錶名稱', on_delete=models.CASCADE, default='')

    class Meta:
        db_table = 'meter_datas'
        verbose_name = "電錶數據"
        verbose_name_plural = verbose_name
        ordering = ['-createTime']

class Params(models.Model):
    id= models.AutoField(primary_key=True)
    paramName = models.CharField(max_length=50, verbose_name='參數名')
    paramValue = models.CharField(max_length=50, verbose_name='參數值')
    remark = models.CharField(max_length=50, verbose_name='用途')
    status = models.IntegerField(verbose_name='狀態')
    sort = models.IntegerField(verbose_name='順序')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')

    class Meta:
        db_table = 'm_params'
        verbose_name = "參數"
        verbose_name_plural = verbose_name

'''
def get_meterdata_model(prefix):
    table_name = 'meter_data_%s' % str(prefix)

    class MeterDataMetaclass(models.base.ModelBase):
        def __new__(cls, name, bases, attrs):
            name += '_' + prefix
            return models.base.ModelBase.__new__(cls, name, bases, attrs)
    class MeterData(models.Model):
        __metaclass__ = MeterDataMetaclass
        id= models.AutoField(primary_key=True)
        v1 = models.IntegerField(verbose_name='V1')
        v2 = models.IntegerField(verbose_name='V2')
        v3 = models.IntegerField(verbose_name='V3')
        l1 = models.IntegerField(verbose_name='L1')
        l2 = models.IntegerField(verbose_name='L2')
        l3 = models.IntegerField(verbose_name='L3')
        pf1 = models.IntegerField(verbose_name='PF1')
        pf2 = models.IntegerField(verbose_name='PF2')
        pf3 = models.IntegerField(verbose_name='PF3')
        kwh = models.IntegerField(verbose_name='KWH')
        time = models.DateTimeField(verbose_name='time')
        createTime = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')

        building = models.ForeignKey(Buildings, verbose_name='大廈名稱', on_delete=models.CASCADE, default='') 
        rasp = models.ForeignKey(Rasps, verbose_name='樹莓派名稱', on_delete=models.CASCADE, default='')
        meter = models.ForeignKey(Meters, verbose_name='電錶名稱', on_delete=models.CASCADE, default='')

        @staticmethod
        def is_exists():
            return table_name in connection.introspection.table_names()
'''
#文件上傳
class FileModel(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,verbose_name='文件名稱')
    file = models.FileField(upload_to='upload')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    building_id=models.IntegerField(verbose_name='大廈id')
    rasp_id=models.IntegerField(verbose_name='樹莓派id')
    meter_id=models.IntegerField(verbose_name='電錶id')
    record_date=models.CharField(max_length=20,verbose_name='文件記錄時間')
    status=models.SmallIntegerField(verbose_name='狀態:2-已處理',default=0)


    class Meta:
        db_table = 'm_upfiles'
        verbose_name = "上傳文件記錄"
        verbose_name_plural = verbose_name
