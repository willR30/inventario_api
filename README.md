# Inventary API

This API provides a comprehensive system for inventory, client, supplier, and sales management for businesses. It enables users to create accounts, manage their businesses, categorize products, generate reports, and access detailed documentation.

## Technologies Used

- **Django:** High-level web framework for rapid development.
- **dj-database-url:** Allows the use of URLs for database configuration.
- **django-admin-rangefilter:** Adds range-based filtering in the Django admin.
- **django-cors-headers:** Manages CORS headers in Django applications.
- **djangorestframework:** Powerful and flexible toolkit for building APIs.
- **drf-writable-nested:** Extension for Django REST Framework enabling nested writes.
- **coreapi:** Tool for documenting web APIs.
  
## Installation and Execution

To run this project locally, follow these steps:

1. Clone this repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the service using `python3 manage.py runserver`.

   
## Authentication and Usage

- **Authentication:** Token-based authentication is implemented.
- **Token Usage:** Endpoints require the token in the header except for user registration and generic entities.
  
## Documentation

The project's documentation is located at `/docs/`, organized by entities.
![image](https://github.com/willR30/inventario_api/assets/50780601/13402334-9d23-4a8e-b003-a6e8cd37de5a)

## Contribution

If you wish to contribute to this project, follow these steps:

1. Fork this repository.
2. Create a branch for your new feature (`git checkout -b feature/new-feature`).
3. Make your changes and commit (`git commit -m 'Add new feature'`).
4. Push the branch (`git push origin feature/new-feature`).
5. Create a pull request detailing your changes.


