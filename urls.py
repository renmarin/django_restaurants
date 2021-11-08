from django.urls import path
from .views import Index, CreateRestaurant, DeleteRestaurant, MenuItems,\
    EditRestaurant, EditMenuItem, DeleteMenuItem, CreateMenuItem, MenuItemsJSON,\
    OneMenuItemJSON, RestaurantsJSON, LoginView

from . import views

app_name = 'restaurant'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('create_restaurant', CreateRestaurant.as_view(), name='create_restaurant'),
    path('<str:restaurant_name>/delete', DeleteRestaurant.as_view(), name='delete_restaurant'),
    path('<str:restaurant_name>/menu', MenuItems.as_view(), name='menu'),
    path('<str:restaurant_name>/edit', EditRestaurant.as_view(), name='edit_restaurant'),
    path('<str:restaurant_name>/create_menu_item', CreateMenuItem.as_view(), name='create_menu_item'),
    path('<str:restaurant_name>/<str:menu_item_id>/edit>', EditMenuItem.as_view(), name='edit_menu_item'),
    path('<str:restaurant_name>/<str:menu_item_id>/delete>', DeleteMenuItem.as_view(), name='delete_menu_item'),
    path('<str:restaurant_name>/menu/JSON', MenuItemsJSON.as_view(), name='menu_json'),
    path('<str:restaurant_name>/menu/<str:menu_item_id>/JSON', OneMenuItemJSON.as_view(), name='menu_item_json'),
    path('JSON', RestaurantsJSON.as_view(), name='restaurants_json'),
    path('login', LoginView.as_view(), name='login'),
]
