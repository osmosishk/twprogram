import xadmin

# Register your models here.
from xadmin import views
from bases import models
from bases.models import Params
from counts.models import MinuteCount,HourCount,DayCount,MonthCount,HourChart_v,HourChart_l,HourChart_o,DayChart_v,DayChart_l,DayChart_o,MonthChart_v,MonthChart_l,MonthChart_o


class GlobalSetting(object):
    # admin top word
    site_title = '管理系統'
    # admin foot word
    site_footer = 'Copyright Energy Vergence Limited.'
    # menu style
    menu_style = "accordion"
    # custom menus
    
    def get_site_menu(self):
        return [
            {
                'title': '數據統計',
                'icon': 'fa fa-flask',
                'menus': (
                    {
                        'title': '分鐘統計表',
                        'url': '/counts/minutecount',
                        'icon': 'fa fa-clock-o'
                    },
                    {
                        'title': '小時統計表',
                        'url': '/counts/hourcount',
                        'icon': 'fa fa-hourglass-o'
                    },
                    {
                        'title': '小時統計圖:電壓',
                        'url': '/counts/hourchart_v',
                        'icon': 'fa fa-hourglass-o',
                        'perm': self.get_model_perm(HourChart_v, 'view')
                    },
                    {
                        'title': '小時統計圖:電流',
                        'url': '/counts/hourchart_l',
                        'icon': 'fa fa-hourglass-o',
                        'perm': self.get_model_perm(HourChart_l, 'view')
                    },
                    {
                        'title': '小時統計圖:其他',
                        'url': '/counts/hourchart_o',
                        'icon': 'fa fa-hourglass-o',
                        'perm': self.get_model_perm(HourChart_o, 'view')
                    },
                    {
                        'title': '每日統計表',
                        'url': '/counts/daycount',
                        'icon': 'fa fa-sun-o'
                    },
                    {
                        'title': '每日統計圖:電壓',
                        'url': '/counts/daychart_v',
                        'icon': 'fa fa-sun-o',
                        'perm': self.get_model_perm(DayChart_v, 'view')
                    },
                    {
                        'title': '每日統計圖:電流',
                        'url': '/counts/daychart_l',
                        'icon': 'fa fa-sun-o',
                        'perm': self.get_model_perm(DayChart_l, 'view')
                    },
                    {
                        'title': '每日統計圖:其他',
                        'url': '/counts/daychart_o',
                        'icon': 'fa fa-sun-o',
                        'perm': self.get_model_perm(DayChart_o, 'view')
                    },
                    {
                        'title': '每月統計表',
                        'url': '/counts/monthcount',
                        'icon': 'fa fa-moon-o'
                    },
                    {
                        'title': '每月統計圖:電壓',
                        'url': '/counts/monthchart_v',
                        'icon': 'fa fa-moon-o',
                        'perm': self.get_model_perm(MonthChart_v, 'view')
                    },
                    {
                        'title': '每月統計圖:電流',
                        'url': '/counts/monthchart_l',
                        'icon': 'fa fa-moon-o',
                        'perm': self.get_model_perm(MonthChart_l, 'view')
                    },
                    {
                        'title': '每月統計圖:其他',
                        'url': '/counts/monthchart_o',
                        'icon': 'fa fa-moon-o',
                        'perm': self.get_model_perm(MonthChart_o, 'view')
                    }
                )
            },
            {
                'title': '用戶管理',
                'icon': 'fa fa-user',
                'menus':(
                    {
                        'title': '用戶',
                        'icon': 'fa fa-user',
                        'url': "/users/user",
                        'perm': self.get_model_perm(Params, 'view')

                    },)
            },
            {
                'title': '參數設定',
                'icon': 'fa fa-cogs',
                'menus':(
                    {
                        'title': '參數設定',
                        'icon': 'fa fa-cog',
                        'url': "/bases/params",
                        'perm': self.get_model_perm(Params, 'view')

                    },)
            }
        ]

##Registe up menus
#from .views import TestView
#xadmin.site.register_view(r'test_view/$', TestView, name='for_test')


class BaseSetting(object):

    enable_themes = True
    use_bootswatch = True



xadmin.site.register(views.CommAdminView, GlobalSetting)

