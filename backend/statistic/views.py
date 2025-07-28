from django.shortcuts import render
from django.views import View
from django import forms
from django.contrib.auth.mixins import UserPassesTestMixin

from services.statistic_service import StatisticService
from repositories.statistic_repository import StatisticRepository

class StatisticForm(forms.Form):
    date_start = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date", "class": "input-custom" }))
    date_end = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date", "class": "input-custom" }))


class StatisticView(UserPassesTestMixin, View):
    template_name = 'statistics/statistics.html'
    
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):
        form = StatisticForm(request.GET or None)
        repo = StatisticRepository()
        service = StatisticService(repository=repo)

        total_sales = service.get_total_sales()
        sales_today = service.get_sales_by_date(None, None)
        new_orders = service.get_new_orders()
        close_orders = service.get_close_orders()

        chart_data = None
        date_start = None
        date_end = None
        items = None

        if form.is_valid():
            date_start = form.cleaned_data.get('date_start')
            date_end = form.cleaned_data.get('date_end')

            if date_start and date_end:
                items = service.get_top_items_in_period(date_start, date_end)
                report = service.get_sales_by_date_chart(date_start, date_end)
                chart_data = {
                    'labels': [item['period'] for item in report['data']],
                    'values': [item['total'] for item in report['data']],
                    'time_unit': report['time_unit'],
                    'total_sum': report['total_sum'],
                }
                date_start = date_start.isoformat()
                date_end = date_end.isoformat()

        context = {
            'form': form,
            'total_sales': total_sales,
            'sales_today': sales_today,
            'new_orders': new_orders,
            'close_orders': close_orders,
            'chart_data': chart_data, 
            'date_start': date_start,
            'date_end': date_end,
            'show_chart': chart_data is not None, 
            'items': items,
        }

        return render(request, self.template_name, context)