from typing import Any
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,DetailView
from .models import Item,Image
from .forms import ItemForm,ImageForm


class HomeView(TemplateView):
    template_name='marketplace/home.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context=super().get_context_data(**kwargs)
        context['items']=Item.objects.all()
        return context
    
class ItemDetailView(DetailView):
    model = Item
    template_name = 'marketplace/item_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object 
        item_id=item.id
        category = item.category
        others = Item.objects.exclude(id=item_id).filter(category=category)
        context['others'] = others
        return context
    


class CreateItemView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'marketplace/item_create.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = ImageForm()
        return context

    def form_valid(self, form):
        item = form.save(commit=False)
        item.user = self.request.user
        item.save()

        image_form = ImageForm(self.request.POST, self.request.FILES)
        if image_form.is_valid():
            for file in image_form.cleaned_data['image']:
                image = Image(item=item, image=file)
                image.save()
        return super().form_valid(form)