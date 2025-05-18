1.     .venv\Scripts\activate
2. **Install the missing module**:
   - Install `django-extensions` using pip:
     pip install django-extensions

3. **Add `django_extensions` to `INSTALLED_APPS`**:
   - Open your `settings.py` file and add `'django_extensions'` to the `INSTALLED_APPS` list:
     
python
     INSTALLED_APPS = [
         # other apps
         'django_extensions',
     ]

4. **Run the server again**:
   - Start the server with:
     python manage.py runserver

If the issue persists, ensure your virtual environment is correctly set up and activated.
