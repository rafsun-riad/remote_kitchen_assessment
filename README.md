1. Create a virtual enviroment
2. Activate virtual enviroment
3. Install neccessary dependencies using "pip install -r requirments.txt"
4. Run project
5. Superuser:
        username: rafsun
        password: 1234

=============================================================================
Base URL : http://127.0.0.1:8000/
=============================================================================

For User Login (POST): account/login/ [need username,password]

For User Register (POST) : account/register/ [need username, email, password]

For User Logout (POST) : account/logout/

=============================================================================

For all Restaurants (GET): api/restaurants/ 

For adding Restaurants (POST): api/restaurants/add/ [need restaurant name, location]

For editing Restaurant (PUT): api/restaurants/edit/<str:id>/ [need restaurant name or location or both]

For deleting Restaurant (DELETE): api/restaurants/delete/<str:id>/ [need restaurant id]

For getting Employees of a Restaurant (GET): api/restaurants/<str:id>/employee/ [need restaurant id]

For adding Employee of a Restaurant (POST): api/restaurants/<str:id>/employee/add/ [need restaurant id and employee username]

For deleteing Employee of a Restaurant (DELETE): api/restaurants/employee/delete/<str:id>/ [need employee id]

For getting Categories of a Restaurant (GET): api/restaurants/<str:id>/categories/ [need restaurant id]

For adding Category of a Restaurant (POST): api/restaurants/<str:id>/categories/add/ [need restaurant id, caregory name]

For editing Category of a Restaurant (PUT): api/restaurants/categories/edit/<str:id>/ [need category id, name]

For deleting Category of a Restaurant (DELETE): api/restaurants/categories/delete/<str:id>/ [need category id]

For getting Menus of a Category(GET): api/restaurants/categories/<str:id>/menus/ [need category id]

For adding Menu of a Category (POST): api/restaurants/categories/<str:id>/menus/add/ [need category id, menu name]

For editing Menu of a Category (PUT): api/restaurants/categories/menus/edit/<str:id>/ [need menu id, name]

For deleting Menu of a Category (DELETE) : api/restaurants/categories/menus/delete/<str:id>/ [need menu id]

For getting Fooditems of a Menu (GET): api/restaurants/caregories/menus/<str:id>/fooditems/ [need menu id]

For getting a Fooditem by ID(GET): api/restaurants/fooditem/<str:id>/ [need fooditem id]

For adding Fooditem of a Menu (POST): api/restaurants/categories/menus/<str:id>/fooditem/add/ [need menu id, fooditem name, price, description]

For editing Fooditem of a Menu (PUT): api/restaurants/categories/menus/fooditem/edit/<str:id>/ [need food item id, name or price or description or all]

For deleting Fooditem of a Menu (DELETE): api/restaurants/categories/menus/fooditem/delete/<str:id>/ [need food item id]

For getting modifier of a fooditem (GET): api/restaurants/fooditems/<str:id>/modifiers/ [need fooditem id]

For adding modifier of a fooditem (POST): api/restaurants/fooditems/<str:id>/modifiers/add/ [need fooditem id, name, extraPrice]

For editing modifier of a fooditem (PUT): api/restaurants/fooditems/modifiers/edit/<str:id>/ [need modifier id]

For deleting modifier of a fooditem (DELETE): api/restaurants/fooditems/modifiers/delete/<str:id>/ [delete modifier id]

=======================================================================================================

For getting all order of a user (GET): api/orders/myorders/

For getting all order of a Restaurant (GET): api/orders/restaurants/<str:id>/ [need restaurant id]

For getting order by id (GET): api/orders/<str:id>/ [need order id]

For adding order (POST): api/orders/add/ [need restaurant, totalPrice, deliveryAddress, orderItems]

For making payment (POST): api/orders/make-payment/ [need card info, amount, currency]

For updating order after success payment (PUT): api/orders/<str:id>/success-payment/ [need order id, paymentMethod]

For deleting a order (DELETE): api/orders/delete/<str:id>/ [need order id]
