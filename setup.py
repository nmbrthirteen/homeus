#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def setup_homeus():
    print("🏠 Setting up Homeus - Georgian Real Estate Scraper")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print(f"📁 Working directory: {project_root}")
    
    if not run_command("python --version", "Checking Python version"):
        print("❌ Python is required. Please install Python 3.8+")
        return False
    
    venv_path = project_root / "venv"
    if not venv_path.exists():
        if not run_command("python -m venv venv", "Creating virtual environment"):
            return False
    else:
        print("✅ Virtual environment already exists")
    
    if sys.platform == "win32":
        activate_script = venv_path / "Scripts" / "activate"
        pip_path = venv_path / "Scripts" / "pip"
    else:
        activate_script = venv_path / "bin" / "activate"
        pip_path = venv_path / "bin" / "pip"
    
    if not run_command(f"{pip_path} install -r requirements.txt", "Installing dependencies"):
        return False
    
    config_path = project_root / "config" / "config.yaml"
    config_example_path = project_root / "config" / "config.example.yaml"
    
    if not config_path.exists() and config_example_path.exists():
        shutil.copy(config_example_path, config_path)
        print("✅ Configuration file created from example")
        print("⚠️  Please edit config/config.yaml with your settings")
    elif config_path.exists():
        print("✅ Configuration file already exists")
    else:
        print("❌ No configuration example found")
        return False
    
    data_dir = project_root / "data"
    logs_dir = data_dir / "logs"
    
    data_dir.mkdir(exist_ok=True)
    logs_dir.mkdir(exist_ok=True)
    print("✅ Data directories created")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit config/config.yaml with your settings")
    print("2. (Optional) Set up Google Sheets integration")
    print("3. Run: python src/main.py --once")
    print("\n📖 For detailed instructions, see README.md")
    
    if sys.platform == "win32":
        print(f"\n💡 To activate virtual environment: {venv_path}\\Scripts\\activate")
    else:
        print(f"\n💡 To activate virtual environment: source {venv_path}/bin/activate")
    
    return True

if __name__ == "__main__":
    success = setup_homeus()
    sys.exit(0 if success else 1) 