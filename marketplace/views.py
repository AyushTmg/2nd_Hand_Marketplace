from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,CreateView,DetailView,FormView,DeleteView
from .models import Item,Image,Comment,Reply
from django.http import JsonResponse
from .forms import ItemForm,ImageForm,CommentForm,ReplyForm
from django.contrib.auth import get_user_model
from django.urls import reverse



class HomeView(TemplateView):
    template_name='marketplace/home.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['items']=Item.objects.all()
        return context
    
    def dispatch(self, request, *args, **kwargs):
         if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
         else:
            return redirect('login')
    
class ItemDetailView(DetailView):
    model = Item
    template_name = 'marketplace/item_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object 
        item_id=item.id
        category = item.category
        comment=Comment.objects.filter(item=item)
        others = Item.objects.exclude(id=item_id).filter(category=category)
        context['comments']=comment
        context['others'] = others
        context['comment_form']=CommentForm()
        return context
    
    def post(self,request, *args, **kwargs):
        item=self.get_object()
        form=CommentForm(request.POST)
        if request.method=='POST':
            if form.is_valid():
                new_comment=form.save(commit=False)
                new_comment.item=item 
                new_comment.user=request.user
                new_comment.save()
                pk=self.kwargs['pk']
                return redirect(reverse('item-detail', args=[pk]))

    


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
    
    def dispatch(self, request, *args, **kwargs):
         if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
         else:
            return redirect('login')
    


def replyView(request,pk):
    comment=get_object_or_404(Comment,id=pk)
    replies=Reply.objects.filter(comment=comment)
    form=ReplyForm()
    if request.method=='POST':
        form=ReplyForm(request.POST)
        if form.is_valid():
            reply=form.save(commit=False)
            reply.comment=comment
            reply.user=request.user
            reply.save()
            redirect(reverse('add-reply', args=[pk]))
    context={
        'form':form,
        'replies':replies,
        'comment':comment
    }
    return render(request,'marketplace/add_reply.html',context)

class ItemDeleteView(DeleteView):
    model=Item
    template_name='marketplace/item_delete.html'
    success_url ='/'
        
    def dispatch(self, request, *args, **kwargs):
         if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
         else:
            return redirect('login')

    

