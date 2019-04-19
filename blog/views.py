from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Post, Rating
from django.contrib.auth.models import User
from users.models import Profile
from django.core import serializers
from .forms import Recipes, findByIngredients
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.db.models import Count
from django.db.models import Avg
import json
from django.db.models import Q
def home(request):
    return render(request, 'blog/home.html')

def post (request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/post.html', context)

def results(request):
    search_result= {}
    if 'food' in request.GET: #check item entered
        form= Recipes(request.GET) #call the class from forms.py
        if form.is_valid():
            search_result= form.search() #fill the search_result variable with the response obtained from the API

    else:
        form= Recipes()
    return render(request, 'blog/results.html', {'form': form, 'search_result': search_result}) #parse the response to the template

def result_ing(request):
    search_result= {}
    if 'ingredients' in request.GET:
        form= findByIngredients(request.GET)
        if form.is_valid():
            search_result= form.ingred()
    else:
        form= findByIngredients()
    return render(request, 'blog/ingredients.html', {'form': form, 'search_result': search_result})



def info (request, id):

    recipe= Recipes.info(str(id))
    jokes=Recipes.joke()
    return render(request,'blog/info.html', {'recipe': recipe,'jokes': jokes})

def random (request):
    random= Recipes.random()
    return render (request, 'blog/random.html', {'random': random})


@login_required
def rate(request):
    if request.method == 'GET':
        rating = Rating.objects.get_or_create(recipe=request.GET.get('recipe', None), rating=request.GET.get('rating', None),user=User.objects.get(id=request.session['_auth_user_id']))


    return render(request,'blog/info.html', {'rating':rating} )
@login_required
def getRating(request, recipeId):
    if request.method == 'GET':
        total = 0
        count = 0
        userRating = 0
        ratings = Rating.objects.all().filter(recipe=recipeId)
        for rating in ratings:
            total += rating.rating
            count += 1
            if (str(rating.user.id) == request.session['_auth_user_id']):
                userRating = rating.rating
        average = total/count
        return JsonResponse(json.loads(json.dumps({'average': average, 'userRating': userRating})))

@login_required
def user_recommendation_list(request):

    user_rating = Rating.objects.filter(user_id=request.user.id)
    user_rating_recipe_ids = set(map(lambda x: x.user_id, user_rating)) #get current user id
    recipe_list = Rating.objects.exclude(user_id__in=user_rating_recipe_ids) #exclude current user
     #count how many recipes were rated and sort in descending order
    #now recipes that had a high average and were rated the most will be recommended
    anno=recipe_list.values('recipe').annotate(Avg('rating')).order_by('-rating__avg') #compute average of ratings and order in descending order
    unique_recipe=anno.annotate(Count('recipe')).order_by('-recipe__count')
    unique= unique_recipe.values_list('recipe',flat=True)
    uniquea=[]
    for un in unique:
        id= str(un)
        uniquea.append(Recipes.info(id))

    others=recipe_list.values('recipe').filter(Q(rating=5) | Q(rating= 4))#get rating of recipes with 4 and 5 rated by others
    me= user_rating.values('recipe').filter(Q(rating=5) | Q(rating= 4))#get rating of recipes with 4 and 5 rated by me
    similar=others.filter(recipe__in=me).filter(recipe__in=others)#filter by common recipes
    similarity= Rating.objects.filter(recipe__in=similar).exclude(id__in=user_rating)#to get recipe objects that were rated by those users that rated common recipes as me
    user=set(map(lambda x:x.user_id,similarity))#get the user_id of common raters
    user_high=unique_recipe.filter(user_id__in=user)[:5]#get 5 recipes of common raters
    listing_high= user_high.values('recipe')





    others_low=recipe_list.values('recipe').filter(Q(rating=1) | Q(rating= 2))
    me_low= user_rating.values('recipe').filter(Q(rating=1) | Q(rating= 2))
    similar_low=others.filter(recipe__in=me_low).filter(recipe__in=others_low)
    similarity_low= Rating.objects.filter(recipe__in=similar_low).exclude(id__in=user_rating)
    user_low=set(map(lambda x:x.user_id,similarity_low))#get the user_id of common raters
    user_low=unique_recipe.filter(user_id__in=user_low)[:5]#get 5 recipes of common raters
    listing_low= user_low.values('recipe')




    intersection= similarity.union(similarity_low)
    users=set(map(lambda x:x.user_id,intersection))#get the user_id of common raters
    useras=unique_recipe.filter(user_id__in=users)
    best= useras.values_list('recipe',flat=True)
    recipea_best=[]
    for besty in best:
        id= str(besty)
        recipea_best.append(Recipes.info(id))
        print(recipea_best)




    return render(request, 'blog/user_recommendation_list.html', {'username': request.user.username, 'recipe_list': recipe_list, 'uniquea':uniquea, 'recipea_best':recipea_best})

class PostListView(ListView):
    model = Post
    template_name = 'blog/post.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# Create your views here.
