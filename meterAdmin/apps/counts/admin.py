import datetime
import xadmin
from xadmin.views import CommAdminView
from django.db.models.query import QuerySet
# Register your models here.
from xadmin import views
from counts import models
from bases.models import Buildings

from .views import minuteView
from .views import hourView
from .views import dayView
from .views import monthView

#xadmin.site.register_view(r'counts/minutechart/$', minuteView, name='minuteChart')
#xadmin.site.register_view(r'counts/hourchart/$', hourView, name='hourChart')
#xadmin.site.register_view(r'counts/daychart/$', dayView, name='dayChart')
#xadmin.site.register_view(r'counts/monthchart/$', monthView, name='monthChart')


class MinuteCountAdmin(object):
    # old config
    model_icon = 'fa  fa-clock-o'
    #list_export = ['xlsx', 'csv']
    list_display = ['id', 'dt', 'v1','v2','v3', 'l1','l2','l3', 'pf1','pf2','pf3','kva','kw','karl','opeationHR', 'createTime']
    #search_fields = ['v1', 'v2','v3']
    list_filter = ['building','dt']
    ordering = ['dt']
    hidden_menu=True
    
    #獲得當前用戶可管理數據
    def queryset(self):
        if not self.request.user.is_superuser:
            bid=self.request.user.building_id
            bd=Buildings.objects.get(id=bid)
            sr = self.model.objects.filter(building=bd)
            return sr 
        else:
            sf_building=""
            try:
                sf_building=self.request.GET['_p_building__id__exact']
                return self.model.objects.filter(building_id=sf_building)
            except:
                return models.MinuteCountTotal.objects.all()

xadmin.site.register(models.MinuteCount, MinuteCountAdmin)


class HourCountAdmin(object):
    model_icon = 'fa  fa-hourglass-o'
    #list_export = ['xlsx', 'csv']
    list_display = ['id', 'dt', 'v1','v2','v3', 'l1','l2','l3', 'pf1','pf2','pf3','kva','kw','karl','opeationHR', 'createTime']
    #search_fields = ['v1', 'v2','v3']
    list_filter = ['building','dt']
    ordering = ['dt']
    hidden_menu=True

    #獲得當前用戶可管理數據
    def queryset(self):
        if not self.request.user.is_superuser:
            bid=self.request.user.building_id
            bd=Buildings.objects.get(id=bid)
            sr = self.model.objects.filter(building=bd)
            return sr 
        else:
            sf_building=""
            try:
                sf_building=self.request.GET['_p_building__id__exact']
                return self.model.objects.filter(building_id=sf_building)
            except:
                return models.HourCountTotal.objects.all()

xadmin.site.register(models.HourCount, HourCountAdmin)


class HourChartAdmin_v(object):
    #use echart
    object_list_template = 'xadmin/countchart_v.html'
    #object_list_template = 'xadmin/500.html'
    # old config
    model_icon = 'fa  fa-clock-o'
    #search_fields = ['v1', 'v2','v3']
    list_filter = ['building','dt']
    ordering = ['dt']
    hidden_menu=True
    #獲得當前用戶可管理數據
    def get_context(self):
        context = super().get_context()
        qs=MonthChartAdmin.GetDb(self,"m_hour_count")
        return MonthChartAdmin.getListV(context,qs,"小時統計圖:電壓","%Y-%m-%d %H",0)
xadmin.site.register(models.HourChart_v, HourChartAdmin_v)

class HourChartAdmin_l(object):
    #use echart
    object_list_template = 'xadmin/countchart_l.html'
    #object_list_template = 'xadmin/500.html'
    # old config
    model_icon = 'fa  fa-clock-o'
    #search_fields = ['v1', 'v2','v3']
    list_filter = ['building','dt']
    ordering = ['dt']
    hidden_menu=True
    #獲得當前用戶可管理數據
    def get_context(self):
        context = super().get_context()
        qs=MonthChartAdmin.GetDb(self,"m_hour_count")
        return MonthChartAdmin.getListL(context,qs,"小時統計圖:電流","%Y-%m-%d %H",0)
xadmin.site.register(models.HourChart_l, HourChartAdmin_l)

class HourChartAdmin_o(object):
    #use echart
    object_list_template = 'xadmin/countchart_o.html'
    #object_list_template = 'xadmin/500.html'
    # old config
    model_icon = 'fa  fa-clock-o'
    #search_fields = ['v1', 'v2','v3']
    list_filter = ['building','dt']
    ordering = ['dt']
    hidden_menu=True
    #獲得當前用戶可管理數據
    def get_context(self):
        context = super().get_context()
        qs=MonthChartAdmin.GetDb(self,"m_hour_count")
        return MonthChartAdmin.getListO(context,qs,"小時統計圖:其他","%Y-%m-%d %H",0)
xadmin.site.register(models.HourChart_o, HourChartAdmin_o)

