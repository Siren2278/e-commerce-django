# E-commerce Inventory Management System

## Overview
This project is an **E-commerce Inventory Management System** built with **Django**, **MySQL**, **HTML**, **CSS**, **Bootstrap**, and **JavaScript**. It provides an intuitive platform for managing products, orders, customers, and other essential e-commerce functionalities, including user authentication, order processing, and CRUD operations for products. Admin users can manage products, view order details, and generate analytics reports.

## Features

### Customer Features:
- **User Authentication**: Login, registration, password reset functionality.
- **Product Browsing**: View products by category or all products.
- **Cart Management**: Add items to the shopping cart, modify quantities, and checkout.
- **Order Management**: View and track order history.

### Admin Features:
- **Product Management**: Add, update, or delete products through the Django admin panel.
- **Order Management**: View, process, and manage orders.
- **Reports**: Generate reports for sales and product statistics.

## Technologies Used
- **Backend**: Django (Python)
- **Database**: MySQL
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Authentication**: Django authentication system (Custom user model)
- **API**: Django REST Framework for potential future API extensions

## Project Structure

├── ecommerce/ │ ├── manage.py │ ├── store/ (App for product, order, and customer management) │ └── templates/ (HTML templates) │ └── static/ (CSS, JS, images, etc.) ├── requirements.txt ├── .env (for environment variables such as DB credentials) └──
