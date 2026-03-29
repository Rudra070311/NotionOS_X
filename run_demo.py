"""
Enhanced main with improved imports and demonstration.
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator import NotionOSXOrchestrator
from utils.logger import get_logger


async def demo_system_capabilities():
    """Demonstrate NotionOS X capabilities."""
    logger = get_logger()
    
    # Print banner
    print("\n" + "=" * 80)
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "NotionOS X: Autonomous Multi-Agent Operating System".center(78) + "║")
    print("║" + "with Persistent Intelligence".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print("=" * 80 + "\n")
    
    logger.info(
        "SYSTEM",
        "NotionOS X Initializing",
        {"version": "1.0", "timestamp": datetime.now().isoformat()}
    )
    
    # Initialize orchestrator
    orchestrator = NotionOSXOrchestrator()
    
    logger.info("SYSTEM", "Orchestrator initialized with all subsystems")
    print("\n✓ System initialized successfully\n")
    
    # Demo 1: Simple task
    print("\n" + "-" * 80)
    print("DEMO 1: Basic Task Processing")
    print("-" * 80 + "\n")
    
    task1 = "Analyze current market trends in machine learning and create a summary report."
    
    print(f"📋 TASK: {task1}\n")
    
    try:
        result1 = await orchestrator.process_task(task1)
        
        print("\n✓ Task completed successfully\n")
        print(f"  Status: {result1['status']}")
        print(f"  Approved: {result1['approved']}")
        
        print("\n  Critic Scores:")
        for critic_name, score in result1['critic_scores'].items():
            bar_length = 30
            filled = int(bar_length * score)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"    {critic_name:20s} [{bar}] {score:.1%}")
        
    except Exception as e:
        logger.error("DEMO", f"Task 1 failed: {str(e)}")
        print(f"\n✗ Task failed: {str(e)}\n")
    
    # Demo 2: Complex task
    print("\n" + "-" * 80)
    print("DEMO 2: Complex Multi-Step Task")
    print("-" * 80 + "\n")
    
    task2 = """Create a comprehensive business case for AI implementation in enterprise software,
               including risk analysis, cost-benefit assessment, and implementation roadmap."""
    
    print(f"📋 TASK: {task2}\n")
    
    try:
        result2 = await orchestrator.process_task(task2)
        
        print("\n✓ Task completed successfully\n")
        print(f"  Status: {result2['status']}")
        print(f"  Approved: {result2['approved']}")
        
        exec_summary = result2['execution_summary']
        print(f"\n  Execution Metrics:")
        print(f"    Total Nodes: {exec_summary.get('total_nodes', 'N/A')}")
        print(f"    Completed: {exec_summary.get('completed', 'N/A')}")
        print(f"    Duration: {exec_summary.get('total_execution_time', 0):.2f}s")
        
    except Exception as e:
        logger.error("DEMO", f"Task 2 failed: {str(e)}")
        print(f"\n✗ Task failed: {str(e)}\n")
    
    # Print final system status
    print("\n" + "=" * 80)
    orchestrator.print_status()
    
    # Save final report
    final_report = {
        "timestamp": datetime.now().isoformat(),
        "system_status": orchestrator.get_system_status(),
        "memory_summary": orchestrator.memory_system.get_summary(),
    }
    
    report_path = Path("output") / "system_report_final.json"
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(final_report, f, indent=2, default=str)
    
    logger.info("DEMO", f"System report saved to {report_path}")
    print(f"\n📄 System report saved to: {report_path}\n")
    
    # Save event logs
    logger.save_events_log()
    print(f"📊 Event logs saved to: logs/events.json\n")


async def main():
    """Main entry point."""
    try:
        await demo_system_capabilities()
        print("\n✓ Demo completed successfully!\n")
        return 0
    
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted by user\n")
        return 130
    
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
