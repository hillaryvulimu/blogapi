# Blog API

## Description

Blog API V 1.0.0 is a blogging platform built using Django and Django REST Framework. The API allows users to register their own accounts and create, edit, or delete their own blog posts. Anyone, even those who aren't registered, can view any blog post. However, only registered users can post, edit, or delete their own posts. Admin users have full control and can modify any content, including user accounts and blog posts.

## Installation

To install and set up the Blog API, follow these steps:

1. **Clone the repository:**
   ```sh
   git clone https://github.com/hillaryvulimu/blogapi.git
   cd blogapi
   ```

2. **Create a virtual environment and activate it:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create a `.env` file in the root directory of the project with the following variables:
     ```env
     DEBUG=True  # Set to False in production
     SECRET_KEY=your_secret_key
     DATABASE_URL=sqlite:///db.sqlite3  # Or your database URL
     ```

5. **Configure settings:**
   - In `settings.py`, set the following:
     ```python
     ALLOWED_HOSTS = ['your_domain_or_IP']
     CORS_ALLOWED_ORIGINS = ['http://your_frontend_domain']
     CSRF_TRUSTED_ORIGINS = ['http://your_frontend_domain']
     ```

6. **Set up email preferences:**
   - Configure email settings in `settings.py` for sending signup or password reset confirmation emails.

7. **Create a blank database:**
   - If you prefer to use a SQLite database, run:
     ```sh
     python create_blank_db.py
     ```
   - This will create a new db.sqlite3 file that you can use in development. However, in production, it is recommended that you use PostgreSQL, MySQL or another database instead of SQLite. 

8. **Run migrations:**
   ```sh
   python manage.py migrate
   ```

9. **Run tests:**
   ```sh
   python manage.py test
   ```

## Usage

- Start the Django development server:
  ```sh
  python manage.py runserver
  ```

- The API can be used with a frontend application or another Django app/project.

## Authentication

- This project uses Session authentication for the Django Rest Framework's browsable API and Token authentication for API interactions, such as with a frontend blog app.
- To manage users (registration, login, password change, etc.), you can use:
  - `rest_framework` URLs (at `api-auth/`), which provide basic authentication, as well as signup and password reset features
  - `dj_rest_auth` URLs (at `api/v1/dj-rest-auth/`), which provide additional features, including Token authentication, social authentication, password management, etc. 
- See the project's `urls.py` file or Redoc/SwaggerUI schemas for more details and relevant endpoints.

## API Documentation Endpoints

- **Redoc schema:** [api/schema/redoc/]
- **SwaggerUI schema:** [api/schema/swagger-ui/]

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
