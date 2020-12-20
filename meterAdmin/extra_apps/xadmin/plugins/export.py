import io
import datetime
import sys
from future.utils import iteritems

from django.http import HttpResponse
from django.template import loader
from django.utils import six
from django.utils.encoding import force_text, smart_text
from django.utils.html import escape
from django.utils.translation import ugettext as _
from django.utils.xmlutils import SimplerXMLGenerator
from django.db.models import BooleanField, NullBooleanField

from xadmin.plugins.utils import get_context_dict
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, ListAdminView
from xadmin.util import json
from xadmin.views.list import ALL_VAR

try:
    import xlwt
    has_xlwt = True
except:
    has_xlwt = False

try:
    import xlsxwriter
    has_xlsxwriter = True
except:
    has_xlsxwriter = False


class ExportMenuPlugin(BaseAdminPlugin):

    list_export = ('xlsx', 'xls', 'csv', 'xml', 'json')
    export_names = {'xlsx': 'Excel 2007', 'xls': 'Excel', 'csv': 'CSV',
                    'xml': 'XML', 'json': 'JSON'}

    def init_request(self, *args, **kwargs):
        self.list_export = [
            f for f in self.list_export
            if (f != 'xlsx' or has_xlsxwriter) and (f != 'xls' or has_xlwt)]

    def block_top_toolbar(self, context, nodes):
        if self.list_export:
            context.update({
                'show_export_all': self.admin_view.paginator.count > self.admin_view.list_per_page and not ALL_VAR in self.admin_view.request.GET,
                'form_params': self.admin_view.get_form_params({'_do_': 'export'}, ('export_type',)),
                'export_types': [{'type': et, 'name': self.export_names[et]} for et in self.list_export],
            })
            nodes.append(loader.render_to_string('xadmin/blocks/model_list.top_toolbar.exports.html',
                                                 context=get_context_dict(context)))


