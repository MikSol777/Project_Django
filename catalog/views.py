from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import ProductForm
from .models import Category, Product
from .services import (
    get_cached_products_list,
    get_products_by_category,
    invalidate_products_cache,
)


def cache_page_if_enabled(timeout: int):
    def decorator(view_func):
        if settings.CACHE_ENABLED:
            return cache_page(timeout)(view_func)
        return view_func

    return decorator

class HomePageView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('category')
        if settings.CACHE_ENABLED:
            return get_cached_products_list()
        return queryset

class ContactsPageView(TemplateView):
    template_name = 'catalog/contacts.html'

@method_decorator(cache_page_if_enabled(60 * 15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        invalidate_products_cache()
        return response


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home_page')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        invalidate_products_cache()
        return response


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('home_page')

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('catalog.delete_product'):
            return queryset
        return queryset.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.has_perm('catalog.delete_product'):
            raise PermissionDenied("Недостаточно прав для удаления продукта.")
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        invalidate_products_cache()
        return response


class ProductUnpublishView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.owner == request.user or request.user.has_perm('catalog.can_unpublish_product'):
            product.is_published = False
            product.save(update_fields=['is_published'])
            messages.success(request, 'Публикация продукта отменена.')
            invalidate_products_cache()
            return redirect('product_detail', pk=product.pk)
        raise PermissionDenied("Недостаточно прав для отмены публикации продукта.")


class CategoryProductsView(ListView):
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, pk=self.kwargs['category_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return get_products_by_category(self.category.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

