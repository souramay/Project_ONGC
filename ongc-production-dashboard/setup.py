#!/usr/bin/env python3
"""
Setup script for ONGC Monthly Production Dashboard
Installs all required dependencies and verifies the installation
"""

import sys
import subprocess
import os
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"   {text}")
    print("="*60)

def print_step(step, total, description):
    """Print step information"""
    print(f"\n[{step}/{total}] {description}")
    print("-" * 40)

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8 or higher is required")
        print("Please upgrade your Python installation")
        return False
    
    return True

def install_package(package):
    """Install a single package"""
    try:
        print(f"Installing {package}...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", package
        ], capture_output=True, text=True, check=True)
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}")
        print(f"Error: {e.stderr}")
        return False

def verify_import(module_name, package_name=None):
    """Verify that a module can be imported"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"✅ {package_name} is working")
        return True
    except ImportError:
        print(f"❌ {package_name} failed to import")
        return False

def check_file_exists(filename, required=True):
    """Check if a file exists"""
    if os.path.exists(filename):
        print(f"✅ {filename} found")
        return True
    else:
        status = "❌" if required else "⚠️ "
        print(f"{status} {filename} not found")
        return False

def main():
    """Main setup function"""
    
    print_header("ONGC Monthly Production Dashboard - Setup")
    print("\nThis script will install all required dependencies")
    print("for the Monthly Production Dashboard application.\n")
    
    # Step 1: Check Python version
    print_step(1, 6, "Checking Python installation")
    if not check_python_version():
        return 1
    
    # Step 2: Upgrade pip
    print_step(2, 6, "Upgrading pip")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ], check=True, capture_output=True)
        print("✅ pip upgraded successfully")
    except subprocess.CalledProcessError:
        print("⚠️  Could not upgrade pip, continuing with current version")
    
    # Step 3: Install packages
    print_step(3, 6, "Installing required packages")
    
    packages = [
        "pandas>=1.5.0",
        "matplotlib>=3.6.0", 
        "Pillow>=9.0.0",
        "numpy>=1.20.0",
        "openpyxl>=3.0.0"
    ]
    
    failed_packages = []
    
    for package in packages:
        if not install_package(package):
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n❌ Failed to install: {', '.join(failed_packages)}")
        print("Please check your internet connection and try again")
        return 1
    
    # Step 4: Verify installations
    print_step(4, 6, "Verifying installations")
    
    verification_tests = [
        ("pandas", "pandas"),
        ("matplotlib", "matplotlib"),
        ("PIL", "Pillow"),
        ("numpy", "numpy"),
        ("tkinter", "tkinter"),
        ("openpyxl", "openpyxl")
    ]
    
    failed_verifications = []
    
    for module, package in verification_tests:
        if not verify_import(module, package):
            failed_verifications.append(package)
    
    # Step 5: Check required files
    print_step(5, 6, "Checking required files")
    
    required_files = [
        ("Monthly_Production.py", True),
        ("Monthly_Production_Volume_Students.csv", True),
    ]
    
    optional_files = [
        ("logo.png", False),
        ("ongc.png", False),
        ("run_dashboard.bat", False)
    ]
    
    missing_required = []
    
    for filename, required in required_files:
        if not check_file_exists(filename, required) and required:
            missing_required.append(filename)
    
    for filename, required in optional_files:
        check_file_exists(filename, required)
    
    # Step 6: Final report
    print_step(6, 6, "Setup Summary")
    
    if failed_verifications:
        print(f"❌ Some packages failed verification: {', '.join(failed_verifications)}")
        return 1
    
    if missing_required:
        print(f"❌ Missing required files: {', '.join(missing_required)}")
        print("Please ensure all required files are in the same directory")
        return 1
    
    print_header("SETUP COMPLETE")
    print("\n✅ All dependencies have been installed successfully!")
    print("\nYou can now run the dashboard using:")
    print("  • Command line: python Monthly_Production.py")
    print("  • Double-click: run_dashboard.bat (if available)")
    
    if not os.path.exists("run_dashboard.bat"):
        print("\n💡 Tip: Consider creating run_dashboard.bat for easier execution")
    
    print("\nIf you encounter any issues, please ensure:")
    print("  1. All required files are in the same directory")
    print("  2. Python is properly installed with tkinter support")
    print("  3. Internet connection is available for package downloads")
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        input("\nPress Enter to exit...")
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
