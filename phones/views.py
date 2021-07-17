from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from phones.forms import EntryForm
from phones.models import Entry


@csrf_exempt
@require_POST
def create_entry(request):
    form_instance = EntryForm(data=request.POST)
    if form_instance.is_valid():
        entry_object = form_instance.save()
        return JsonResponse(data={
            'success': True,
            'pk': entry_object.pk,
            'name': entry_object.name,
            'last_name': entry_object.last_name,
            'phone_number': entry_object.phone_number
        }, status=201)
    else:
        return JsonResponse(data={
            'success': False
        }, status=400)


@require_GET
def show_add_entry_form(request):
    return render(request, 'phones/add_entry.html', context={'form': EntryForm()})


@require_GET
def show_search_form(request):
    return render(request, 'phones/search.html')


def find_entry(request):
    phone_number = request.GET.get('phone', None)
    if not phone_number:
        return JsonResponse(data={'success': False, 'error': 'No number specified'}, status=400)

    qs = Entry.objects.filter(phone_number__contains=phone_number)
    if not qs.count():
        return JsonResponse(data={'success': False, 'error': 'No number specified'}, status=400)
    return JsonResponse(data={'results': list(qs.values()), 'count': qs.count()}, status=200)
