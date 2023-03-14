# Estyle
This is django based ecommerce application.

### Implementation
We used Django for our project which follows MVT (Model View Template) software design pattern. The view is used to execute the basic logic and interact with a model to carry data and renders a template. In our projects, we created three major models namely Item, OrderItem and Order. We used both class-based and function-based views; the class-based views namely HomeView, ItemDetailView, OrderSummaryView and CheckoutView and the function-based views namely add_to_cart, remove_from_cart and remove_single_item_from_cart. We used many html pages for different segments of our web application. Some of them are base.html, home.html, navbar.html, footer.html, signup.html, login.html, logout.html ,product,html, order_summary.html and checkout.html. 

### Working
The user chooses the product he wants to buy, and he can see the detail of the product. He can then add the product to cart if he is logged in. Otherwise he will be redirected to the login or signup page. The user can also change the quantity of the product in the shopping cart and can also remove a product from the cart. Then he can proceed to checkout and place an order. 

### Tools Used
We used Python 3.7.4 and its framework Django for the backend and Bootstrap ( html, css, js ) for the frontend of our web application. The database used is sqlite3 which is supported by Django. We used Atom Code Editor for creating our application.

### Libraries Used
We used Allauth which is used for user authentication. It is the integrated set of Django application addressing authentication, registration, account management. We also used some Django packages like Pillow for images, crispy_forms and phonenumber_field for forms.

### Scrennshots

Home Page

![Home Page](https://github.com/Fatima-Mujahid/estyle/blob/main/Resources/1.png)
![Home Page](https://github.com/Fatima-Mujahid/estyle/blob/main/Resources/2.png)

User Login

![User Login](https://github.com/Fatima-Mujahid/estyle/blob/main/Resources/3.png)

Product Page

![Product Page](https://github.com/Fatima-Mujahid/estyle/blob/main/Resources/4.png)

Order Summary

![Order Summary](https://github.com/Fatima-Mujahid/estyle/blob/main/Resources/5.png)

Checkout

![Checkout](https://github.com/Fatima-Mujahid/estyle/blob/main/Resources/6.png)

Admin Page

![Admin Page](https://github.com/Fatima-Mujahid/estyle/blob/main/Resources/7.png)

Error Handling

![Error Handling](https://github.com/Fatima-Mujahid/estyle/blob/main/Resources/8.png)
# motiplug
