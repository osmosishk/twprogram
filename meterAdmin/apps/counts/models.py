from django.db import models

from bases.models import Buildings,Rasps,Meters

class MinuteCount(models.Model):
    dt=models.DateTimeField(max_length=20,verbose_name='時間')
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
    kva = models.IntegerField(verbose_name='KVA',default=0)
    kw = models.IntegerField(verbose_name='KW',default=0)
    karl = models.IntegerField(verbose_name='KARL',default=0)
    opeationHR = models.IntegerField(verbose_name='OpeationHR',default=0)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')

    building = models.ForeignKey(Buildings, verbose_name='大廈名稱', on_delete=models.CASCADE, default='') 
    #rasp = models.ForeignKey(Rasps, verbose_name='樹莓派名稱', on_delete=models.CASCADE, default='')
    #meter = models.ForeignKey(Meters, verbose_name='電錶名稱', on_delete=models.CASCADE, default='')

    class Meta:
        db_table = 'm_minute_count'
        verbose_name = "分鐘統計表"
        verbose_name_plural = verbose_name
        ordering = ['-dt']
        unique_together=(("dt"),("building"))

class MinuteCountTotal(models.Model):
    dt=models.DateTimeField(max_length=20,verbose_name='時間')
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
    kva = models.IntegerField(verbose_name='KVA',default=0)
    kw = models.IntegerField(verbose_name='KW',default=0)
    karl = models.IntegerField(verbose_name='KARL',default=0)
    opeationHR = models.IntegerField(verbose_name='OpeationHR',default=0)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')

    class Meta:
        db_table = 'm_minute_count_total'
        unique_together=(("dt"),)


class HourCount(models.Model):
    dt=models.DateTimeField(max_length=20,verbose_name='時間')
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
    kva = models.IntegerField(verbose_name='KVA',default=0)
    kw = models.IntegerField(verbose_name='KW',default=0)
    karl = models.IntegerField(verbose_name='KARL',default=0)
    opeationHR = models.IntegerField(verbose_name='OpeationHR',default=0)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')

    building = models.ForeignKey(Buildings, verbose_name='大廈名稱', on_delete=models.CASCADE, default='') 
    #rasp = models.ForeignKey(Rasps, verbose_name='樹莓派名稱', on_delete=models.CASCADE, default='')
    #meter = models.ForeignKey(Meters, verbose_name='電錶名稱', on_delete=models.CASCADE, default='')

    class Meta:
        db_table = 'm_hour_count'
        verbose_name = "小時統計表"
        verbose_name_plural = verbose_name
        ordering = ['-dt']
        unique_together=(("dt"),("building"))

class HourCountTotal(models.Model):
    dt=models.DateTimeField(max_length=20,verbose_name='時間')
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
    kva = models.IntegerField(verbose_name='KVA',default=0)
    kw = models.IntegerField(verbose_name='KW',default=0)
    karl = models.IntegerField(verbose_name='KARL',default=0)
    opeationHR = models.IntegerField(verbose_name='OpeationHR',default=0)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')

    class Meta:
        db_table = 'm_hour_count_total'
        verbose_name = "小時統計表"
        verbose_name_plural = verbose_name
        ordering = ['-dt']
        unique_together=(("dt"),)

class HourChart_v(models.Model):
    dt=models.DateTimeField(max_length=20,verbose_name='時間')
    v1 = models.IntegerField(verbose_name='V1')
    v2 = models.IntegerField(verbose_name='V2')
    v3 = models.IntegerField(verbose_name='V3')

    building = models.ForeignKey(Buildings, verbose_name='大廈名稱', on_delete=models.CASCADE, default='')

    class Meta:
        db_table = 'm_hour_count'
        verbose_name = "小時統計圖"
        verbose_name_plural = verbose_name

