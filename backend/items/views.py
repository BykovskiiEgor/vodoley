from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


@staff_member_required
def run_custom_command(request):
    try:
        call_command("update_flexi")
        messages.success(request, "Команда успешно выполнена.")
    except Exception as e:
        messages.error(request, f"Ошибка при выполнении команды: {e}")
    return HttpResponseRedirect(reverse("admin:index"))