class ExportPlugin(BaseAdminPlugin):

    export_mimes = {'xlsx': 'application/vnd.ms-excel',
                    'xls': 'application/vnd.ms-excel',
                    'csv': 'text/csv',
                    'xml': 'application/xhtml+xml',
                    'json': 'application/json'}

    def init_request(self, *args, **kwargs):
        return self.request.GET.get('_do_') == 'export'

    def _format_value(self, o):
        if (o.field is None and getattr(o.attr, 'boolean', False)) or \
           (o.field and isinstance(o.field, (BooleanField, NullBooleanField))):
                value = o.value
        elif str(o.text).startswith("<span class='text-muted'>"):
            value = escape(str(o.text)[25:-7])
        else:
            value = escape(str(o.text))
        return value

    def _get_objects(self, context):
        headers = [c for c in context['result_headers'].cells if c.export]
        rows = context['results']

        return [dict([
            (force_text(headers[i].text), self._format_value(o)) for i, o in
            enumerate(filter(lambda c:getattr(c, 'export', False), r.cells))]) for r in rows]

    def _get_datas(self, context):
        rows = context['results']

        new_rows = [[self._format_value(o) for o in
            filter(lambda c:getattr(c, 'export', False), r.cells)] for r in rows]
        new_rows.insert(0, [force_text(c.text) for c in context['result_headers'].cells if c.export])
        return new_rows

    def get_xlsx_export(self, context):
        datas = self._get_datas(context)
        output = io.BytesIO()
        export_header = (
            self.request.GET.get('export_xlsx_header', 'off') == 'on')

        model_name = self.opts.verbose_name
        book = xlsxwriter.Workbook(output)
        sheet = book.add_worksheet()
        styles = {'datetime': book.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss'}),
                  'date': book.add_format({'num_format': 'yyyy-mm-dd'}),
                  'time': book.add_format({'num_format': 'hh:mm:ss'}),
                  'header': book.add_format({'font': 'name Times New Roman', 'color': 'red', 'bold': 'on', 'num_format': '#,##0.00'}),
                  'default': book.add_format()}

        if not export_header:
            datas = datas[1:]
        for rowx, row in enumerate(datas):
            for colx, value in enumerate(row):
                if export_header and rowx == 0:
                    cell_style = styles['header']
                else:
                    if isinstance(value, datetime.datetime):
                        cell_style = styles['datetime']
                    elif isinstance(value, datetime.date):
                        cell_style = styles['date']
                    elif isinstance(value, datetime.time):
                        cell_style = styles['time']
                    else:
                        cell_style = styles['default']
                try:
                    sheet.write(rowx, colx, int(value), cell_style)
                except:
                    sheet.write(rowx, colx, value, cell_style)
        lines=rowx+1
        if ("統計" in model_name)==False:
            book.close()
            output.seek(0)
            return output.getvalue()
        # add line chart
        chart_col = book.add_chart({'type': 'line'})
        chart_col.width=600
        chart_col.height=400

        # add series
        chart_col.add_series({
        'name': '=Sheet1!$C$1',
        'categories': '=Sheet1!$B$2:$B$%d'%lines,
        'values':   '=Sheet1!$C$2:$C$%d'%lines,
        'line': {'color': 'blue'},
        })

        # add series
        chart_col.add_series({
        'name': '=Sheet1!$D$1',
        'categories':  '=Sheet1!$B$2:$B$%d'%lines,
        'values':   '=Sheet1!$D$2:$D$%d'%lines,
        'line': {'color': 'brown'},
        })

        #if model_name=="每日統計表":
        # add series
        chart_col.add_series({
        'name': '=Sheet1!$E$1',
        'categories':  '=Sheet1!$B$2:$B$%d'%lines,
        'values':   '=Sheet1!$E$2:$E$%d'%lines,
        'line': {'color': 'black'},
        })

        # title and x y info
        chart_col.set_title({'name': '電壓圖'})
        chart_col.set_x_axis({'name': 'Date'})
        chart_col.set_y_axis({'name':  'Value'})

        chart_col.set_style(2)

        # set chart location
        sheet.insert_chart('Q1', chart_col, {'x_offset': 25, 'y_offset': 10})

        #chart for l1 l2 l3
        # add line chart
        chart_col = book.add_chart({'type': 'line'})
        chart_col.width=600
        chart_col.height=400

        # add series
        chart_col.add_series({
        'name': '=Sheet1!$F$1',
        'categories': '=Sheet1!$B$2:$B$%d'%lines,
        'values':   '=Sheet1!$F$2:$F$%d'%lines,
        'line': {'color': 'blue'},
        })

        # add series
        chart_col.add_series({
        'name': '=Sheet1!$G$1',
        'categories':  '=Sheet1!$B$2:$B$%d'%lines,
        'values':   '=Sheet1!$G$2:$G$%d'%lines,
        'line': {'color': 'brown'},
        })

        #if model_name=="每日統計表":
        # add series
        chart_col.add_series({
        'name': '=Sheet1!$H$1',
        'categories':  '=Sheet1!$B$2:$B$%d'%lines,
        'values':   '=Sheet1!$H$2:$H$%d'%lines,
        'line': {'color': 'black'},
        })

        # title and x y info
        chart_col.set_title({'name': '電流圖'})
        chart_col.set_x_axis({'name': 'Date'})
        chart_col.set_y_axis({'name':  'Value'})

        chart_col.set_style(2)

        # set chart location
        sheet.insert_chart('Q20', chart_col, {'x_offset': 25, 'y_offset': 10})

        #chart for kav karl kw
        if model_name=="每日統計表" or model_name=="每月統計表":
            # add line chart
            chart_col = book.add_chart({'type': 'line'})
            chart_col.width=600
            chart_col.height=400

            # add series
            chart_col.add_series({
            'name': '=Sheet1!$L$1',
            'categories': '=Sheet1!$B$2:$B$%d'%lines,
            'values':   '=Sheet1!$L$2:$L$%d'%lines,
            'line': {'color': 'blue'},
            })

            # add series
            chart_col.add_series({
            'name': '=Sheet1!$M$1',
            'categories':  '=Sheet1!$B$2:$B$%d'%lines,
            'values':   '=Sheet1!$M$2:$M$%d'%lines,
            'line': {'color': 'brown'},
            })

            # add series
            chart_col.add_series({
            'name': '=Sheet1!$N$1',
            'categories':  '=Sheet1!$B$2:$B$%d'%lines,
            'values':   '=Sheet1!$N$2:$N$%d'%lines,
            'line': {'color': 'black'},
            })

            # add series
            chart_col.add_series({
            'name': '=Sheet1!$O$1',
            'categories':  '=Sheet1!$B$2:$B$%d'%lines,
            'values':   '=Sheet1!$O$2:$O$%d'%lines,
            'line': {'color': 'orange'},
            })

            # title and x y info
            chart_col.set_title({'name': '其他數據'})
            chart_col.set_x_axis({'name': 'Date'})
            chart_col.set_y_axis({'name':  'Value'})

            chart_col.set_style(2)

            # set chart location
            sheet.insert_chart('Q40', chart_col, {'x_offset': 25, 'y_offset': 10})

        book.close()

        output.seek(0)
        return output.getvalue()

    def get_xls_export(self, context):
        datas = self._get_datas(context)
        output = io.BytesIO()
        export_header = (
            self.request.GET.get('export_xls_header', 'off') == 'on')

        model_name = self.opts.verbose_name
        book = xlwt.Workbook(encoding='utf8')
        sheet = book.add_sheet(
            u"%s %s" % (_(u'Sheet'), force_text(model_name)))
        styles = {'datetime': xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm:ss'),
                  'date': xlwt.easyxf(num_format_str='yyyy-mm-dd'),
                  'time': xlwt.easyxf(num_format_str='hh:mm:ss'),
                  'header': xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00'),
                  'default': xlwt.Style.default_style}

        if not export_header:
            datas = datas[1:]
        for rowx, row in enumerate(datas):
            for colx, value in enumerate(row):
                if export_header and rowx == 0:
                    cell_style = styles['header']
                else:
                    if isinstance(value, datetime.datetime):
                        cell_style = styles['datetime']
                    elif isinstance(value, datetime.date):
                        cell_style = styles['date']
                    elif isinstance(value, datetime.time):
                        cell_style = styles['time']
                    else:
                        cell_style = styles['default']
                sheet.write(rowx, colx, value, style=cell_style)
        book.save(output)

        output.seek(0)
        return output.getvalue()
    #Rain add in 20200925
    def get_xlschart_export(self,context):
        datas = self._get_datas(context)
        output = io.BytesIO()
        export_header = (
            self.request.GET.get('export_xls_header', 'off') == 'on')
        
        # 創建一個excel
        workbook = xlsxwriter.Workbook("chart_line.xls")
        # 創建一個sheet
        worksheet = workbook.add_worksheet()
        # worksheet = workbook.add_worksheet("bug_analysis")

        # 自訂樣式，加粗
        bold = workbook.add_format({'bold': 1})

        # --------1、準備資料並寫入excel---------------
        # 向excel中寫入資料，建立圖示時要用到
        headings = ['Number', 'testA', 'testB']
        data = [
            ['2017-9-1', '2017-9-2', '2017-9-3', '2017-9-4', '2017-9-5', '2017-9-6'],
            [10, 40, 50, 20, 10, 50],
            [30, 60, 70, 50, 40, 30],
        ]

        # 寫入表頭
        worksheet.write_row('A1', headings, bold)

        # 寫入資料
        worksheet.write_column('A2', data[0])
        worksheet.write_column('B2', data[1])
        worksheet.write_column('C2', data[2])

        # 創建一個柱狀圖(line chart)
        chart_col = workbook.add_chart({'type': 'line'})

        # 配置第一個系列資料
        chart_col.add_series({
        # 這裡的sheet1是默認的值，因為我們在新建sheet時沒有指定sheet名
        # 如果我們新建sheet時設置了sheet名，這裡就要設置成相應的值
        'name': '=Sheet1!$B$1',
        'categories': '=Sheet1!$A$2:$A$7',
        'values':   '=Sheet1!$B$2:$B$7',
        'line': {'color': 'red'},
        })

        # 配置第二個系列資料
        chart_col.add_series({
        'name': '=Sheet1!$C$1',
        'categories':  '=Sheet1!$A$2:$A$7',
        'values':   '=Sheet1!$C$2:$C$7',
        'line': {'color': 'yellow'},
        })

        # 設置圖表的title 和 x，y軸資訊
        chart_col.set_title({'name': 'The xxx site Bug Analysis'})
        chart_col.set_x_axis({'name': 'Test number'})
        chart_col.set_y_axis({'name':  'Sample length (mm)'})

        # 設置圖表的風格
        chart_col.set_style(1)

        # 把圖表插入到worksheet並設置偏移
        worksheet.insert_chart('A10', chart_col, {'x_offset': 25, 'y_offset': 10})
        workbook.close() 

        output.seek(0)
        return output.getvalue()

    def _format_csv_text(self, t):
        if isinstance(t, bool):
            return _('Yes') if t else _('No')
        t = t.replace('"', '""').replace(',', '\,')
        cls_str = str if six.PY3 else basestring
        if isinstance(t, cls_str):
            t = '"%s"' % t
        return t

    def get_csv_export(self, context):
        datas = self._get_datas(context)
        stream = []

        if self.request.GET.get('export_csv_header', 'off') != 'on':
            datas = datas[1:]

        for row in datas:
            stream.append(','.join(map(self._format_csv_text, row)))

        return '\r\n'.join(stream)

    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                xml.startElement("row", {})
                self._to_xml(xml, item)
                xml.endElement("row")
        elif isinstance(data, dict):
            for key, value in iteritems(data):
                key = key.replace(' ', '_')
                xml.startElement(key, {})
                self._to_xml(xml, value)
                xml.endElement(key)
        else:
            xml.characters(smart_text(data))

    def get_xml_export(self, context):
        results = self._get_objects(context)
        stream = io.StringIO()

        xml = SimplerXMLGenerator(stream, "utf-8")
        xml.startDocument()
        xml.startElement("objects", {})

        self._to_xml(xml, results)

        xml.endElement("objects")
        xml.endDocument()

        return stream.getvalue().split('\n')[1]

    def get_json_export(self, context):
        results = self._get_objects(context)
        return json.dumps({'objects': results}, ensure_ascii=False,
                          indent=(self.request.GET.get('export_json_format', 'off') == 'on') and 4 or None)

    def get_response(self, response, context, *args, **kwargs):
        file_type = self.request.GET.get('export_type', 'csv')
        response = HttpResponse(
            content_type="%s; charset=UTF-8" % self.export_mimes[file_type])

        file_name = self.opts.verbose_name.replace(' ', '_')
        response['Content-Disposition'] = ('attachment; filename=%s.%s' % (
            file_name, file_type)).encode('utf-8')

        response.write(getattr(self, 'get_%s_export' % file_type)(context))
        return response

    # View Methods
    def get_result_list(self, __):
        if self.request.GET.get('all', 'off') == 'on':
            self.admin_view.list_per_page = sys.maxsize
        return __()

    def result_header(self, item, field_name, row):
        item.export = not item.attr or field_name == '__str__' or getattr(item.attr, 'allow_export', True)
        return item

    def result_item(self, item, obj, field_name, row):
        item.export = item.field or field_name == '__str__' or getattr(item.attr, 'allow_export', True)
        return item


site.register_plugin(ExportMenuPlugin, ListAdminView)
site.register_plugin(ExportPlugin, ListAdminView)
