# Blog API

## Description

Blog API V 1.0.0 is a blogging platform built using Django and Django REST Framework. The API allows users to register their own accounts and create, edit, or delete their own blog posts. Anyone, even those who aren't registered, can view any blog post. However, only registered users can post, edit, or delete their own posts, as well as react to different posts. Admin users have full control and can modify any content, including user accounts and blog posts.

## Installation

To install and set up the Blog API, follow these steps:

1. **Clone the repository:**
   git clone https://github.com/hillaryvulimu/blogapi.git
   cd blogapi

2. **Create a virtual environment and activate it:**
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the required packages:**
   pip install -r requirements.txt

4. **Set up environment variables:**
   - Create a `.env` file in the root directory of the project with the following variables:
     DEBUG=True  # Set to False in production
     SECRET_KEY=your_secret_key
     DATABASE_URL=sqlite:///db.sqlite3  # Or your database URL
     ALLOWED_HOSTS=your_domain_or_IP
     CORS_ALLOWED_ORIGINS=http://your_frontend_domain
     CSRF_TRUSTED_ORIGINS=http://your_frontend_domain

   - Note: In production (e.g., on Render), you might need to provide the environment variables in the platform's Environment Variables page. On Render, this is found under `Environment`.

5. **Set up email preferences:**
   - Configure email settings in `settings.py` for sending signup or password reset confirmation emails. You can also add any sensitive email configurations inside the .env file or on your deployment platform's Environment Variables page.

6. **Create a blank database:**
   - If you prefer to use a SQLite database (e.g. in development), run:

     python create_blank_db.py
     ```
   - This will create a new db.sqlite3 file that you can use in development. However, in production, it is recommended that you use PostgreSQL, MySQL, or another database instead of SQLite. 

7. **Run migrations:**
   python manage.py migrate

8. **Run tests:**
   python manage.py test

## Usage

- Start the Django development server:
  python manage.py runserver

- The blog only serves API data using JSON and does not have templates for rendering. You can use a separate front-end found at [blog_frontend](https://github.com/hillaryvulimu/blog_frontend). For more on the front-end, check its `README.md` file. You can also build your own front-end to take advantage of the various endpoints of the API.

## Authentication

- This project uses Session authentication for the Django Rest Framework's browsable API and Token authentication for API interactions, such as with a frontend blog app.
- To manage users (registration, login, password change, etc.), you can use:
  - `rest_framework` URLs (at `api-auth/`), which provide basic authentication, as well as signup and password reset features
  - `dj_rest_auth` URLs (at `api/v1/dj-rest-auth/`), which provide additional features, including Token authentication, social authentication, password management, etc. 
- See the project's `urls.py` file or Redoc/SwaggerUI schemas for more details and relevant endpoints.

## API Documentation Endpoints

- **Redoc schema:** [api/schema/redoc/]
- **SwaggerUI schema:** [api/schema/swagger-ui/]

## Additional Information

- Currently, the front-end found at [blog_frontend](https://github.com/hillaryvulimu/blog_frontend) does not have the option for users to create and manage their own posts due to database limitations in the current deployment tier. However, the backend is very ready to accept such input from different users, and it's just a matter of adding the functionality to the front-end.
- Social login/registration features are not implemented but will be added in the future. However, you can add them on your own using dj-allauth and dj-rest-auth.
- You can change/update game categories in the `Category` subclass of the `Post` model class.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For more information, feel free to reach out via email at hillaryvulimu@gmail.com.