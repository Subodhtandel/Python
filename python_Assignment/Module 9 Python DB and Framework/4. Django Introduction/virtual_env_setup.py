"""
Virtual Environment Setup Guide for Django Projects
This program explains and demonstrates virtual environment setup and management.
"""

import os
import sys
import subprocess
from pathlib import Path


class VirtualEnvManager:
    """
    A class to manage Python virtual environments for Django projects.
    """
    
    def __init__(self, project_path, venv_name="venv"):
        self.project_path = Path(project_path)
        self.venv_name = venv_name
        self.venv_path = self.project_path / venv_name
    
    def display_what_is_venv(self):
        """
        Explain what a virtual environment is.
        """
        print("\n" + "=" * 80)
        print("WHAT IS A VIRTUAL ENVIRONMENT?")
        print("=" * 80 + "\n")
        
        explanation = """
A virtual environment (venv) is an isolated Python environment on your system that:

✓ Allows you to install packages specific to a project
✓ Prevents conflicts between different project dependencies
✓ Keeps your system Python clean and unaffected
✓ Makes it easy to share dependencies using requirements.txt
✓ Ensures reproducibility across different machines

For example:
  Project A might need Django 3.2
  Project B might need Django 4.0
  
With virtual environments, each project can have its own version without conflicts!

Directory Structure:
  mysite/
  ├── venv/                    # Virtual environment folder
  │   ├── Scripts/             # Executable scripts (Windows)
  │   │   ├── activate.bat     # Activation script
  │   │   ├── python.exe       # Python executable
  │   │   └── pip.exe          # Package manager
  │   ├── Lib/                 # Installed packages
  │   └── pyvenv.cfg           # Configuration file
  ├── manage.py
  ├── requirements.txt         # List of project dependencies
  └── mysite/
        """
        print(explanation)
    
    def display_commands(self):
        """
        Display common virtual environment commands.
        """
        print("\n" + "=" * 80)
        print("COMMON VIRTUAL ENVIRONMENT COMMANDS")
        print("=" * 80 + "\n")
        
        commands = {
            "Creating Virtual Environment": {
                "Command": "python -m venv venv",
                "Purpose": "Create a new virtual environment named 'venv'",
                "Notes": "Use python3 on Linux/Mac if python doesn't work"
            },
            "Activating Virtual Environment": {
                "Windows (PowerShell)": ".\\venv\\Scripts\\Activate.ps1",
                "Windows (CMD)": "venv\\Scripts\\activate.bat",
                "Linux/Mac": "source venv/bin/activate",
                "Purpose": "Activate the virtual environment",
                "Result": "Prompt changes to show (venv) prefix"
            },
            "Deactivating Virtual Environment": {
                "Command": "deactivate",
                "Purpose": "Exit the virtual environment",
                "Works On": "All platforms"
            },
            "Installing Packages": {
                "Command": "pip install django",
                "Purpose": "Install Django in the virtual environment",
                "Notes": "Only installs in the active venv"
            },
            "Installing from Requirements": {
                "Command": "pip install -r requirements.txt",
                "Purpose": "Install all dependencies listed in requirements.txt",
                "Useful For": "Sharing projects with others"
            },
            "Freezing Requirements": {
                "Command": "pip freeze > requirements.txt",
                "Purpose": "Generate requirements.txt from installed packages",
                "Notes": "Must be run inside the active venv"
            },
            "Listing Installed Packages": {
                "Command": "pip list",
                "Purpose": "Show all installed packages in the venv",
                "Alternative": "pip freeze"
            }
        }
        
        for category, details in commands.items():
            print(f"\n{'─' * 80}")
            print(f"📋 {category}")
            print(f"{'─' * 80}")
            
            if isinstance(details, dict):
                for key, value in details.items():
                    if key.startswith("Windows") or key.startswith("Linux"):
                        print(f"  {key}: {value}")
                    else:
                        print(f"  {key}: {value}")
            else:
                print(f"  {details}")
    
    def display_workflow(self):
        """
        Display step-by-step workflow.
        """
        print("\n" + "=" * 80)
        print("STEP-BY-STEP SETUP WORKFLOW")
        print("=" * 80 + "\n")
        
        workflow = [
            {
                "step": 1,
                "name": "Create Virtual Environment",
                "command": "python -m venv venv",
                "description": "Creates a new venv directory with Python interpreter"
            },
            {
                "step": 2,
                "name": "Activate Virtual Environment",
                "command": ".\\venv\\Scripts\\Activate.ps1  (PowerShell on Windows)",
                "description": "Activates the virtual environment for this terminal"
            },
            {
                "step": 3,
                "name": "Upgrade pip",
                "command": "python -m pip install --upgrade pip",
                "description": "Ensures you have the latest pip version"
            },
            {
                "step": 4,
                "name": "Install Django",
                "command": "pip install django",
                "description": "Installs Django framework"
            },
            {
                "step": 5,
                "name": "Create Project",
                "command": "django-admin startproject mysite",
                "description": "Generates Django project structure"
            },
            {
                "step": 6,
                "name": "Create App",
                "command": "python manage.py startapp main",
                "description": "Creates a new Django app within the project"
            },
            {
                "step": 7,
                "name": "Generate Requirements",
                "command": "pip freeze > requirements.txt",
                "description": "Saves all dependencies to requirements.txt"
            },
            {
                "step": 8,
                "name": "Run Development Server",
                "command": "python manage.py runserver",
                "description": "Starts the Django development server"
            }
        ]
        
        for item in workflow:
            print(f"\nStep {item['step']}: {item['name']}")
            print(f"  Command: {item['command']}")
            print(f"  Details: {item['description']}")
    
    def display_best_practices(self):
        """
        Display best practices for virtual environments.
        """
        print("\n" + "=" * 80)
        print("BEST PRACTICES FOR VIRTUAL ENVIRONMENTS")
        print("=" * 80 + "\n")
        
        practices = [
            {
                "title": "Always Use Virtual Environments",
                "details": [
                    "Never install packages directly to system Python",
                    "Use venv for every project",
                    "Avoid global package installations"
                ]
            },
            {
                "title": "Version Control",
                "details": [
                    "Add venv/ to .gitignore",
                    "Commit requirements.txt to version control",
                    "This allows others to install dependencies easily"
                ]
            },
            {
                "title": "Naming Conventions",
                "details": [
                    "Common names: venv, env, .venv",
                    "Be consistent across projects",
                    ".venv is often preferred to hide it in file explorers"
                ]
            },
            {
                "title": "Requirements Management",
                "details": [
                    "Regularly update requirements.txt",
                    "Use pip freeze to capture exact versions",
                    "Consider using pip-tools for better dependency management",
                    "Document major dependencies and their versions"
                ]
            },
            {
                "title": "Activation Tips",
                "details": [
                    "Always activate before installing packages",
                    "Check the prompt for (venv) indicator",
                    "Deactivate when done if switching projects",
                    "Use full paths if activation script fails"
                ]
            },
            {
                "title": "Troubleshooting",
                "details": [
                    "If venv won't activate, try: python -m venv venv --upgrade",
                    "If packages won't install, upgrade pip first",
                    "Delete venv folder and recreate if issues persist",
                    "Always recreate venv on a new machine from requirements.txt"
                ]
            }
        ]
        
        for practice in practices:
            print(f"\n{'─' * 80}")
            print(f"✓ {practice['title']}")
            print(f"{'─' * 80}")
            for detail in practice['details']:
                print(f"  • {detail}")
    
    def display_gitignore_template(self):
        """
        Display .gitignore template for Django projects.
        """
        print("\n" + "=" * 80)
        print(".GITIGNORE TEMPLATE FOR DJANGO PROJECTS")
        print("=" * 80 + "\n")
        
        gitignore_content = """
# Virtual Environment
venv/
env/
.venv/
ENV/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
/media
/staticfiles

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment variables
.env
.env.local

# IDE Settings
.project
.pydevproject
.settings/
*.sublime-project
*.sublime-workspace

# OS
Thumbs.db
.DS_Store
        """
        
        print(gitignore_content)
    
    def show_status(self):
        """
        Show the status of the virtual environment.
        """
        print("\n" + "=" * 80)
        print("VIRTUAL ENVIRONMENT STATUS")
        print("=" * 80 + "\n")
        
        print(f"Project Path: {self.project_path}")
        print(f"Virtual Environment Path: {self.venv_path}")
        print(f"Virtual Environment Name: {self.venv_name}")
        
        if self.venv_path.exists():
            print(f"\n✓ Virtual Environment EXISTS")
            
            # Check for key directories
            scripts_path = self.venv_path / "Scripts"
            lib_path = self.venv_path / "Lib"
            
            print(f"  • Scripts folder: {'✓ EXISTS' if scripts_path.exists() else '✗ MISSING'}")
            print(f"  • Lib folder: {'✓ EXISTS' if lib_path.exists() else '✗ MISSING'}")
            
            # Check for Python executable
            python_exe = scripts_path / "python.exe"
            if python_exe.exists():
                print(f"  • Python executable: ✓ EXISTS")
            else:
                print(f"  • Python executable: ✗ MISSING")
        else:
            print(f"\n✗ Virtual Environment DOES NOT EXIST")
            print(f"  Run: python -m venv {self.venv_name}")


def main():
    """
    Main function to display virtual environment setup guide.
    """
    project_path = r"d:\PYTHON\python_Assignment\Module 9 Python DB and Framework\4. Django Introduction\mysite"
    
    # Create manager instance
    manager = VirtualEnvManager(project_path, "venv")
    
    # Display comprehensive guide
    manager.display_what_is_venv()
    manager.display_commands()
    manager.display_workflow()
    manager.display_best_practices()
    manager.display_gitignore_template()
    manager.show_status()
    
    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80 + "\n")
    
    print("To set up your Django virtual environment:\n")
    print("1. Open PowerShell and navigate to your project folder:")
    print("   cd 'd:\\PYTHON\\python_Assignment\\Module 9 Python DB and Framework\\4. Django Introduction\\mysite'")
    print("\n2. Create the virtual environment:")
    print("   python -m venv venv")
    print("\n3. Activate the virtual environment:")
    print("   .\\venv\\Scripts\\Activate.ps1")
    print("\n4. Upgrade pip:")
    print("   python -m pip install --upgrade pip")
    print("\n5. Install required packages:")
    print("   pip install django")
    print("\n6. Generate requirements file:")
    print("   pip freeze > requirements.txt")
    print("\n7. Start development:")
    print("   python manage.py runserver")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
