from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Basket
from rank_item.models import Company


@login_required
def basket_add(request):
    if request.method == 'POST' and request.is_ajax():
        company = get_object_or_404(Company, pk=request.POST.get('company_id'))
        added_item = Basket.objects.filter(user=request.user, company=company)
        count = 1

        if added_item:
            added_item[0].quantity += 1
            added_item[0].save()
            count = added_item[0].quantity
        else:
            item = Basket(user=request.user, company=company)
            item.quantity = 1
            item.save()

        return JsonResponse({
            'success':
                {'count': count}
        })
    raise Http404
