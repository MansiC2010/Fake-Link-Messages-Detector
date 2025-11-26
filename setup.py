"""
Setup script for Fake Message and Link Detection System
Automatically creates virtual environment and installs dependencies
"""

import os
import sys
import subprocess
import platform

def create_virtual_env():
    """Create virtual environment"""
    venv_name = 'venv'
    
    if os.path.exists(venv_name):
        print(f"Virtual environment '{venv_name}' already exists.")
        return venv_name
    
    print(f"Creating virtual environment '{venv_name}'...")
    subprocess.check_call([sys.executable, '-m', 'venv', venv_name])
    print(f"[OK] Virtual environment created successfully!")
    return venv_name

def get_pip_command(venv_name):
    """Get the pip command for the virtual environment"""
    if platform.system() == 'Windows':
        pip_path = os.path.join(venv_name, 'Scripts', 'pip.exe')
        python_path = os.path.join(venv_name, 'Scripts', 'python.exe')
    else:
        pip_path = os.path.join(venv_name, 'bin', 'pip')
        python_path = os.path.join(venv_name, 'bin', 'python')
    
    return pip_path, python_path

def install_dependencies(venv_name):
    """Install required dependencies"""
    pip_path, python_path = get_pip_command(venv_name)
    
    print("\nInstalling dependencies from requirements.txt...")
    try:
        # Try to upgrade pip (may fail if pip is in use, that's okay)
        try:
            subprocess.check_call([pip_path, 'install', '--upgrade', 'pip'], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass  # Ignore pip upgrade errors
        
        # Install requirements
        subprocess.check_call([pip_path, 'install', '-r', 'requirements.txt'])
        print("[OK] All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error installing dependencies: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 70)
    print("Fake Message and Link Detection System - Setup")
    print("=" * 70)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("[ERROR] Python 3.7 or higher is required.")
        print(f"  Current version: {sys.version}")
        sys.exit(1)
    
    print(f"[OK] Python version: {sys.version.split()[0]}")
    
    # Create virtual environment
    venv_name = create_virtual_env()
    
    # Install dependencies
    if not install_dependencies(venv_name):
        sys.exit(1)
    
    # Print instructions
    print("\n" + "=" * 70)
    print("Setup Complete!")
    print("=" * 70)
    print("\nTo activate the virtual environment:")
    
    if platform.system() == 'Windows':
        print(f"  {venv_name}\\Scripts\\activate")
        print("\nOr in PowerShell:")
        print(f"  {venv_name}\\Scripts\\Activate.ps1")
    else:
        print(f"  source {venv_name}/bin/activate")
    
    print("\nNext steps:")
    print("  1. Activate the virtual environment (see above)")
    print("  2. Run: python train_models.py")
    print("  3. Run: python demo.py")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()

