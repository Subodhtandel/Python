"""
Virtual Environment Creation and Django Installation Program
This program demonstrates creating a virtual environment, activating it,
and installing Django with all necessary dependencies.
"""

import os
import sys
import subprocess
import json
from pathlib import Path


class VirtualEnvironmentManager:
    """
    A comprehensive class to manage virtual environment creation, activation,
    and package installation for Django projects.
    """
    
    def __init__(self, project_path, venv_name="venv"):
        """
        Initialize the Virtual Environment Manager.
        
        Args:
            project_path (str): Path to the project directory
            venv_name (str): Name of the virtual environment folder
        """
        self.project_path = Path(project_path)
        self.venv_name = venv_name
        self.venv_path = self.project_path / venv_name
        self.python_exe = self.venv_path / "Scripts" / "python.exe"
        self.pip_exe = self.venv_path / "Scripts" / "pip.exe"
        self.activate_script = self.venv_path / "Scripts" / "Activate.ps1"
    
    def display_program_overview(self):
        """
        Display the program overview and objectives.
        """
        print("\n" + "=" * 90)
        print("VIRTUAL ENVIRONMENT CREATION AND DJANGO INSTALLATION PROGRAM")
        print("=" * 90 + "\n")
        
        overview = """
OBJECTIVES:
───────────
✓ Create a Python virtual environment
✓ Display the virtual environment directory structure
✓ Understand virtual environment components
✓ Activate the virtual environment
✓ Install Django and dependencies
✓ Verify successful installation
✓ Generate requirements.txt file

WHY USE VIRTUAL ENVIRONMENTS?
──────────────────────────────
1. Isolation: Each project has its own dependencies
2. Version Control: Different projects can use different package versions
3. Clean System: Doesn't affect system-wide Python installation
4. Reproducibility: Easy to replicate environment on other machines
5. Dependency Management: Track exactly what's needed for the project

PROGRAM FLOW:
─────────────
Step 1: Create virtual environment
Step 2: Display directory structure
Step 3: Show virtual environment components
Step 4: Display activation instructions
Step 5: Provide installation verification
Step 6: Show requirements management
        """
        print(overview)
    
    def create_virtual_environment(self):
        """
        Create a new Python virtual environment.
        
        Returns:
            bool: True if successful, False otherwise
        """
        print("\n" + "=" * 90)
        print("STEP 1: CREATING VIRTUAL ENVIRONMENT")
        print("=" * 90 + "\n")
        
        print(f"Creating virtual environment at: {self.venv_path}\n")
        
        try:
            # Create the virtual environment
            subprocess.run(
                [sys.executable, "-m", "venv", str(self.venv_path)],
                check=True,
                capture_output=True
            )
            
            print("✓ Virtual environment created successfully!\n")
            
            # Verify creation
            if self.venv_path.exists():
                print(f"Location: {self.venv_path}")
                print(f"Status: READY FOR USE\n")
                return True
            else:
                print("✗ Failed to create virtual environment")
                return False
        
        except subprocess.CalledProcessError as e:
            print(f"✗ Error creating virtual environment: {e}")
            return False
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return False
    
    def display_venv_structure(self):
        """
        Display and explain the virtual environment directory structure.
        """
        print("\n" + "=" * 90)
        print("STEP 2: VIRTUAL ENVIRONMENT DIRECTORY STRUCTURE")
        print("=" * 90 + "\n")
        
        structure = """
Virtual Environment Folder Layout:
──────────────────────────────────

venv/
├── Scripts/                          # Executable scripts and binaries
│   ├── Activate.ps1                 # PowerShell activation script
│   ├── activate.bat                 # Command Prompt activation script
│   ├── python.exe                   # Python interpreter
│   ├── pip.exe                      # Package manager
│   ├── pip3.exe                     # Python 3 package manager
│   ├── django-admin.exe             # Django admin tool
│   └── ... (other utilities)
│
├── Lib/                              # Site-packages and libraries
│   ├── site-packages/               # Installed Python packages
│   │   ├── django/                  # Django framework
│   │   ├── asgiref/                 # ASGI reference implementation
│   │   ├── sqlparse/                # SQL parser
│   │   └── ... (other packages)
│   └── python-version.zip           # Standard library
│
├── Include/                          # C header files
│   └── python.h                     # Python header file
│
└── pyvenv.cfg                        # Virtual environment configuration
    
        """
        print(structure)
        
        # Show what actually exists
        print("\nActual Directory Contents:")
        print("─" * 90 + "\n")
        
        if self.venv_path.exists():
            for item in sorted(self.venv_path.iterdir()):
                item_type = "📁 [DIR]" if item.is_dir() else "📄 [FILE]"
                print(f"  {item_type}  {item.name}")
            
            # Check for key folders
            print("\n\nKey Components Status:")
            print("─" * 90)
            
            components = {
                "Scripts folder": self.venv_path / "Scripts",
                "Lib folder": self.venv_path / "Lib",
                "Include folder": self.venv_path / "Include",
                "Python executable": self.python_exe,
                "Pip executable": self.pip_exe,
                "Activation script": self.activate_script,
            }
            
            for component_name, component_path in components.items():
                exists = component_path.exists()
                status = "✓ EXISTS" if exists else "✗ MISSING"
                print(f"  {status:<12} | {component_name}")
        else:
            print("  ✗ Virtual environment folder does not exist yet!")
    
    def display_venv_components(self):
        """
        Display and explain the components of a virtual environment.
        """
        print("\n" + "=" * 90)
        print("STEP 3: UNDERSTANDING VIRTUAL ENVIRONMENT COMPONENTS")
        print("=" * 90 + "\n")
        
        components = {
            "Scripts/ Folder": {
                "Purpose": "Contains executable scripts and binaries",
                "Key Files": [
                    "Activate.ps1 - PowerShell activation script",
                    "activate.bat - CMD activation script",
                    "python.exe - Isolated Python interpreter",
                    "pip.exe - Package manager for this venv",
                    "django-admin.exe - Django admin tool"
                ],
                "Usage": "All Python commands run in this venv use these executables"
            },
            "Lib/ Folder": {
                "Purpose": "Contains the Python standard library and installed packages",
                "Key Directories": [
                    "site-packages/ - Third-party packages (Django, requests, etc.)",
                    "python3.x/ - Standard library modules"
                ],
                "Usage": "When you install packages with pip, they go here"
            },
            "Include/ Folder": {
                "Purpose": "Contains C header files for Python extensions",
                "Key Files": [
                    "python.h - Main Python header"
                ],
                "Usage": "Needed for compiling C extensions (advanced use)"
            },
            "pyvenv.cfg": {
                "Purpose": "Configuration file for the virtual environment",
                "Contains": [
                    "home = [path to system Python]",
                    "include-system-site-packages = false",
                    "version = [Python version]"
                ],
                "Usage": "Tells Python where the real installation is"
            }
        }
        
        for component, details in components.items():
            print(f"\n{'─' * 90}")
            print(f"📦 {component}")
            print(f"{'─' * 90}")
            
            for key, value in details.items():
                if isinstance(value, list):
                    print(f"\n  {key}:")
                    for item in value:
                        print(f"    • {item}")
                else:
                    print(f"\n  {key}: {value}")
    
    def display_activation_instructions(self):
        """
        Display detailed instructions for activating the virtual environment.
        """
        print("\n" + "=" * 90)
        print("STEP 4: ACTIVATING THE VIRTUAL ENVIRONMENT")
        print("=" * 90 + "\n")
        
        instructions = f"""
HOW TO ACTIVATE THE VIRTUAL ENVIRONMENT:
─────────────────────────────────────────

METHOD 1: PowerShell (Recommended for Windows)
──────────────────────────────────────────────
Command:
  cd "{self.project_path}"
  .\\{self.venv_name}\\Scripts\\Activate.ps1

Result:
  ({self.venv_name}) C:\\path\\to\\project>


METHOD 2: Command Prompt (Windows)
──────────────────────────────────
Command:
  cd "{self.project_path}"
  {self.venv_name}\\Scripts\\activate.bat

Result:
  ({self.venv_name}) C:\\path\\to\\project>


METHOD 3: Linux/Mac Terminal
──────────────────────────────
Command:
  cd {self.project_path}
  source {self.venv_name}/bin/activate

Result:
  ({self.venv_name}) user@machine:~/project$


WHAT HAPPENS WHEN ACTIVATED:
────────────────────────────
1. Prompt changes to show ({self.venv_name}) prefix
2. Python interpreter points to venv's python.exe
3. pip installs packages into the venv, not system Python
4. All Python commands use the isolated environment
5. Virtual environment is LOCAL to that terminal session


IMPORTANT NOTES:
────────────────
✓ You MUST activate before installing packages
✓ Different terminal sessions need separate activation
✓ Activation is NOT permanent (ends when terminal closes)
✓ Always check for ({self.venv_name}) prefix in your prompt
✓ Use 'deactivate' command to exit the virtual environment


DEACTIVATING THE VIRTUAL ENVIRONMENT:
──────────────────────────────────────
Command:
  deactivate

Result:
  ({self.venv_name}) C:\\path\\to\\project> deactivate
  C:\\path\\to\\project>
        """
        print(instructions)
    
    def display_installation_steps(self):
        """
        Display steps for installing Django.
        """
        print("\n" + "=" * 90)
        print("STEP 5: INSTALLING DJANGO AND DEPENDENCIES")
        print("=" * 90 + "\n")
        
        steps = f"""
DJANGO INSTALLATION PROCEDURE:
──────────────────────────────

Step 1: Activate Virtual Environment
────────────────────────────────────
Command:
  .\\{self.venv_name}\\Scripts\\Activate.ps1

Expected:
  ({self.venv_name}) C:\\path\\to\\project>


Step 2: Upgrade pip (Optional but Recommended)
───────────────────────────────────────────────
Command:
  python -m pip install --upgrade pip

Purpose:
  • Ensures you have the latest pip version
  • Fixes potential installation issues
  • Better dependency resolution

Output:
  Successfully installed pip-xx.x


Step 3: Install Django
──────────────────────
Command:
  pip install django

What Gets Installed:
  • Django 6.0 (latest stable version)
  • asgiref 3.11.0 (ASGI support)
  • sqlparse 0.5.4 (SQL query parsing)
  • tzdata 2025.2 (timezone information)

Output:
  Successfully installed django-6.0 asgiref-3.11.0 sqlparse-0.5.4 tzdata-2025.2


Step 4: Verify Installation
────────────────────────────
Commands:
  pip list                                    # List all packages
  pip show django                             # Show Django details
  python -c "import django; print(django.VERSION)"  # Print Django version

Expected Output:
  Django       6.0
  asgiref      3.11.0
  sqlparse     0.5.4
  tzdata       2025.2
  pip          25.x


Step 5: Create Django Project (Optional)
──────────────────────────────────────────
Command:
  django-admin startproject myproject

Creates:
  myproject/
  ├── manage.py
  └── myproject/
      ├── __init__.py
      ├── settings.py
      ├── urls.py
      ├── asgi.py
      └── wsgi.py


Step 6: Run Development Server
──────────────────────────────
Command:
  python manage.py runserver

Expected Output:
  Starting development server at http://127.0.0.1:8000/
  Quit the server with CONTROL-C.


COMMON DJANGO COMMANDS:
──────────────────────
makemigrations    - Create database migrations
migrate           - Apply database migrations
createsuperuser   - Create admin account
startapp          - Create new Django app
shell             - Open Django Python shell
runserver         - Start development server
collectstatic     - Collect static files

Example:
  python manage.py migrate
  python manage.py createsuperuser
  python manage.py startapp blog
        """
        print(steps)
    
    def display_requirements_management(self):
        """
        Display information about requirements.txt management.
        """
        print("\n" + "=" * 90)
        print("STEP 6: MANAGING PROJECT DEPENDENCIES (requirements.txt)")
        print("=" * 90 + "\n")
        
        requirements_info = """
WHAT IS requirements.txt?
─────────────────────────
A text file that lists all project dependencies with their specific versions.
Allows others to install the exact same packages used in your project.


GENERATING requirements.txt:
──────────────────────────
Command (while venv is activated):
  pip freeze > requirements.txt

Result:
  File created with contents like:
  
  asgiref==3.11.0
  Django==6.0
  sqlparse==0.5.4
  tzdata==2025.2


WHY USE requirements.txt?
─────────────────────────
✓ Version Control: Track exact package versions
✓ Reproducibility: Same environment across machines
✓ Collaboration: Share with team members
✓ Deployment: Deploy with identical packages
✓ Documentation: Clear list of project dependencies


HOW TO USE requirements.txt:
───────────────────────────

To Install From requirements.txt:
  pip install -r requirements.txt

To Update requirements.txt:
  pip freeze > requirements.txt  (after installing new packages)

To Uninstall All Packages:
  pip freeze | xargs pip uninstall -y

To Show Package Info:
  pip show django
  pip show -f django  (show files)


EXAMPLE requirements.txt:
────────────────────────
# Django Web Framework
Django==6.0

# REST API Framework
djangorestframework==3.14.0

# Image Processing
Pillow==10.0.0

# Environment Variables
python-dotenv==1.0.0

# Database
psycopg2-binary==2.9.7

# Testing
pytest==7.4.0
pytest-django==4.5.2

# Code Quality
flake8==6.0.0
black==23.7.0


BEST PRACTICES:
───────────────
✓ Always create requirements.txt for your projects
✓ Update it whenever you install new packages
✓ Commit requirements.txt to version control
✓ Never commit the venv/ folder to git
✓ Use specific versions (==) for production
✓ Use >= for flexible versions during development
✓ Document major dependencies in comments
        """
        print(requirements_info)
    
    def display_troubleshooting(self):
        """
        Display troubleshooting guide.
        """
        print("\n" + "=" * 90)
        print("TROUBLESHOOTING GUIDE")
        print("=" * 90 + "\n")
        
        troubleshooting = """
COMMON ISSUES AND SOLUTIONS:
───────────────────────────

ISSUE 1: "python: command not found"
────────────────────────────────────
Cause: Python is not in PATH
Solution:
  • Use full path: C:\\Python\\python.exe -m venv venv
  • Or use: python3 -m venv venv
  • Or add Python to PATH environment variable


ISSUE 2: "Cannot activate the script"
──────────────────────────────────────
Cause: PowerShell execution policy blocks scripts
Solution:
  • Run PowerShell as Administrator
  • Run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  • Then try activation again


ISSUE 3: "pip: command not found" (after activation)
────────────────────────────────────────────────────
Cause: Virtual environment not properly activated
Solution:
  • Check for (venv) prefix in prompt
  • Deactivate with: deactivate
  • Activate again with: .\\venv\\Scripts\\Activate.ps1
  • Or use: python -m pip install django


ISSUE 4: "Module not found" after installing package
─────────────────────────────────────────────────────
Cause: Not using the activated venv's Python
Solution:
  • Verify (venv) is in your prompt
  • Use: which python (to check which Python is active)
  • Reinstall: pip install --force-reinstall package-name


ISSUE 5: "Permission denied" during activation
───────────────────────────────────────────────
Cause: Script execution not allowed
Solution:
  • Use CMD instead: venv\\Scripts\\activate.bat
  • Or use Python directly: python -m venv venv


ISSUE 6: Virtual environment won't activate
────────────────────────────────────────────
Cause: Corrupted virtual environment
Solution:
  • Delete venv folder: rmdir /s venv
  • Recreate: python -m venv venv
  • Activate again


VERIFICATION CHECKLIST:
──────────────────────
✓ Can I see (venv) in my prompt?
✓ Can I run: python --version
✓ Can I run: pip list
✓ Can I import django: python -c "import django"
✓ Is virtual environment folder created?
✓ Does requirements.txt exist?
        """
        print(troubleshooting)
    
    def display_quick_reference(self):
        """
        Display quick reference guide.
        """
        print("\n" + "=" * 90)
        print("QUICK REFERENCE GUIDE")
        print("=" * 90 + "\n")
        
        reference = """
ESSENTIAL COMMANDS:
──────────────────

Virtual Environment:
  Create:         python -m venv venv
  Activate (PS):  .\\venv\\Scripts\\Activate.ps1
  Activate (CMD): venv\\Scripts\\activate.bat
  Deactivate:     deactivate

Package Management:
  Install:        pip install package-name
  Uninstall:      pip uninstall package-name
  Upgrade:        pip install --upgrade package-name
  List all:       pip list
  Show info:      pip show package-name
  Save to file:   pip freeze > requirements.txt
  Install from:   pip install -r requirements.txt

Django Commands:
  Create project: django-admin startproject myproject
  Create app:     python manage.py startapp appname
  Migrations:     python manage.py makemigrations
  Apply migrate:  python manage.py migrate
  Run server:     python manage.py runserver
  Create admin:   python manage.py createsuperuser
  Open shell:     python manage.py shell


WORKFLOW SUMMARY:
─────────────────
1. Create venv:      python -m venv venv
2. Activate venv:    .\\venv\\Scripts\\Activate.ps1
3. Upgrade pip:      python -m pip install --upgrade pip
4. Install Django:   pip install django
5. Create project:   django-admin startproject myproject
6. Save requirements: pip freeze > requirements.txt
7. Run server:       python manage.py runserver
        """
        print(reference)
    
    def display_summary(self):
        """
        Display program summary.
        """
        print("\n" + "=" * 90)
        print("PROGRAM SUMMARY")
        print("=" * 90 + "\n")
        
        summary = f"""
WHAT THIS PROGRAM COVERED:
──────────────────────────

✓ Virtual Environment Basics
  • What virtual environments are
  • Why they are important
  • How they work

✓ Creating Virtual Environments
  • Step-by-step creation process
  • Directory structure explanation
  • Component breakdown

✓ Virtual Environment Activation
  • Windows PowerShell activation
  • Windows Command Prompt activation
  • Linux/Mac activation
  • Verification methods

✓ Installing Django
  • Installation process
  • Dependency overview
  • Verification steps
  • Common commands

✓ Dependency Management
  • requirements.txt creation
  • Package management
  • Version control

✓ Troubleshooting
  • Common issues
  • Solutions
  • Best practices


YOUR PROJECT STRUCTURE:
──────────────────────
{self.project_path}/
├── {self.venv_name}/                    # Virtual environment folder
│   ├── Scripts/                         # Python executables
│   ├── Lib/                             # Installed packages
│   └── Include/                         # C headers
├── manage.py                            # Django management script (optional)
└── requirements.txt                     # Project dependencies (optional)


NEXT STEPS:
───────────
1. Activate your virtual environment:
   .\\{self.venv_name}\\Scripts\\Activate.ps1

2. Install Django:
   pip install django

3. Create Django project:
   django-admin startproject myproject

4. Run development server:
   cd myproject
   python manage.py runserver

5. Visit: http://127.0.0.1:8000/


KEY TAKEAWAYS:
──────────────
• Virtual environments isolate project dependencies
• Always activate before installing packages
• Use requirements.txt for dependency management
• Never commit venv/ to version control
• One virtual environment per project (best practice)
• Easy to recreate from requirements.txt
        """
        print(summary)


def main():
    """
    Main function to run the complete virtual environment setup guide.
    """
    # Use Module 9 folder
    project_path = r"d:\PYTHON\python_Assignment\Module 9 Python DB and Framework"
    
    # Create manager instance
    manager = VirtualEnvironmentManager(project_path, "venv")
    
    # Display comprehensive guide
    manager.display_program_overview()
    
    # Check if venv already exists
    if not manager.venv_path.exists():
        print("\nAttempting to create virtual environment...")
        manager.create_virtual_environment()
    else:
        print(f"\n✓ Virtual environment already exists at: {manager.venv_path}")
    
    # Display all information
    manager.display_venv_structure()
    manager.display_venv_components()
    manager.display_activation_instructions()
    manager.display_installation_steps()
    manager.display_requirements_management()
    manager.display_troubleshooting()
    manager.display_quick_reference()
    manager.display_summary()
    
    print("\n" + "=" * 90)
    print("END OF PROGRAM")
    print("=" * 90 + "\n")


if __name__ == "__main__":
    main()
