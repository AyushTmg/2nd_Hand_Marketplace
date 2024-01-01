from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,CreateView,DetailView,DeleteView
from django.views import View
from .models import Item,Image,Comment,Reply,Message
from .forms import ItemForm,ImageForm,CommentForm,ReplyForm
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Q



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
                image = Image.objects.create(item=item, image=file)
                

        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
         if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
         else:
            return redirect('login')
    
         
class ReplyView(View):
    template_name = 'marketplace/add_reply.html'

    def get(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        replies = Reply.objects.filter(comment=comment)
        form = ReplyForm()
        context = {
            'form': form,
            'replies': replies,
            'comment': comment
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.user = request.user
            reply.save()
            return redirect(reverse('add-reply', args=[pk]))

        replies = Reply.objects.filter(comment=comment)
        context = {
            'form': form,
            'replies': replies,
            'comment': comment
        }
        return render(request, self.template_name, context)
    
    def dispatch(self, request, *args, **kwargs):
         if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
         else:
            return redirect('login')

class ItemDeleteView(DeleteView):
    model=Item
    template_name='marketplace/item_delete.html'
    success_url ='/'
        
    def dispatch(self, request, *args, **kwargs):
         if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
         else:
            return redirect('login')
         
class CommentDeleteView(DeleteView):
    model=Comment
    template_name='marketplace/comment_delete.html'
    success_url ='/'
        
    def dispatch(self, request, *args, **kwargs):
         if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
         else:
            return redirect('login')
         
class ReplyDeleteView(DeleteView):
    model=Reply
    template_name='marketplace/reply_delete.html'
    success_url ='/'
        
    def dispatch(self, request, *args, **kwargs):
         if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
         else:
            return redirect('login')
         
def chat(request,pk):
    user_model = get_user_model() 
    user = user_model.objects.get(pk=pk)
    messages=[]
    try:
        messages=Message.objects.filter(sender=request.user,receiver=user)
        
    except:
        pass
    context={
        'user_id':pk,
        'messages':messages
    }
    return render(request,'marketplace/chat.html',context)    

def viewChat(request):
    messages=[]
    try:
        messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        
    except:
        pass
    context={
        'messages':messages
    }
    return render(request,'marketplace/view_chat.html',context)  

    

