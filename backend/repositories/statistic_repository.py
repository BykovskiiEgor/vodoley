from abc import ABC, abstractmethod
from datetime import date
from django.db.models import Sum
from django.db.models.functions import TruncHour, TruncDay, TruncMonth
from typing import List, Dict, Literal, Optional


from orders.models import OrderItem, Order

class IStatisticRepository(ABC):
    """Abstarct statistic class."""
    
    @abstractmethod
    def get_total_sales(self):
        """Abstarct method."""
        pass
    
    
    @abstractmethod
    def get_sales_by_date(self, date_start: date, date_end: date):
        """Abstarct method."""
        pass
          
    
    @abstractmethod
    def get_orders_count_by_status(self, status: str) -> int:
        """Abstarct method."""
        pass
    
    
    @abstractmethod
    def get_order_by_perid_chart(self):
        """Abstarct method."""
        pass
    
    @abstractmethod
    def get_top_items_in_period(self):
        """Abstarct method."""
        pass
    
    
    
class StatisticRepository(IStatisticRepository):
    """StatisticRepository."""
    
    def get_total_sales(self):
        """Get total sales method."""
        result = Order.objects.filter(status='Доставлен').aggregate(total=Sum('total_price'))
        return result['total'] or 0
    
    
    def get_sales_by_date(self, date_start: date, date_end: date):
        """Get sales by date method."""
        result = Order.objects.filter(
            status='Доставлен',
            order_date__date__gte=date_start,
            order_date__date__lte=date_end,
        ).aggregate(
            total_sales=Sum('total_price')
        )
        
        return float(result['total_sales']) if result['total_sales'] is not None else 0.0            
                                           
    
    def get_orders_count_by_status(self, status: str) -> int:
        return Order.objects.filter(status=status).count()
    
    
    def get_order_by_perid_chart(self, date_start: date, date_end: date, period: Literal['hour', 'day', 'month']):
        trunc_map = {
            'hour': TruncHour,
            'day': TruncDay,
            'month': TruncMonth,
        }
        
        return list(
            Order.objects
            .filter(
                status='Доставлен',
                order_date__date__gte=date_start,
                order_date__date__lte=date_end,
            )
            .annotate(period=trunc_map[period]('order_date'))
            .values('period')
            .annotate(total=Sum('total_price'))
            .order_by('period'),
        )
        
        
    def get_top_items_in_period(self, date_start: date, date_end: date):
        """Get top sold items in period."""
        return (
            OrderItem.objects.filter(
                order__order_date__date__gte=date_start,
                order__order_date__date__lte=date_end,
            )
            .values('item__name')  
            .annotate(total_quantity=Sum('quantity'))  
            .order_by('-total_quantity')[:10]  
        )
        
    
    