class HourChart_l(models.Model):
    dt=models.DateTimeField(max_length=20,verbose_name='時間')
    l1 = models.IntegerField(verbose_name='L1')
    l2 = models.IntegerField(verbose_name='L2')
    l3 = models.IntegerField(verbose_name='L3')

    building = models.ForeignKey(Buildings, verbose_name='大廈名稱', on_delete=models.CASCADE, default='') 

    class Meta:
        db_table = 'm_hour_count'
        verbose_name = "小時統計圖"
        verbose_name_plural = verbose_name

class HourChart_o(models.Model):
    dt=models.DateTimeField(max_length=20,verbose_name='時間')
    kwh = models.IntegerField(verbose_name='KWH')
    kva = models.IntegerField(verbose_name='KVA')
    kw = models.IntegerField(verbose_name='KW')
    karl = models.IntegerField(verbose_name='KARL')
    opeationHR = models.IntegerField(verbose_name='OpeationHR')

    building = models.ForeignKey(Buildings, verbose_name='大廈名稱', on_delete=models.CASCADE, default='') 

    class Meta:
        db_table = 'm_hour_count'
        verbose_name = "小時統計圖"
        verbose_name_plural = verbose_name

class DayCount(models.Model):
    dt=models.DateTimeField(max_length=20,verbose_name='時間')
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
    kva = models.IntegerField(verbose_name='KVA',default=0)
    kw = models.IntegerField(verbose_name='KW',default=0)
    karl = models.IntegerField(verbose_name='KARL',default=0)
    opeationHR = models.IntegerField(verbose_name='OpeationHR',default=0)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')

    building = models.ForeignKey(Buildings, verbose_name='大廈名稱', on_delete=models.CASCADE, default='') 
    #rasp = models.ForeignKey(Rasps, verbose_name='樹莓派名稱', on_delete=models.CASCADE, default='')
    #meter = models.ForeignKey(Meters, verbose_name='電錶名稱', on_delete=models.CASCADE, default='')

    class Meta:
        db_table = 'm_day_count'
        verbose_name = "每日統計表"
        verbose_name_plural = verbose_name
        ordering = ['-dt']
        unique_together=(("dt"),("building"))

class DayCountTotal(models.Model):
    dt=models.DateTimeField(max_length=20,verbose_name='時間')
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
    kva = models.IntegerField(verbose_name='KVA',default=0)
    kw = models.IntegerField(verbose_name='KW',default=0)
    karl = models.IntegerField(verbose_name='KARL',default=0)
    opeationHR = models.IntegerField(verbose_name='OpeationHR',default=0)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')

    
    class Meta:
        db_table = 'm_day_count_total'
        verbose_name = "每日統計表"
        verbose_name_plural = verbose_name
        ordering = ['-dt']
        unique_together=(("dt"),)

class DayChart_v(models.Model):
    dt=models.DateTimeField(max_length=20,verbose_name='時間')
    v1 = models.IntegerField(verbose_name='V1')
    v2 = models.IntegerField(verbose_name='V2')
    v3 = models.IntegerField(verbose_name='V3')

    building = models.ForeignKey(Buildings, verbose_name='大廈名稱', on_delete=models.CASCADE, default='') 
    
    class Meta:
        db_table = 'm_day_count'
        verbose_name = "每日統計圖"
        verbose_name_plural = verbose_name        


class DayChart_l(models.Model):
    dt=models.DateTimeField(max_length=20,verbose_name='時間')
    l1 = models.IntegerField(verbose_name='L1')
    l2 = models.IntegerField(verbose_name='L2')
    l3 = models.IntegerField(verbose_name='L3')

    building = models.ForeignKey(Buildings, verbose_name='大廈名稱', on_delete=models.CASCADE, default='') 

    class Meta:
        db_table = 'm_day_count'
        verbose_name = "每日統計圖"
        verbose_name_plural = verbose_name 


