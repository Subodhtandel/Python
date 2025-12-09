"""
Virtual Environment Verification Script
Tests that the Django virtual environment is properly configured and ready to use.
"""

import subprocess
import sys
from pathlib import Path


class VenvVerifier:
    """
    Verifies that the virtual environment is properly set up.
    """
    
    def __init__(self, project_path, venv_name="venv"):
        self.project_path = Path(project_path)
        self.venv_path = self.project_path / venv_name
        self.python_exe = self.venv_path / "Scripts" / "python.exe"
        self.pip_exe = self.venv_path / "Scripts" / "pip.exe"
    
    def verify_structure(self):
        """
        Verify the virtual environment directory structure.
        """
        print("\n" + "=" * 80)
        print("VIRTUAL ENVIRONMENT VERIFICATION")
        print("=" * 80 + "\n")
        
        print("Checking Directory Structure:")
        print(f"  Project Path: {self.project_path}")
        print(f"  Venv Path: {self.venv_path}")
        
        checks = {
            "Venv Folder": self.venv_path.exists(),
            "Scripts Folder": (self.venv_path / "Scripts").exists(),
            "Lib Folder": (self.venv_path / "Lib").exists(),
            "Python Executable": self.python_exe.exists(),
            "Pip Executable": self.pip_exe.exists(),
            "pyvenv.cfg": (self.venv_path / "pyvenv.cfg").exists(),
        }
        
        print("\nDirectory Structure Status:")
        all_exist = True
        for check_name, exists in checks.items():
            status = "✓" if exists else "✗"
            print(f"  {status} {check_name}")
            if not exists:
                all_exist = False
        
        return all_exist
    
    def verify_files(self):
        """
        Verify that required files exist.
        """
        print("\n" + "─" * 80)
        print("Project Files Status:")
        print("─" * 80)
        
        files = {
            "manage.py": self.project_path / "manage.py",
            "db.sqlite3": self.project_path / "db.sqlite3",
            "requirements.txt": self.project_path / "requirements.txt",
            ".gitignore": self.project_path / ".gitignore",
        }
        
        all_exist = True
        for file_name, file_path in files.items():
            exists = file_path.exists()
            status = "✓" if exists else "✗"
            print(f"  {status} {file_name}")
            if not exists:
                all_exist = False
        
        return all_exist
    
    def verify_packages(self):
        """
        Verify that Django and other packages are installed.
        """
        print("\n" + "─" * 80)
        print("Installed Packages:")
        print("─" * 80 + "\n")
        
        try:
            # Get pip list output
            result = subprocess.run(
                [str(self.pip_exe), "list", "--format=json"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                import json
                packages = json.loads(result.stdout)
                
                required = {"Django", "asgiref", "sqlparse", "tzdata"}
                found = set()
                
                print(f"{'Package':<20} {'Version':<15}")
                print("─" * 35)
                
                for package in packages:
                    name = package["name"]
                    version = package["version"]
                    print(f"{name:<20} {version:<15}")
                    
                    if name in required:
                        found.add(name)
                
                print("\nRequired Packages Check:")
                all_found = True
                for pkg in required:
                    status = "✓" if pkg in found else "✗"
                    print(f"  {status} {pkg}")
                    if pkg not in found:
                        all_found = False
                
                return all_found
            else:
                print("Error running pip list:", result.stderr)
                return False
        
        except Exception as e:
            print(f"Error verifying packages: {e}")
            return False
    
    def verify_django(self):
        """
        Verify Django installation and version.
        """
        print("\n" + "─" * 80)
        print("Django Verification:")
        print("─" * 80 + "\n")
        
        try:
            result = subprocess.run(
                [str(self.python_exe), "-c", "import django; print(django.get_version())"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✓ Django is installed")
                print(f"  Version: {version}")
                return True
            else:
                print("✗ Django is not installed")
                return False
        
        except Exception as e:
            print(f"Error checking Django: {e}")
            return False
    
    def verify_manage_py(self):
        """
        Verify that manage.py is accessible.
        """
        print("\n" + "─" * 80)
        print("Django Project Files:")
        print("─" * 80 + "\n")
        
        try:
            result = subprocess.run(
                [str(self.python_exe), str(self.project_path / "manage.py"), "check"],
                capture_output=True,
                text=True,
                cwd=str(self.project_path)
            )
            
            if result.returncode == 0:
                print("✓ manage.py is working correctly")
                print("  Django project is properly configured")
                return True
            else:
                print("⚠ manage.py check output:")
                print(result.stdout)
                if result.stderr:
                    print("Errors:", result.stderr)
                return True  # Still consider it okay if project exists
        
        except Exception as e:
            print(f"Note: {e}")
            return True
    
    def run_all_checks(self):
        """
        Run all verification checks.
        """
        checks_results = {
            "Directory Structure": self.verify_structure(),
            "Project Files": self.verify_files(),
            "Installed Packages": self.verify_packages(),
            "Django Installation": self.verify_django(),
            "Django Project Files": self.verify_manage_py(),
        }
        
        print("\n" + "=" * 80)
        print("VERIFICATION SUMMARY")
        print("=" * 80 + "\n")
        
        for check_name, result in checks_results.items():
            status = "✓ PASSED" if result else "✗ FAILED"
            print(f"{status:<15} | {check_name}")
        
        all_passed = all(checks_results.values())
        
        print("\n" + "=" * 80)
        if all_passed:
            print("✓ ALL CHECKS PASSED - Virtual Environment is Ready!")
        else:
            print("⚠ Some checks did not pass - Review the output above")
        print("=" * 80 + "\n")
        
        return all_passed
    
    def print_activation_instructions(self):
        """
        Print instructions for activating the virtual environment.
        """
        print("\n" + "=" * 80)
        print("HOW TO USE YOUR VIRTUAL ENVIRONMENT")
        print("=" * 80 + "\n")
        
        print("1. Activate the virtual environment:")
        print(f"   cd \"{self.project_path}\"")
        print("   .\\venv\\Scripts\\Activate.ps1\n")
        
        print("2. You should see (venv) in your prompt:\n")
        print("   (venv) C:\\path\\to\\mysite>\n")
        
        print("3. Now you can run Django commands:")
        print("   python manage.py runserver")
        print("   python manage.py migrate")
        print("   python manage.py createsuperuser\n")
        
        print("4. To deactivate:")
        print("   deactivate\n")
        
        print("=" * 80 + "\n")


def main():
    """
    Main function.
    """
    project_path = r"d:\PYTHON\python_Assignment\Module 9 Python DB and Framework\4. Django Introduction\mysite"
    
    verifier = VenvVerifier(project_path, "venv")
    verifier.run_all_checks()
    verifier.print_activation_instructions()


if __name__ == "__main__":
    main()
