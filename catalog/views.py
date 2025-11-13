from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import ProductForm
from .models import Product

class HomePageView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ContactsPageView(TemplateView):
    template_name = 'catalog/contacts.html'

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
        return super().form_valid(form)


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


class ProductUnpublishView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.owner == request.user or request.user.has_perm('catalog.can_unpublish_product'):
            product.is_published = False
            product.save(update_fields=['is_published'])
            messages.success(request, 'Публикация продукта отменена.')
            return redirect('product_detail', pk=product.pk)
        raise PermissionDenied("Недостаточно прав для отмены публикации продукта.")

