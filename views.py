from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Restaurant, MenuItem
from .serializers import MenuItemSerializer, RestaurantsSerializer
from .forms import NameOfNewRestaurant, NewMenuItem
from django.contrib import messages
from rest_framework.parsers import JSONParser



class Index(View):
    def get(self, request):
        self.restaurants = Restaurant.objects.all()
        self.context = {
            'restaurants': (self.restaurants),
        }
        return render(request, 'restaurant/index.html', self.context)


class RestaurantsJSON(View):
    def get(self, request):
        self.restaurants = Restaurant.objects.all()
        self.serializer = RestaurantsSerializer(self.restaurants, many=True)
        return JsonResponse(self.serializer.data, safe=False)


class CreateRestaurant(View):
    def get(self, request):
        form = NameOfNewRestaurant(request.POST)
        form.fields['name'].widget.attrs['placeholder'] = 'New Restaurant\'s name'
        self.context = {
            'NameOfNewRestaurant': form,
        }
        NameOfNewRestaurant()
        return render(request, 'restaurant/create.html', self.context)
    def post(self, request):
        NameOfNewRestaurant(request.POST)
        if 'name' in request.POST:
            restaurant_db = Restaurant(name=request.POST['name'])
            restaurant_db.save()
            messages.info(request, f"New restaurant - {request.POST['name']} - was created!")
            return HttpResponseRedirect(reverse('restaurant:index'))


class DeleteRestaurant(View):
    def get(self, request, restaurant_name):
        self.context = {
            'restaurant_name': Restaurant.objects.get(name=restaurant_name)
        }
        return render(request, 'restaurant/delete_restaurant.html', self.context)

    def post(self, request, restaurant_name):
        restaurant_db = Restaurant.objects.get(name=restaurant_name)
        restaurant_db.delete()
        messages.info(request, f"Restaurant - {restaurant_name} - was deleted!")
        return HttpResponseRedirect(reverse('restaurant:index'))


class EditRestaurant(View):
    def get(self, request, restaurant_name):
        form = NameOfNewRestaurant(request.POST)
        form.fields['name'].widget.attrs['placeholder'] = Restaurant.objects.get(name=restaurant_name)
        self.context = {
            'restaurant_name': Restaurant.objects.get(name=restaurant_name),
            'NameOfNewRestaurant': form,
        }
        return render(request, 'restaurant/edit_restaurant.html', self.context)

    def post(self, request, restaurant_name):
        # NameOfNewRestaurant(request.POST)
        restaurant_db = Restaurant.objects.get(name=restaurant_name)
        restaurant_db.name = request.POST['name']
        restaurant_db.save()
        messages.info(request, f"Changed name of {restaurant_name} to {request.POST['name']}")
        return HttpResponseRedirect(reverse('restaurant:index'))


class MenuItems(View):
    def get(self, request, restaurant_name):
        self.restaurant = Restaurant.objects.get(name=restaurant_name)
        self.menu = self.restaurant.menuitem_set.values()
        self.context = {
            'restaurant_name': (self.restaurant),
            'menu': self.menu if len(self.menu) > 0 else False,
        }
        return render(request, 'restaurant/menu.html', self.context)


class MenuItemsJSON(View):
    def get(self, request, restaurant_name):
        self.restaurant = Restaurant.objects.get(name=restaurant_name)
        self.menu_items = self.restaurant.menuitem_set.all()
        self.serializer = MenuItemSerializer(self.menu_items, many=True)
        return JsonResponse(self.serializer.data, safe=False)


class OneMenuItemJSON(View):
    def get(self, request, restaurant_name, menu_item_id):
        self.restaurant = Restaurant.objects.get(name=restaurant_name)
        self.menu_item = self.restaurant.menuitem_set.filter(id=menu_item_id)
        self.serializer = MenuItemSerializer(self.menu_item, many=True)
        return JsonResponse(self.serializer.data, safe=False)


class CreateMenuItem(View):
    def get(self, request, restaurant_name):
        form = NewMenuItem()
        form.fields['name'].widget.attrs['placeholder'] = 'New  Menu Item\'s name'
        self.context = {
            'restaurant_name': restaurant_name,
            'NewMenuItem': form,
        }
        return render(request, 'restaurant/create_menu_item.html', self.context)

    def post(self, request, restaurant_name):
        restaurant = Restaurant.objects.get(name=restaurant_name)
        if 'name' in request.POST:
            menu_item = MenuItem(name=request.POST['name'], restaurant=restaurant,
                                 description=request.POST['description'],
                                 price=f"${request.POST['price']}", course=request.POST['course'])
            menu_item.save()
            messages.info(request, f"New Menu Item - {request.POST['name']} - was created!")
            return HttpResponseRedirect(reverse('restaurant:menu', args=(restaurant_name,)))


class EditMenuItem(View):
    def get(self, request, restaurant_name, menu_item_id):
        form = NewMenuItem()
        restaurant = Restaurant.objects.get(name=restaurant_name)
        menu_item = restaurant.menuitem_set.filter(id__startswith=menu_item_id).values()
        form.fields['name'].widget.attrs['placeholder'] = menu_item[0]['name']
        form.fields['price'].widget.attrs['placeholder'] = menu_item[0]['price']
        form.fields['description'].widget.attrs['placeholder'] = menu_item[0]['description']
        self.context = {
            'menu_item_name': menu_item[0]['name'],
            'NewMenuItem': form,
            'menu_item_id': menu_item_id,
            'restaurant_name': restaurant_name,
        }
        return render(request, 'restaurant/edit_menu_item.html', self.context)

    def post(self, request, restaurant_name, menu_item_id):
        restaurant = Restaurant.objects.get(name=restaurant_name)
        menu_item = MenuItem.objects.get(restaurant=restaurant, id=menu_item_id)
        menu_item_name = menu_item.name
        menu_item.name = request.POST['name']
        menu_item.price = request.POST['price']
        menu_item.description = request.POST['description']
        menu_item.course = request.POST['course']
        menu_item.save()
        messages.info(request, f"Changed name of {menu_item_name} to {request.POST['name']}")
        return HttpResponseRedirect(reverse('restaurant:menu', args=(restaurant_name,)))


class DeleteMenuItem(View):
    def get(self, request, restaurant_name, menu_item_id):
        restaurant = Restaurant.objects.get(name=restaurant_name)
        menu_item = restaurant.menuitem_set.filter(id__startswith=menu_item_id).values()
        self.context = {
            'menu_item_name': menu_item[0]['name'],
            'menu_item_id': menu_item_id,
            'restaurant_name': restaurant_name,
        }
        return render(request, 'restaurant/delete_menu_item.html', self.context)

    def post(self, request, restaurant_name, menu_item_id):
        restaurant = Restaurant.objects.get(name=restaurant_name)
        menu_item = MenuItem.objects.get(restaurant=restaurant, id=menu_item_id)
        menu_item_message = menu_item.name
        menu_item.delete()
        messages.info(request, f"Deleted {menu_item_message} from {restaurant_name}")
        return HttpResponseRedirect(reverse('restaurant:menu', args=(restaurant_name,)))


class LoginView(View):
    def get(self, request):
        return render(request, 'restaurant/login.html')
