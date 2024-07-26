from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from recipe import views
from recipe.views import recipes, delete_recipe, update_recipe, main, user_login, user_signup, user_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='main'),
    path('recipes/', recipes, name='recipes'),
    path('delete_recipe/<int:recipe_id>/', delete_recipe, name='delete_recipe'),
    path('update_recipe/<int:recipe_id>/', update_recipe, name='update_recipe'),
    path('login/', user_login, name='login'),
    path('signup/', user_signup, name='signup'),
    path('logout/', user_logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
