from django import forms
from .models import Order

class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        if self.instance.pk:
            current_status = self.instance.status
            allowed_statuses = [
                s for s, _ in Order.STATUS_CHOICES
                if Order.STATUS_ORDER[s] >= Order.STATUS_ORDER[current_status]
            ]
            self.fields['status'].choices = [
                (s, label) for s, label in Order.STATUS_CHOICES if s in allowed_statuses
            ]
