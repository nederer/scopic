from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from home_page.models import Product
from api.models import UserAutoBidding

from scopic_task import settings


class HomePageView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "home.html"
    paginate_by = 10
    context_object_name = "products"

    def get_ordering(self):
        ordering = self.request.GET.get('ordering')
        if ordering not in ["current_bid", "-current_bid"]:
            ordering = "id"
        return ordering

    def get_queryset(self):
        query = Q()
        queryset = self.model.objects.all()
        
        search_text = self.request.GET.get('search')
        if search_text:
            query &= Q(title__icontains=search_text) | Q(description__icontains=search_text)

        ordering = self.get_ordering()
        return queryset.filter(query).order_by(ordering)


class ProductView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "product.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['highest_bid'] = settings.HIGHEST_BID
        return context


class AutoBiddingView(LoginRequiredMixin, DetailView):
    template_name = "auto-bidding.html"
    context_object_name = "bidding"

    def get_object(self, queryset=None):
        return UserAutoBidding.objects.get(user=self.request.user)
