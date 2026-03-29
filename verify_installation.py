"""
Install and test script for NotionOS X
Run: python verify_installation.py
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Verify Python version."""
    version = sys.version_info
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ⚠ Warning: Python 3.8+ recommended")
        return False
    return True

def check_directory_structure():
    """Verify directory structure."""
    base = Path(__file__).parent
    required_dirs = [
        "agents", "memory", "tools", "notion", "utils"
    ]
    
    for dir_name in required_dirs:
        dir_path = base / dir_name
        if dir_path.exists():
            print(f"✓ Directory: {dir_name}/")
        else:
            print(f"✗ Missing: {dir_name}/")
            return False
    return True

def check_required_files():
    """Verify all required Python files."""
    base = Path(__file__).parent
    required_files = [
        "main.py",
        "run_demo.py",
        "orchestrator.py",
        "task_graph.py",
        "execution_engine.py",
        "config.py",
        "agents/base_agent.py",
        "agents/planner.py",
        "agents/executor.py",
        "agents/researcher.py",
        "agents/critic_agents.py",
        "memory/memory_system.py",
        "tools/tools_interface.py",
        "notion/notion_client.py",
        "utils/logger.py",
    ]
    
    all_exist = True
    for file_name in required_files:
        file_path = base / file_name
        if file_path.exists():
            print(f"✓ File: {file_name}")
        else:
            print(f"✗ Missing: {file_name}")
            all_exist = False
    return all_exist

def check_imports():
    """Verify that imports work."""
    print("\nChecking imports...")
    try:
        # Add to path
        sys.path.insert(0, str(Path(__file__).parent))
        
        # Try importing core modules
        print("  Importing utils.logger...", end=" ")
        from utils.logger import get_logger
        print("✓")
        
        print("  Importing task_graph...", end=" ")
        from task_graph import TaskGraph, TaskGraphBuilder
        print("✓")
        
        print("  Importing tools...", end=" ")
        from tools.tools_interface import ToolManager
        print("✓")
        
        print("  Importing agents...", end=" ")
        from agents.base_agent import BaseAgent
        from agents.planner import PlannerAgent
        print("✓")
        
        print("  Importing memory...", end=" ")
        from memory.memory_system import MemorySystem
        print("✓")
        
        print("  Importing notion...", end=" ")
        from notion.notion_client import NotionClient
        print("✓")
        
        print("  Importing orchestrator...", end=" ")
        from orchestrator import NotionOSXOrchestrator
        print("✓")
        
        return True
    except Exception as e:
        print(f"\n✗ Import failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("NotionOS X - Installation Verification")
    print("=" * 60 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Directory Structure", check_directory_structure),
        ("Required Files", check_required_files),
        ("Module Imports", check_imports),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        print("-" * 40)
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            results.append((check_name, False))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for check_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {check_name}")
        if not result:
            all_passed = False
    
    print("=" * 60 + "\n")
    
    if all_passed:
        print("✓ Installation verified successfully!")
        print("\nNext steps:")
        print("  python run_demo.py          # Run multi-task demo")
        print("  python main.py              # Run single-task demo")
        print("  cat QUICKSTART.md           # Read quick start guide")
        return 0
    else:
        print("✗ Installation verification failed!")
        print("Please check the errors above and fix them.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
