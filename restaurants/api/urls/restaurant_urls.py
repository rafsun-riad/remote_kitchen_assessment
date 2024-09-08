from django.urls import path
from restaurants.api.views import restaurant_views as views

urlpatterns = [
    path('', views.get_all_restuarants, name='all-restaurants'),

    path('add/', views.add_restaurants, name='add-restaurant'),

    path('edit/<str:id>/', views.edit_restaurant, name='edit-restaurant'),

    path('delete/<str:id>/', views.delete_restaurant, name='delete-restaurant'),

    path('<str:id>/employee/', views.get_all_empolyee_of_restaurant,
         name='restaurant-employee'),

    path('<str:id>/employee/add/', views.add_empolyee, name='add-employee'),

    path('employee/delete/<str:id>/',
         views.delete_employee, name='delete-employee'),

    path('<str:id>/categories/', views.get_categories_of_restaurant,
         name='restaurants-categories'),

    path('<str:id>/categories/add/', views.add_category, name='add-category'),

    path('categories/edit/<str:id>/', views.edit_category, name='edit-category'),

    path('categories/delete/<str:id>/',
         views.delete_category, name='delete-category'),

    path('categories/<str:id>/menus/',
         views.get_menus_of_category, name='categories-menu'),

    path('categories/<str:id>/menus/add/', views.add_menu, name='add-menu'),

    path('categories/menus/edit/<str:id>/', views.edit_menu, name='edit-menu'),

    path('categories/menus/delete/<str:id>/',
         views.delete_menu, name='delete-menu'),

    path('caregories/menus/<str:id>/fooditems/',
         views.get_fooditems_of_menu, name='menus-fooditem'),

    path('fooditem/<str:id>/', views.get_fooditem_by_id, name='fooditem_by_id'),

    path('categories/menus/<str:id>/fooditem/add/',
         views.add_fooditem, name='add-fooditem'),

    path('categories/menus/fooditem/edit/<str:id>/',
         views.edit_fooditem, name='edit-fooditem'),

    path('categories/menus/fooditem/delete/<str:id>/',
         views.delete_fooditem, name='delete-fooditem'),

    path('fooditems/<str:id>/modifiers/',
         views.get_modifier_of_fooditem, name='fooditem-modifier'),

    path('fooditems/<str:id>/modifiers/add/',
         views.add_modifiers, name='add-modifier'),

    path('fooditems/modifiers/edit/<str:id>/',
         views.edit_modifier, name='edit-modifier'),

    path('fooditems/modifiers/delete/<str:id>/',
         views.delete_modifier, name='delete-modifier'),


]
