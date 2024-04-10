from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required

from catalog.forms import ProductForm, VersionForm, ModeratorProductForm
from catalog.models import Product, Version


@permission_required('users.add_product', raise_exception=True)
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        products = Product.objects.all()

        for product in products:
            versions = Version.objects.filter(product=product)
            active_versions = versions.filter(is_active=True)
            if active_versions:
                product.active_version = active_versions.last().name
            else:
                product.active_version = 'Нет активной версии'

        context_data['object_list'] = products
        return context_data


class ContactsView(View):
    def get(self, request):
        return render(request, 'catalog/contacts.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Name: {name}, Phone: {phone}, Message: {message}')
        return super().get(request, *args, **kwargs)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        if self.object.user == self.request.user:
            return self.object
        raise PermissionDenied

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        product = self.get_object()
        versions = Version.objects.filter(product=product)
        active_version = versions.filter(is_active=True).last()

        if active_version:
            product.active_version = active_version.name
        else:
            product.active_version = 'Нет активной версии'

        context_data['object'] = product
        return context_data


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog/product_create'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, formset=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST)
        else:
            context_data['formset'] = VersionFormset()
        context_data['show_create_button'] = not self.request.user.groups.filter(name='moderator').exists()
        return context_data


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        if self.request.user.has_perms(
                (
                        'catalog.change_description_product',
                        'catalog.change_categories_product',
                        'catalog.change_publication_product'
                )
        ) or (self.get_object().user == self.request.user):
            return True
        return self.handle_no_permission()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_form_class(self):
        if self.request.user.groups.filter(name='moderator'):
            return ModeratorProductForm
        return ProductForm


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')
