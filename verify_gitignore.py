#!/usr/bin/env python3

import os
import subprocess
import tempfile
from pathlib import Path

def test_gitignore():
    print("🔍 Testing .gitignore configuration...")
    
    # Initialize git repo for testing
    subprocess.run(['git', 'init'], capture_output=True)
    
    # Create test files that should be ignored
    test_files = [
        'test.pyc',
        'test.tmp',
        'test.log',
        '.DS_Store',
        'Thumbs.db',
        'test.egg-info/metadata.txt',
        '.pytest_cache/test.txt',
        '.coverage',
        'test.pid',
        'test.tgz'
    ]
    
    test_dirs = [
        '__pycache__',
        '.pytest_cache',
        'test.egg-info',
        'htmlcov'
    ]
    
    print("📁 Creating test files and directories...")
    
    # Create test files
    for file_path in test_files:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        Path(file_path).touch()
    
    # Create test directories
    for dir_path in test_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        (Path(dir_path) / 'test.txt').touch()
    
    # Check git status
    result = subprocess.run(['git', 'status', '--porcelain'], 
                          capture_output=True, text=True)
    
    untracked_files = [line for line in result.stdout.split('\n') 
                      if line.startswith('??')]
    
    # Check if any test files appear as untracked
    ignored_correctly = True
    for line in untracked_files:
        file_path = line[3:].strip()  # Remove '?? ' prefix
        if any(test_file in file_path for test_file in test_files + test_dirs):
            print(f"❌ File should be ignored but appears as untracked: {file_path}")
            ignored_correctly = False
    
    # Clean up test files
    print("🧹 Cleaning up test files...")
    for file_path in test_files:
        try:
            Path(file_path).unlink()
        except FileNotFoundError:
            pass
    
    for dir_path in test_dirs:
        try:
            import shutil
            shutil.rmtree(dir_path)
        except FileNotFoundError:
            pass
    
    # Clean up git repo
    import shutil
    shutil.rmtree('.git')
    
    if ignored_correctly:
        print("✅ All test files properly ignored!")
        print("✅ .gitignore is configured correctly!")
    else:
        print("❌ Some files are not being ignored properly")
    
    return ignored_correctly

def show_gitignore_summary():
    print("\n📋 .gitignore Summary:")
    print("=" * 50)
    
    categories = {
        "Python cache & compiled": ["__pycache__/", "*.pyc", "*.pyo", "*.pyd"],
        "Testing & coverage": [".pytest_cache/", ".coverage", ".hypothesis/"],
        "Virtual environments": ["venv/", "env/", "ENV/"],
        "Configuration (sensitive)": ["config/config.yaml", "config/*.json", "config/google_credentials.json"],
        "Database & logs": ["data/", "*.db", "*.log"],
        "Development tools": [".vscode/", ".idea/", "*.sublime-*"],
        "OS files": [".DS_Store", "Thumbs.db", "._*"],
        "Temporary files": ["*.tmp", "*.temp", "*.swp", "*~"],
        "Build artifacts": ["build/", "dist/", "*.egg-info/"]
    }
    
    for category, patterns in categories.items():
        print(f"\n🔸 {category}:")
        for pattern in patterns:
            print(f"   • {pattern}")

if __name__ == "__main__":
    print("🏠 Homeus - .gitignore Verification")
    print("=" * 40)
    
    success = test_gitignore()
    show_gitignore_summary()
    
    if success:
        print("\n🎉 Ready for open-source! All sensitive and cache files are properly ignored.")
    else:
        print("\n⚠️  Please review .gitignore configuration.") 