xadmin.site.register(views.BaseAdminView, BaseSetting)



class BuildingAdmin(object):
    model_icon = 'fa  fa-building-o'
    list_display = ['id', 'name', 'status', 'createTime']
    #list_export = ['xls', 'csv']
    search_fields = ['name', 'status']
    list_filter = ['status', 'createTime']
    ordering = ['-createTime']
    #readonly_fields = ['click_nums', 'fav_nums', 'reserve_times']
    # exclude = ['fav_nums']
    list_editable = ['name', 'status']


# Building Register
xadmin.site.register(models.Buildings, BuildingAdmin)

class MeterAdmin(object):
    model_icon = 'fa  fa-tachometer'
    #list_export = ['xls', 'csv']
    list_display = ['id', 'name', 'status','location', 'no', 'building', 'rasp', 'createTime']
    search_fields = ['name', 'status']
    list_filter = ['building','rasp','status', 'createTime']
    ordering = ['-createTime']
    #readonly_fields = ['createTime']
    # exclude = ['fav_nums']
    list_editable = ['name', 'status','lastMinuteTime']

    #獲得當前用戶可管理數據
    def queryset(self):
        if not self.request.user.is_superuser:
            bid=self.request.user.building_id
            bd=models.Buildings.objects.get(id=bid)
            sr = self.model.objects.filter(building=bd)
            return sr 
        return self.model.objects.all()


# Meter Register
xadmin.site.register(models.Meters, MeterAdmin)

class RaspAdmin(object):
    model_icon = 'fa  fa-fax'
    #list_export = ['xls', 'csv']
    list_display = ['id', 'name', 'status','location', 'no', 'building', 'createTime']
    search_fields = ['name', 'status']
    list_filter = ['building','status', 'createTime']
    ordering = ['-createTime']
    #readonly_fields = ['click_nums', 'fav_nums', 'reserve_times']
    # exclude = ['fav_nums']
    list_editable = ['name', 'status']

    #獲得當前用戶可管理數據
    def queryset(self):
        if not self.request.user.is_superuser:
            bid=self.request.user.building_id
            bd=models.Buildings.objects.get(id=bid)
            sr = self.model.objects.filter(building=bd)
            return sr 
        return self.model.objects.all()

# Rasp Register
xadmin.site.register(models.Rasps, RaspAdmin)

class MeterDataAdmin(object):
    model_icon = 'fa  fa-database'
    #list_export = ['xls', 'csv']
    list_display = ['id', 'v1', 'v2', 'v3', 'l1', 'l2', 'l3', 'pf1', 'pf2', 'pf3', 'kwh', 'time', 'rasp', 'meter', 'building', 'createTime']
    #search_fields = ['building']
    list_filter = ['building','time','createTime']
    ordering = ['-createTime']
    #readonly_fields = ['click_nums', 'fav_nums', 'reserve_times']
    # exclude = ['fav_nums']
    #list_editable = ['name', 'status']

    #獲得當前用戶可管理數據
    def queryset(self):
        if not self.request.user.is_superuser:
            bid=self.request.user.building_id
            bd=models.Buildings.objects.get(id=bid)
            sr = self.model.objects.filter(building=bd)
            return sr 
        return self.model.objects.all()

# Rasp Register
xadmin.site.register(models.MeterData, MeterDataAdmin)

class ParamAdmin(object):
    model_icon = 'fa  fa-database'
    #list_export = ['xls', 'csv']
    list_display = ['id', 'paramName', 'paramValue','remark','status','sort', 'createTime']
    search_fields = ['paramName', 'paramValue','remark']
    list_filter = ['status', 'createTime']
    ordering = ['paramName']
    hidden_menu=True

# Param Register
xadmin.site.register(models.Params, ParamAdmin)

class UplogsAdmin(object):
    model_icon = 'fa  fa-file-o'
    #list_export = ['xls', 'csv']
    list_display = ['name', 'file','record_date','status','createTime']
    #search_fields = ['name']
    list_filter = ['status', 'createTime']
    ordering = ['-record_date']
    #hidden_menu=True

# Param Register
xadmin.site.register(models.Uplogs, UplogsAdmin)