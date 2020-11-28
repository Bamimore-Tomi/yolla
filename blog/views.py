from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView, DetailView,CreateView, DeleteView,UpdateView
from django.db.models import Q
from django.urls import reverse
from .models import Post, Category
from .forms import CommentForm, PostForm

class HomeView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    paginate_by = 5
    
    def get_queryset(self):
        """Filter and order by different values if it is provided in GET parameters"""
        try:
            if "sort" in self.request.GET:
                if self.request.GET["sort"]=="a":
                    return Post.objects.all().order_by("published_date")
                elif self.request.GET["sort"]=="activity":
                    return Post.objects.all().order_by("-comment_count")
                elif self.request.GET["sort"]=="category":
                    return Post.objects.all().order_by("-category")
            if "search" in self.request.GET:
                query = Post.objects.filter(Q(title__icontains=self.request.GET["search"]) |
                                             Q(content__icontains=self.request.GET["search"]))
                print(query)
                if query is not None:
                    return query
        except:
            pass
        return super().get_queryset()
    # Overriding post method to allow this view rec
    # ieve comment.
    def post(self, request, *args, **kwargs):
        # Getting the related post oject based on the post primary key, used as a hidden field the the form.
        post = Post.objects.get(id=int(request.POST.get("post")))
        # Creating a copy of the request querydict so it can be mutated to append the realted post to it.
        data = request.POST.copy()
        data["post"]=post
        form = CommentForm(data)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            # This block should return error it there are after form validation. This is not currently setup in the templates."
            # For now, this just returns a redirect
            return redirect("/")
            
    
class PostCreateView(CreateView):
    model = Post
    fields = ["category","title","author","content"]
    def post(self, request, *args,**kwargs):
        # Returns Object and a boolean
        category = Category.objects.get_or_create(title=request.POST.get("category"))[0]
        # Creating a copy of the request data to mutate it and append the appropraite object
        data = request.POST.copy()
        data["category"] = category
        form = PostForm(data)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            # This error should be passed into the template, just printing it for now
            print(form.errors)
        
class PostDetailView(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get posts in the same category except the this post object itself
        context["related"]=Post.objects.filter(category__title=self.object.category).exclude(title=self.object.title)
        # Fetching related comments through the foreign key object related name
        context["comments"] = Post.objects.get(pk=self.object.pk).comments.all()
        return context
class PostEditView(UpdateView):
    model = Post
    fields = ["category","title","author","content"]
    
    def post(self,request,*args,**kwargs):
        category = Category.objects.get_or_create(title=request.POST.get("category"))[0]
        request.POST=request.POST.copy()
        request.POST["category"]=category
        return super().post(request, **kwargs)
    
class PostDeleteView(DeleteView):
    model = Post
    success_url = "/"
    
    # Did not create a post delete tempalte confirmation. Overriding the post delete reidrect with my custom get method.
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    #There can be a test_func method to ensure the self.request.user has the necessary permission to delete the post i.e ...
    #The user is either an admin or the creator of the post.