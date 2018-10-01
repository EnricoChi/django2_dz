from django.views.generic import ListView

from rank_item.models import Company


class LandView(ListView):
    model = Company
    f = model.objects.filter()
    template_name = 'landing/index.html'

    def get_queryset(self):
        parent = super().get_queryset()
        return parent.filter(is_published=True, category__is_published=True).select_related('category')
