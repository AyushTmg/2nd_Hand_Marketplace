from django.views import View
from .models import (
    Item,
    Image,
    Comment,
    Reply,
    Category
)

from .forms import (
    ItemForm,
    ImageForm,
    CommentForm,
    ReplyForm
)


from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,CreateView,DetailView,DeleteView


from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin



# ! Home View
class HomeView(TemplateView):
    template_name='marketplace/home.html'

    def get_context_data(self, **kwargs):
        """
        Passing items and categories to templates
        """
        context=super().get_context_data(**kwargs)
        context['items']=Item.objects.all()
        context['categories']=Category.objects.all()
        return context
    


# ! Item Detail View
class ItemDetailView(DetailView,LoginRequiredMixin):
    model = Item
    template_name = 'marketplace/item_detail.html'


    def get_context_data(self, **kwargs):
        """ 
        passing context of similar products and comments related
        to that product
        """
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
        """
        Method for creating a comment
        """
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

    

# ! Create Item View
class CreateItemView(CreateView,LoginRequiredMixin):
    model = Item
    form_class = ItemForm
    template_name = 'marketplace/item_create.html'
    success_url = '/'


    def get_context_data(self, **kwargs):
        """
        For passing a context
        """
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
         """
         This methods redirects user to login page if 
         they are not authenticated
         """
         if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
         else:
            return redirect('login')
    


#! Review View  
class ReplyView(View,LoginRequiredMixin):
    template_name = 'marketplace/add_reply.html'



    def get(self, request, pk):
        """
        Method for getting review and option for
        adding reply to review too
        """
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
    



# ! for Deleting Item view
class ItemDeleteView(DeleteView,LoginRequiredMixin):
    model=Item
    template_name='marketplace/item_delete.html'
    success_url ='/'



# ! For Deleting Comment view
class CommentDeleteView(DeleteView,LoginRequiredMixin):
    model=Comment
    template_name='marketplace/comment_delete.html'
    success_url ='/'
        


# ! For Deleting a Reply view 
class ReplyDeleteView(DeleteView,LoginRequiredMixin):
    model=Reply
    template_name='marketplace/reply_delete.html'
    success_url ='/'
        
        


# ! Category View function for making categories visible to user 
def category(request,pk):
    """  
    This methods helps to filter items by category
    """
    items = Item.objects.filter(category__id=pk).order_by("-created_at")
    category=Category.objects.all()

    context={
        'items':items,
        'categories':category
    }
    
    return render(request,'marketplace/category.html',context)
  