class DayCountAdmin(object):
    model_icon = 'fa  fa-sun-o'
    #list_export = ['xlsx', 'csv']
    list_display = ['id', 'dt', 'v1','v2','v3', 'l1','l2','l3', 'pf1','pf2','pf3','kva','kw','karl','opeationHR', 'createTime']
    #search_fields = ['v1', 'v2','v3']
    list_filter = ['building','dt']
    ordering = ['dt']
    hidden_menu=True

    #獲得當前用戶可管理數據
    def queryset(self):
        if not self.request.user.is_superuser:
            bid=self.request.user.building_id
            bd=Buildings.objects.get(id=bid)
            sr = self.model.objects.filter(building=bd)
            return sr
        else:
            sf_building=""
            try:
                sf_building=self.request.GET['_p_building__id__exact']
                return self.model.objects.filter(building_id=sf_building)
            except:
                return models.DayCountTotal.objects.all()
        #query = self.model.objects.all().query
        #return QuerySet(query = query, model = models.DayCount)

xadmin.site.register(models.DayCount, DayCountAdmin)


class DayChartAdmin_v(object):
    #use echart
    object_list_template = 'xadmin/countchart_v.html'
    #object_list_template = 'xadmin/500.html'
    # old config
    model_icon = 'fa  fa-clock-o'
    #search_fields = ['v1', 'v2','v3']
    list_filter = ['building','dt']
    ordering = ['dt']
    hidden_menu=True
    
    #獲得當前用戶可管理數據
    def get_context(self):
        context = super().get_context()
        qs=MonthChartAdmin.GetDb(self,"m_day_count")
        return MonthChartAdmin.getListV(context,qs,"每日統計圖:電壓","%Y-%m-%d",0)

xadmin.site.register(models.DayChart_v, DayChartAdmin_v)


class DayChartAdmin_l(object):
    #use echart
    object_list_template = 'xadmin/countchart_l.html'
    #object_list_template = 'xadmin/500.html'
    # old config
    model_icon = 'fa  fa-clock-o'
    #search_fields = ['v1', 'v2','v3']
    list_filter = ['building','dt']
    ordering = ['dt']
    hidden_menu=True
    #獲得當前用戶可管理數據
    def get_context(self):
        context = super().get_context()
        qs=MonthChartAdmin.GetDb(self,"m_day_count")
        return MonthChartAdmin.getListL(context,qs,"每日統計圖:電流","%Y-%m-%d",0)

xadmin.site.register(models.DayChart_l, DayChartAdmin_l)


class DayChartAdmin_o(object):
    #use echart
    object_list_template = 'xadmin/countchart_o.html'
    #object_list_template = 'xadmin/500.html'
    # old config
    model_icon = 'fa  fa-clock-o'
    #search_fields = ['v1', 'v2','v3']
    list_filter = ['building','dt']
    ordering = ['dt']
    hidden_menu=True
    #獲得當前用戶可管理數據
    def get_context(self):
        context = super().get_context()
        qs=MonthChartAdmin.GetDb(self,"m_day_count")
        return MonthChartAdmin.getListO(context,qs,"每日統計圖：其他","%Y-%m-%d",0)

xadmin.site.register(models.DayChart_o, DayChartAdmin_o)


class MonthCountAdmin(object):
    model_icon = 'fa  fa-moon-o'
    #list_export = ['xlsx', 'csv']
    list_display = ['id', 'dt', 'v1','v2','v3', 'l1','l2','l3', 'pf1','pf2','pf3', 'kva','kw','karl','opeationHR', 'createTime']
    #search_fields = ['v1', 'v2','v3']
    list_filter = ['building','dt']
    ordering = ['dt']
    hidden_menu=True

    #獲得當前用戶可管理數據
    def queryset(self):
        if not self.request.user.is_superuser:
            bid=self.request.user.building_id
            bd=Buildings.objects.get(id=bid)
            sr = self.model.objects.filter(building=bd)
            return sr 
        else:
            sf_building=""
            try:
                sf_building=self.request.GET['_p_building__id__exact']
                return self.model.objects.filter(building_id=sf_building)
            except:
                return models.MonthCountTotal.objects.all()

xadmin.site.register(models.MonthCount, MonthCountAdmin)


