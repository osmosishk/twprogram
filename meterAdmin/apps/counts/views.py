from xadmin.views import CommAdminView
from django.shortcuts import render
from counts import models
from bases.models import Buildings

class minuteView(CommAdminView):
    def get(self, request):
        context = super().get_context()

        qs=models.MinuteCount.objects.all()
        if not self.request.user.is_superuser:
            bid=self.request.user.building_id
            bd=Buildings.objects.get(id=bid)
            qs = models.MinuteCount.objects.filter(building=bd)#.order_by('-dt')[:15]
        #init params
        title = "分鐘統計圖"
        minv=0
        title_list=['v1', 'v2', 'v3']
        date_list=[]
        v1_list=[]
        v2_list=[]
        v3_list=[]
        kwh_list=[]

        #filter
        sf_building,sf_dts,sf_dte="","",""
        try:
            sf_building=self.request.GET['_p_building__id__exact']
            qs=qs.filter(building_id=sf_building)
        except:
            pass
        try:
            sf_dts=self.request.GET['_p_dt__gte']
            sf_dte=self.request.GET['_p_dt__lt']
            sf_dts_=datetime.datetime.strptime(sf_dts,"%Y-%m-%d")
            sf_dte_=datetime.datetime.strptime(sf_dte,"%Y-%m-%d")
            qs=qs.filter(dt__gte=sf_dts_,dt__lt=sf_dte_)
        except Exception as e:
            print(e)

        #add values
        for q in qs:
            v1_list.append(q.v1)
            v2_list.append(q.v2)
            v3_list.append(q.v3)
            kwh_list.append(q.kwh)
            date_list.append(q.dt.strftime("%Y-%m-%d %H:%M"))

        context["breadcrumbs"].append({'url': '#', 'title': title})
        context["title"] = title
        context["minv"] = minv

        context["title_list"] = title_list
        context["date_list"] = date_list
        context["v1_list"] = v1_list
        context["v2_list"] = v2_list
        context["v3_list"] = v3_list
        context["kwh_list"] = kwh_list
        
        return render(request, 'xadmin/countchart.html', context)

class hourView(CommAdminView):
    list_filter = ['building','dt']
    def get(self, request):
        context = super().get_context()

        title = "小時統計"
        title_list=['v1', 'v2', 'v3', 'kwh']
        date_list=[]
        v1_list=[]
        v2_list=[]
        v3_list=[]
        kwh_list=[]

        qs=models.HourCount.objects.all().order_by('-dt')[:10]
        if not self.request.user.is_superuser:
            bid=self.request.user.building_id
            bd=Buildings.objects.get(id=bid)
            qs = models.HourCount.objects.filter(building=bd).order_by('-dt')[:10]
        minv=2600
        for q in qs:
            v1_list.append(q.v1)
            v2_list.append(q.v2)
            v3_list.append(q.v3)
            kwh_list.append(q.kwh)
            date_list.append(q.dt)
            if q.v1<minv:
                minv=q.v1

        context["breadcrumbs"].append({'url': '#', 'title': title})
        context["title"] = title
        context["minv"] = minv

        context["title_list"] = title_list
        context["date_list"] = date_list
        context["v1_list"] = v1_list
        context["v2_list"] = v2_list
        context["v3_list"] = v3_list
        context["kwh_list"] = kwh_list
        
        return render(request, 'xadmin/countdata.html', context)


class dayView(CommAdminView):
    def get(self, request):
        context = super().get_context()

        title = "日統計"
        title_list=['v1', 'v2', 'v3', 'kwh']
        date_list=[]
        v1_list=[]
        v2_list=[]
        v3_list=[]
        kwh_list=[]

        qs=models.DayCount.objects.all().order_by('-dt')[:10]
        if not self.request.user.is_superuser:
            bid=self.request.user.building_id
            bd=Buildings.objects.get(id=bid)
            qs = models.DayCount.objects.filter(building=bd).order_by('-dt')[:10]
        minv=0
        for q in qs:
            v1_list.append(q.v1)
            v2_list.append(q.v2)
            v3_list.append(q.v3)
            kwh_list.append(q.kwh)
            date_list.append(q.dt)
            if q.v1<minv:
                minv=q.v1

        context["breadcrumbs"].append({'url': '#', 'title': title})
        context["title"] = title
        context["minv"] = minv

        context["title_list"] = title_list
        context["date_list"] = date_list
        context["v1_list"] = v1_list
        context["v2_list"] = v2_list
        context["v3_list"] = v3_list
        context["kwh_list"] = kwh_list
        
        return render(request, 'xadmin/countdata.html', context)

class monthView(CommAdminView):
    def get(self, request):
        context = super().get_context()

        title = "月統計"
        title_list=['v1', 'v2', 'v3', 'kwh']
        date_list=[]
        v1_list=[]
        v2_list=[]
        v3_list=[]
        kwh_list=[]

        qs=models.MonthCount.objects.all().order_by('-dt')[:10]
        if not self.request.user.is_superuser:
            bid=self.request.user.building_id
            bd=Buildings.objects.get(id=bid)
            qs = models.MonthCount.objects.filter(building=bd).order_by('-dt')[:10]
        minv=2600
        for q in qs:
            v1_list.append(q.v1)
            v2_list.append(q.v2)
            v3_list.append(q.v3)
            kwh_list.append(q.kwh)
            date_list.append(q.dt)
            if q.v1<minv:
                minv=q.v1

        context["breadcrumbs"].append({'url': '#', 'title': title})
        context["title"] = title
        context["minv"] = minv

        context["title_list"] = title_list
        context["date_list"] = date_list
        context["v1_list"] = v1_list
        context["v2_list"] = v2_list
        context["v3_list"] = v3_list
        context["kwh_list"] = kwh_list
        
        return render(request, 'xadmin/countdata.html', context)
