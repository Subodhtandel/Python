"""
Django Project Structure Explorer
This program creates a Django project and explains its directory structure.
"""

import os
import json
from pathlib import Path


class DjangoProjectExplorer:
    """
    A class to explore and understand Django project structure.
    """
    
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.structure = {}
    
    def explore_structure(self):
        """
        Recursively explore the Django project structure and document each file.
        """
        print("=" * 80)
        print("DJANGO PROJECT STRUCTURE ANALYSIS")
        print("=" * 80)
        print(f"\nProject Root: {self.project_path}\n")
        
        # Dictionary to store descriptions of Django components
        django_components = {
            'manage.py': {
                'type': 'Script',
                'purpose': 'Command-line utility for administrative tasks',
                'location': 'Project root',
                'usage': [
                    'python manage.py runserver',
                    'python manage.py migrate',
                    'python manage.py createsuperuser',
                    'python manage.py makemigrations',
                    'python manage.py startapp'
                ]
            },
            'db.sqlite3': {
                'type': 'Database',
                'purpose': 'SQLite database file (default database)',
                'location': 'Project root',
                'note': 'Created after running migrations'
            },
            '<project_name>/': {
                'type': 'Project Package',
                'purpose': 'Main project package containing configuration files',
                'location': 'Inside project root',
                'contains': [
                    '__init__.py',
                    'asgi.py',
                    'wsgi.py',
                    'settings.py',
                    'urls.py'
                ]
            },
            '__init__.py': {
                'type': 'Python Package Marker',
                'purpose': 'Makes a directory a Python package',
                'location': 'In project and app directories',
                'content': 'Usually empty'
            },
            'settings.py': {
                'type': 'Configuration',
                'purpose': 'Project settings and configuration',
                'location': 'Inside <project_name>/',
                'contains': [
                    'INSTALLED_APPS',
                    'DATABASES',
                    'MIDDLEWARE',
                    'TEMPLATES',
                    'STATIC_URL',
                    'SECRET_KEY'
                ]
            },
            'urls.py': {
                'type': 'URL Configuration',
                'purpose': 'Main URL routing configuration',
                'location': 'Inside <project_name>/',
                'note': 'Maps URLs to views'
            },
            'wsgi.py': {
                'type': 'Application Gateway',
                'purpose': 'WSGI config for production deployment',
                'location': 'Inside <project_name>/',
                'use_case': 'Web Server Gateway Interface'
            },
            'asgi.py': {
                'type': 'Application Gateway',
                'purpose': 'ASGI config for async support',
                'location': 'Inside <project_name>/',
                'use_case': 'Asynchronous Server Gateway Interface'
            },
            '<app_name>/': {
                'type': 'Django App',
                'purpose': 'Self-contained module with specific functionality',
                'location': 'Inside project root',
                'contains': [
                    'migrations/',
                    '__init__.py',
                    'admin.py',
                    'apps.py',
                    'models.py',
                    'tests.py',
                    'views.py'
                ]
            },
            'models.py': {
                'type': 'Data Models',
                'purpose': 'Define database models',
                'location': 'Inside <app_name>/',
                'example': 'class Post(models.Model): ...'
            },
            'views.py': {
                'type': 'Views',
                'purpose': 'Handle request logic and return responses',
                'location': 'Inside <app_name>/',
                'types': ['Function-based views', 'Class-based views']
            },
            'urls.py': {
                'type': 'URL Routing',
                'purpose': 'App-specific URL patterns',
                'location': 'Inside <app_name>/ (optional)',
                'note': 'Included in project urls.py using include()'
            },
            'admin.py': {
                'type': 'Admin Interface',
                'purpose': 'Register models with Django admin',
                'location': 'Inside <app_name>/',
                'example': 'admin.site.register(Post)'
            },
            'apps.py': {
                'type': 'App Configuration',
                'purpose': 'App-specific configuration',
                'location': 'Inside <app_name>/',
                'contains': 'AppConfig class'
            },
            'tests.py': {
                'type': 'Unit Tests',
                'purpose': 'Test cases for the app',
                'location': 'Inside <app_name>/',
                'note': 'Use TestCase class from django.test'
            },
            'migrations/': {
                'type': 'Database Migrations',
                'purpose': 'Database schema changes history',
                'location': 'Inside <app_name>/',
                'note': 'Auto-generated using makemigrations'
            }
        }
        
        return django_components
    
    def print_directory_tree(self, path=None, prefix="", is_last=True):
        """
        Print directory tree structure in a visual format.
        """
        if path is None:
            path = self.project_path
        
        if not path.exists():
            return
        
        # Skip __pycache__ and .pyc files
        if path.name == '__pycache__' or path.name.endswith('.pyc'):
            return
        
        if path.is_dir():
            print(f"{prefix}{'└── ' if is_last else '├── '}{path.name}/")
            contents = sorted([p for p in path.iterdir() 
                             if p.name != '__pycache__' and not p.name.endswith('.pyc')])
            
            for i, item in enumerate(contents):
                is_last_item = (i == len(contents) - 1)
                extension = "    " if is_last else "│   "
                self.print_directory_tree(item, prefix + extension, is_last_item)
        else:
            print(f"{prefix}{'└── ' if is_last else '├── '}{path.name}")
    
    def display_project_info(self):
        """
        Display complete Django project information.
        """
        components = self.explore_structure()
        
        print("\n" + "=" * 80)
        print("PROJECT DIRECTORY TREE")
        print("=" * 80 + "\n")
        
        self.print_directory_tree()
        
        print("\n" + "=" * 80)
        print("DJANGO PROJECT COMPONENTS EXPLANATION")
        print("=" * 80 + "\n")
        
        for component, details in components.items():
            print(f"\n{'─' * 80}")
            print(f"📁 {component}")
            print(f"{'─' * 80}")
            
            for key, value in details.items():
                if isinstance(value, list):
                    print(f"  {key}:")
                    for item in value:
                        print(f"    • {item}")
                else:
                    print(f"  {key}: {value}")
    
    def explain_workflow(self):
        """
        Explain the typical Django workflow.
        """
        print("\n" + "=" * 80)
        print("TYPICAL DJANGO WORKFLOW")
        print("=" * 80 + "\n")
        
        workflow = [
            ("1. Create Project", "django-admin startproject mysite"),
            ("2. Create App", "python manage.py startapp main"),
            ("3. Define Models", "Edit main/models.py"),
            ("4. Make Migrations", "python manage.py makemigrations"),
            ("5. Apply Migrations", "python manage.py migrate"),
            ("6. Create Views", "Edit main/views.py"),
            ("7. Configure URLs", "Edit main/urls.py and mysite/urls.py"),
            ("8. Register Admin", "Edit main/admin.py"),
            ("9. Run Server", "python manage.py runserver"),
            ("10. Access Application", "Visit http://127.0.0.1:8000/")
        ]
        
        for step, command in workflow:
            print(f"{step}")
            print(f"  Command: {command}")
            print()
    
    def compare_with_actual(self):
        """
        Compare project structure with actual files.
        """
        print("\n" + "=" * 80)
        print("ACTUAL PROJECT STRUCTURE ANALYSIS")
        print("=" * 80 + "\n")
        
        # Check what exists
        files_found = {
            'manage.py': (self.project_path / 'manage.py').exists(),
            'db.sqlite3': (self.project_path / 'db.sqlite3').exists(),
            'mysite/__init__.py': (self.project_path / 'mysite' / '__init__.py').exists(),
            'mysite/settings.py': (self.project_path / 'mysite' / 'settings.py').exists(),
            'mysite/urls.py': (self.project_path / 'mysite' / 'urls.py').exists(),
            'mysite/wsgi.py': (self.project_path / 'mysite' / 'wsgi.py').exists(),
            'mysite/asgi.py': (self.project_path / 'mysite' / 'asgi.py').exists(),
            'main/__init__.py': (self.project_path / 'main' / '__init__.py').exists(),
            'main/models.py': (self.project_path / 'main' / 'models.py').exists(),
            'main/views.py': (self.project_path / 'main' / 'views.py').exists(),
            'main/admin.py': (self.project_path / 'main' / 'admin.py').exists(),
            'main/apps.py': (self.project_path / 'main' / 'apps.py').exists(),
            'main/tests.py': (self.project_path / 'main' / 'tests.py').exists(),
            'main/migrations/': (self.project_path / 'main' / 'migrations').exists(),
        }
        
        print("Files/Directories Status:\n")
        for file_path, exists in files_found.items():
            status = "✓ EXISTS" if exists else "✗ MISSING"
            print(f"  {status:12} | {file_path}")
        
        # Count total files
        total_files = sum(1 for _ in self.project_path.rglob('*') 
                         if _.is_file() and '__pycache__' not in str(_))
        total_dirs = sum(1 for _ in self.project_path.rglob('*') 
                        if _.is_dir() and '__pycache__' not in str(_))
        
        print(f"\n  Total Files: {total_files}")
        print(f"  Total Directories: {total_dirs}")


def main():
    """
    Main function to run the Django Project Structure Explorer.
    """
    project_path = r"d:\PYTHON\python_Assignment\Module 9 Python DB and Framework\4. Django Introduction\mysite"
    
    # Create explorer instance
    explorer = DjangoProjectExplorer(project_path)
    
    # Display comprehensive information
    explorer.display_project_info()
    explorer.explain_workflow()
    explorer.compare_with_actual()
    
    print("\n" + "=" * 80)
    print("KEY TAKEAWAYS")
    print("=" * 80 + "\n")
    
    takeaways = [
        "Django follows the MTV (Model-Template-View) architecture",
        "Each app is a self-contained module with its own models, views, and tests",
        "manage.py is your command-line interface for administrative tasks",
        "settings.py is the central configuration file for your project",
        "URLs are routed through url patterns in urls.py files",
        "Database changes are managed through migrations",
        "Apps must be registered in INSTALLED_APPS in settings.py",
    ]
    
    for i, takeaway in enumerate(takeaways, 1):
        print(f"{i}. {takeaway}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
