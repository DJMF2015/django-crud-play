from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from .models import Recipe
from .forms import SignupForm, LoginForm
import logging

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')


@csrf_protect
def recipes(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        recipe_name = request.POST.get('recipe_name')
        recipe_ingredients = request.POST.get('recipe_ingredients')
        recipe_description = request.POST.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')
        if recipe_name and recipe_description and recipe_image and recipe_ingredients:
            try:
                Recipe.objects.create(
                    user=request.user,
                    recipe_name=recipe_name,
                    recipe_description=recipe_description,
                    recipe_image=recipe_image,
                    recipe_ingredients=recipe_ingredients
                )
                return redirect(reverse('recipes'))
            except Exception as e:
                logger.error("Error saving recipe: %s", e)
                context = {
                    'error': 'An error occurred while saving the recipe.',
                    'recipes': Recipe.objects.filter(user=request.user)
                }
                return render(request, 'recipe.html', context)
        else:
            context = {
                'error': 'All fields are required.',
                'recipes': Recipe.objects.filter(user=request.user)
            }
            return render(request, 'recipe.html', context)

    queryset = Recipe.objects.filter(user=request.user)

    if request.GET.get('search'):
        queryset = queryset.filter(
            recipe_name__icontains=request.GET.get('search'))

    context = {'recipes': queryset}
    return render(request, 'recipe.html', context)


def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    recipe.delete()
    return redirect(reverse('recipes'))


def update_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    if request.method == 'POST':
        recipe_name = request.POST.get('recipe_name')
        recipe_description = request.POST.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')
        recipe_ingredients = request.POST.get('recipe_ingredients')
        if recipe_name and recipe_description and recipe_ingredients:
            try:
                recipe.recipe_name = recipe_name
                recipe.recipe_description = recipe_description
                recipe.recipe_ingredients = recipe_ingredients
                if recipe_image:
                    recipe.recipe_image = recipe_image
                recipe.save()
                return redirect(reverse('recipes'))
            except Exception as e:
                logger.error("Error updating recipe: %s", e)
                context = {
                    'error': 'An error occurred while updating the recipe.',
                    'recipe': recipe
                }
                return render(request, 'update/update_recipe.html', context)
        else:
            context = {
                'error': 'All fields except image are required.',
                'recipe': recipe
            }
            return render(request, 'update/update_recipe.html', context)

    context = {'recipe': recipe}
    return render(request, 'update/update_recipe.html', context)


def main(request):
    return render(request, 'main.html')


def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('main')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')
