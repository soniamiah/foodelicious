from django import forms
from .models import Rating
from django.conf import settings
import requests
import pprint
import urllib.parse
import urllib

#recipe class for making API calls to retrieve recipes
class Recipes(forms.Form):
    food= forms.CharField(max_length=100) #input field
    def search(self): #search recipe by providing item name
        result={}

        endpoint ="https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes"
        headers = { "X-RapidAPI-Key": "6CadSMGC2nmshXLy2NkTwI8tt3rTp1FvyUrjsnI5q3M9aLzlWy"}

        food= self.cleaned_data['food'] #clean input
        url = endpoint.format(source_lang='en') + "/search?number=20&offset=0&" + urllib.parse.urlencode({'query': food})
        #make API request
        json_data = requests.get(url,headers= headers).json()
        formatted_recipes= json_data['results']
        #return API response
        return formatted_recipes


    def info(id):

        endpoint ="https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
        headers = { "X-RapidAPI-Key": "6CadSMGC2nmshXLy2NkTwI8tt3rTp1FvyUrjsnI5q3M9aLzlWy"}

        inforeq= endpoint.format(source_lang='en') + "recipes/" + id + "/information"
        json_info= requests.get(inforeq,headers= headers).json()

        return json_info

    def joke():

        endpoint ="https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"
        headers = { "X-RapidAPI-Key": "6CadSMGC2nmshXLy2NkTwI8tt3rTp1FvyUrjsnI5q3M9aLzlWy"}
        joke= endpoint.format(source_lang='en') + "food/jokes/random"
        json_joke= requests.get(joke,headers= headers).json()

        return json_joke


    def random():
        endpoint ="https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes"
        headers = { "X-RapidAPI-Key": "6CadSMGC2nmshXLy2NkTwI8tt3rTp1FvyUrjsnI5q3M9aLzlWy"}
        random= endpoint.format(source_lang='en') + "/random?number=2"
        json_random= requests.get(random,headers= headers).json()
        formatted_random= json_random['recipes']
        return formatted_random



class findByIngredients(forms.Form):

    ingredients= forms.CharField(max_length=100)

    def ingred(self):
        result={}

        endpoint ="https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/"
        headers = { "X-RapidAPI-Key": "6CadSMGC2nmshXLy2NkTwI8tt3rTp1FvyUrjsnI5q3M9aLzlWy"}

        ingredients= self.cleaned_data['ingredients']
        url = endpoint.format(source_lang='en') + "findByIngredients?number=5&ranking=1&" + urllib.parse.urlencode({'ingredients': ingredients})
        json_ing = requests.get(url,headers= headers).json()

        return json_ing
