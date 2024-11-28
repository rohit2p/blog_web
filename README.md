Blog Website

A simple and user-friendly blog website for sharing articles, thoughts, and ideas. This project is built using Django and includes a clean, responsive interface to enhance the user experience.
Features

    User Authentication: Sign up, log in, and manage your profile.
    Create, Edit, and Delete Posts: Fully functional blog post management.
    Responsive Design: Optimized for desktop, tablet, and mobile views.
    Comments: Users can leave comments on blog posts.
    Categories and Tags: Organize posts for easy navigation.

Technology Stack

    Backend: Django
    Frontend: HTML, CSS (Bootstrap), JavaScript
    Database: SQLite
    Deployment: [Railway, AWS]

Installation (For Local Development)

    Clone the repository:

git clone <repository-url>
cd <project-directory>

Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Apply migrations:

python manage.py makemigrations
python manage.py migrate

Run the development server:

    python manage.py runserver

    Visit the site at http://127.0.0.1:8000/.

Usage

    To create a new blog post, log in and navigate to the "New Post" page.
    Manage your posts under your profile.
    Explore blogs by category, tag, or search.

Deployment

The website is deployed at: https://rhyem.up.railway.app/
Contribution

Contributions are welcome! To contribute:

    Fork the repository.
    Create a new branch:

git checkout -b feature-branch

Commit your changes:

git commit -m "Add new feature"

Push to the branch:

    git push origin feature-branch

    Submit a pull request.