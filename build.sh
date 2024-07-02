#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser --no-input --username admin --email admin@example.com || true

# Set admin password from environment variable
python -c "
import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

User = get_user_model()
user = User.objects.filter(username='admin').first()
admin_password = os.getenv('ADMIN_PASSWORD')

if user and admin_password:
    user.set_password(admin_password)
    user.save()
"
