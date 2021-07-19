from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from phones.forms import EntryForm
from phones.models import Entry
from django.views.generic import ListView, CreateView, UpdateView


#
# @csrf_exempt
# @require_POST
# def create_entry(request):
#     form_instance = EntryForm(data=request.POST)
#     if form_instance.is_valid():
#         form_instance.user = request.user
#         entry_object = form_instance.save()
#         return JsonResponse(data={
#             'success': True,
#             'pk': entry_object.pk,
#             'name': entry_object.name,
#             'last_name': entry_object.last_name,
#             'phone_number': entry_object.phone_number
#         }, status=201)
#     else:
#         return JsonResponse(data={
#             'success': False
#         }, status=400)
#

def find_entry(request):
    phone_number = request.GET.get('phone', None)
    status = request.GET.get('status', None)
    choices = {'contain': Entry.objects.filter(phone_number__contains=phone_number),
               'exact': Entry.objects.filter(phone_number__exact=phone_number),
               'start': Entry.objects.filter(phone_number__startswith=phone_number),
               'end': Entry.objects.filter(phone_number__endswith=phone_number)}
    if not phone_number:
        return JsonResponse(data={'success': False, 'error': 'No number specified'}, status=400)
    qs = choices.get(status, Entry.objects.filter(phone_number__contains=phone_number))
    if not qs.count():
        return JsonResponse(data={'success': False, 'error': 'No number specified'}, status=400)
    return JsonResponse(data={'results': list(qs.values()), 'count': qs.count()}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CreateEntry(LoginRequiredMixin, CreateView):
    template_name = 'phones/add_entry.html'
    form_class = EntryForm

    def form_valid(self, form):
        if (User.objects.get(pk=self.request.user.pk).entry_set.filter(
                phone_number__exact=form.instance.phone_number).exists()):
            return JsonResponse(data={'success': False}, status=400)
        form.instance.user = self.request.user
        form.save()
        return JsonResponse(data={
            'success': True,
            'pk': form.instance.user.pk,
            'name': form.instance.name,
            'last_name': form.instance.last_name,
            'phone_number': form.instance.phone_number
        }, status=201)

    def form_invalid(self, form):
        return JsonResponse(data={
            'success': False
        }, status=400)


class Login(LoginView):
    template_name = 'phones/login.html'
    success_url = 'phones:register'

    def form_valid(self, form):
        return redirect('phones:register')


class Logout(LogoutView):
    next_page = 'phones:login'


class ShowContact(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'phones/search.html'
    paginate_by = 2
    context_object_name = 'contacts'

    def get_queryset(self):
        user = self.request.user
        return Entry.objects.filter(user=user)


class EditContact(LoginRequiredMixin, UpdateView):
    model = Entry
    fields = ('name', 'last_name', 'phone_number')
    success_url = reverse_lazy('phones:search')
    template_name = 'phones/entry_form.html'
