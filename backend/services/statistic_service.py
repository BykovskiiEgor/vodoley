from datetime import date
from datetime import timedelta
from decimal import Decimal
from typing import Literal

from category.models import Categories
from django.db.models.functions import TruncDay
from django.db.models.functions import TruncHour
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
from repositories.statistic_repository import IStatisticRepository


class StatisticService:
    """StatisticService."""

    def __init__(self, repository: IStatisticRepository):
        self.repository = repository

    def get_total_sales(self) -> float:
        return self.repository.get_total_sales()

    def get_sales_by_date(self, date_start: date, date_end: date) -> float:
        if date_start == None and date_end == None:
            date_start = now().date()
            date_end = now().date()
        return self.repository.get_sales_by_date(date_start, date_end)

    def get_sales_by_category(self, category: Categories):
        return self.repository.get_sales_by_category(category)

    def get_new_orders(self):
        return self.repository.get_orders_count_by_status(status="В ожидании")

    def get_close_orders(self):
        return self.repository.get_orders_count_by_status(status="Доставлен")

    def _determine_time_unit(self, date_start: date, date_end: date) -> Literal["hour", "day", "month"]:
        """Определяет единицу группировки на основе периода."""
        delta = date_end - date_start

        if delta <= timedelta(days=1):
            return "hour"
        elif delta <= timedelta(days=31):
            return "day"
        return "month"

    def _get_trunc_function(self, time_unit: str):
        """Возвращает функцию для группировки по времени."""
        return {
            "hour": TruncHour,
            "day": TruncDay,
            "month": TruncMonth,
        }[time_unit]

    def _format_period(self, period, time_unit: str) -> str:
        """Форматирует период для отображения."""
        if time_unit == "hour":
            return period.strftime("%Y-%m-%d %H:%M")
        elif time_unit == "day":
            return period.strftime("%Y-%m-%d")
        return period.strftime("%Y-%m")

    def get_sales_by_date_chart(self, date_start: date, date_end: date):
        time_unit = self._determine_time_unit(date_start, date_end)

        sales_data = self.repository.get_order_by_perid_chart(date_start, date_end, time_unit)

        formatted_data = [
            {
                "period": self._format_period(item["period"], time_unit),
                "total": float(item["total"]) if item["total"] else 0.0,
            }
            for item in sales_data
        ]

        total_sum = sum(Decimal(str(item["total"])) for item in formatted_data)

        return {
            "data": formatted_data,
            "time_unit": time_unit,
            "total_sum": total_sum,
        }

    def get_top_items_in_period(self, date_start: date, date_end: date):
        raw_items = self.repository.get_top_items_in_period(date_start, date_end)
        items = list(raw_items)

        if not items:
            return []

        max_quantity = items[0]["total_quantity"]

        for item in items:
            item["width_percent"] = round((item["total_quantity"] / max_quantity) * 100)

        return items