class MonthChartAdmin(object):
    #use echart
    object_list_template = 'xadmin/countchart_v.html'
    #object_list_template = 'xadmin/500.html'
    # old config
    model_icon = 'fa  fa-clock-o'
    #search_fields = ['v1', 'v2','v3']
    list_filter = ['building','dt']
    ordering = ['dt']
    hidden_menu=True
    #獲得當前用戶可管理數據
    def get_context(self):
        context = super().get_context()
        qs=MonthChartAdmin.GetDb(self,"m_month_count")
        return MonthChartAdmin.getListV(context,qs,"每月統計圖:電壓","%Y-%m",0)
    
    #public func
    def GetDb(self,table):
        hasDate=0
        hasBuild=0
        qs=self.model.objects.all()
        #filter
        sf_dts,sf_dte="",""
        try:
            sf_dts=self.request.GET['_p_dt__gte']
            sf_dte=self.request.GET['_p_dt__lt']
            sf_dts_=datetime.datetime.strptime(sf_dts,"%Y-%m-%d")
            sf_dte_=datetime.datetime.strptime(sf_dte,"%Y-%m-%d")
            qs=qs.filter(dt__gte=sf_dts_,dt__lt=sf_dte_)
            hasDate=1
        except Exception as e:
            print(e)
        sf_building=""
        try:
            sf_building=self.request.GET['_p_building__id__exact']
            qs=qs.filter(building_id=sf_building)
            hasBuild=1
        except:
            pass
        if not self.request.user.is_superuser:
            bid=self.request.user.building_id
            bd=Buildings.objects.get(id=bid)
            qs = qs.filter(building=bd)#.order_by('-dt')[:15]
        else:
            sqlb=""
            sqld=""
            if hasBuild==1:
                sqlb=" and building_id=%d"%int(sf_building)
            if hasDate==1:
                sqld=" and dt<'"+sf_dte+"' and dt>='"+sf_dts+"'"
            sql="select id,dt,avg(v1) v1,avg(v2) v2,avg(v3) v3,avg(l1) l1,avg(l2) l2,avg(l3) l3,avg(pf1) pf1,avg(pf2) pf2,avg(pf3) pf3,avg(kwh) kwh,avg(kva) kva,avg(kw) kw,avg(karl) karl,avg(opeationHR) opeationHR from %s where 1=1 %s %s GROUP BY dt" %(table,sqlb,sqld)
            qs=self.model.objects.raw(sql)
        
        
        return qs
    
    def getListV(context,qs,title,format,minv):
        #init params
        title_list=['v1', 'v2', 'v3']
        date_list=[]
        v1_list=[]
        v2_list=[]
        v3_list=[]

        #add values
        for q in qs:
            v1_list.append(int(q.v1))
            v2_list.append(int(q.v2))
            v3_list.append(int(q.v3))
            date_list.append(q.dt.strftime(format))

        context.update(
            {
                'title_list': title_list,
                'date_list': date_list,
                'v1_list': v1_list,
                'v2_list': v2_list,
                'v3_list': v3_list,
                'title': title,
                'minv' : minv,
            }
        )
        return context
    
    def getListL(context,qs,title,format,minv):
        #init params
        title_list=['l1', 'l2', 'l3']
        date_list=[]
        l1_list=[]
        l2_list=[]
        l3_list=[]

        #add values
        for q in qs:
            l1_list.append(int(q.l1))
            l2_list.append(int(q.l2))
            l3_list.append(int(q.l3))
            date_list.append(q.dt.strftime(format))

        context.update(
            {
                'title_list': title_list,
                'date_list': date_list,
                'l1_list': l1_list,
                'l2_list': l2_list,
                'l3_list': l3_list,
                'title': title,
                'minv' : minv,
            }
        )
        return context
    
    def getListO(context,qs,title,format,minv):
        title_list=['kva', 'kw', 'karl','opeationHR']
        date_list=[]
        kva_list=[]
        kw_list=[]
        karl_list=[]
        ohr_list=[]

        #add values
        for q in qs:
            kva_list.append(int(q.kva))
            kw_list.append(int(q.kw))
            karl_list.append(int(q.karl))
            ohr_list.append(int(q.opeationHR))
            date_list.append(q.dt.strftime(format))

        context.update(
            {
                'title_list': title_list,
                'date_list': date_list,
                'kw_list': kw_list,
                'kva_list': kva_list,
                'karl_list': karl_list,
                'ohr_list': ohr_list,
                'title': title,
                'minv' : minv,
            }
        )
        return context

xadmin.site.register(models.MonthChart_v, MonthChartAdmin)

class MonthChartAdmin_l(object):
    #use echart
    object_list_template = 'xadmin/countchart_l.html'
    #object_list_template = 'xadmin/500.html'
    # old config
    model_icon = 'fa  fa-clock-o'
    #search_fields = ['v1', 'v2','v3']
    list_filter = ['building','dt']
    ordering = ['dt']
    hidden_menu=True
    #獲得當前用戶可管理數據
    def get_context(self):
        context = super().get_context()
        qs=MonthChartAdmin.GetDb(self,"m_month_count")
        return MonthChartAdmin.getListL(context,qs,"每月統計圖:電流","%Y-%m",0)
xadmin.site.register(models.MonthChart_l, MonthChartAdmin_l)

class MonthChartAdmin_o(object):
    #use echart
    object_list_template = 'xadmin/countchart_o.html'
    #object_list_template = 'xadmin/500.html'
    # old config
    model_icon = 'fa  fa-clock-o'
    #search_fields = ['v1', 'v2','v3']
    list_filter = ['building','dt']
    ordering = ['dt']
    hidden_menu=True
    #獲得當前用戶可管理數據
    def get_context(self):
        context = super().get_context()
        qs=MonthChartAdmin.GetDb(self,"m_month_count")
        return MonthChartAdmin.getListO(context,qs,"每月統計圖:其他","%Y-%m",0)
xadmin.site.register(models.MonthChart_o, MonthChartAdmin_o)