class DayChart_o(models.Model):
    dt=models.DateTimeField(max_length=20,verbose_name='時間')
    kwh = models.IntegerField(verbose_name='KWH')
    kva = models.IntegerField(verbose_name='KVA')
    kw = models.IntegerField(verbose_name='KW')
    karl = models.IntegerField(verbose_name='KARL')
    opeationHR = models.IntegerField(verbose_name='OpeationHR')

    building = models.ForeignKey(Buildings, verbose_name='大廈名稱', on_delete=models.CASCADE, default='') 

    class Meta:
        db_table = 'm_day_count'
        verbose_name = "每日統計圖"
        verbose_name_plural = verbose_name 


class MonthCount(models.Model):
    dt=models.DateTimeField(max_length=20,verbose_name='時間')
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
    kva = models.IntegerField(verbose_name='KVA',default=0)
    kw = models.IntegerField(verbose_name='KW',default=0)
    karl = models.IntegerField(verbose_name='KARL',default=0)
    opeationHR = models.IntegerField(verbose_name='OpeationHR',default=0)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')

    building = models.ForeignKey(Buildings, verbose_name='大廈名稱', on_delete=models.CASCADE, default='') 
    #rasp = models.ForeignKey(Rasps, verbose_name='樹莓派名稱', on_delete=models.CASCADE, default='')
    #meter = models.ForeignKey(Meters, verbose_name='電錶名稱', on_delete=models.CASCADE, default='')

    class Meta:
        db_table = 'm_month_count'
        verbose_name = "每月統計表"
        verbose_name_plural = verbose_name
        ordering = ['-dt']
        unique_together=(("dt"),("building"))

class MonthCountTotal(models.Model):
    dt=models.DateTimeField(max_length=20,verbose_name='時間')
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
    kva = models.IntegerField(verbose_name='KVA',default=0)
    kw = models.IntegerField(verbose_name='KW',default=0)
    karl = models.IntegerField(verbose_name='KARL',default=0)
    opeationHR = models.IntegerField(verbose_name='OpeationHR',default=0)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')

    class Meta:
        db_table = 'm_month_count_total'
        verbose_name = "每月統計表"
        verbose_name_plural = verbose_name
        ordering = ['-dt']
        unique_together=(("dt"),)


class MonthChart_v(models.Model):
    dt=models.DateTimeField(max_length=20,verbose_name='時間')
    v1 = models.IntegerField(verbose_name='V1')
    v2 = models.IntegerField(verbose_name='V2')
    v3 = models.IntegerField(verbose_name='V3')

    building = models.ForeignKey(Buildings, verbose_name='大廈名稱', on_delete=models.CASCADE, default='') 

    class Meta:
        db_table = 'm_month_count'
        verbose_name = "每月統計圖"
        verbose_name_plural = verbose_name


class MonthChart_l(models.Model):
    dt=models.DateTimeField(max_length=20,verbose_name='時間')
    l1 = models.IntegerField(verbose_name='L1')
    l2 = models.IntegerField(verbose_name='L2')
    l3 = models.IntegerField(verbose_name='L3')

    building = models.ForeignKey(Buildings, verbose_name='大廈名稱', on_delete=models.CASCADE, default='') 

    class Meta:
        db_table = 'm_month_count'
        verbose_name = "每月統計圖"
        verbose_name_plural = verbose_name


class MonthChart_o(models.Model):
    dt=models.DateTimeField(max_length=20,verbose_name='時間')
    kwh = models.IntegerField(verbose_name='KWH')
    kva = models.IntegerField(verbose_name='KVA')
    kw = models.IntegerField(verbose_name='KW')
    karl = models.IntegerField(verbose_name='KARL')
    opeationHR = models.IntegerField(verbose_name='OpeationHR')

    building = models.ForeignKey(Buildings, verbose_name='大廈名稱', on_delete=models.CASCADE, default='') 

    class Meta:
        db_table = 'm_month_count'
        verbose_name = "每月統計圖"
        verbose_name_plural = verbose_name
