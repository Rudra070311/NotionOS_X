"""
NotionOS X: Autonomous Multi-Agent Operating System with Persistent Intelligence
Main entry point and demo executable.
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

from orchestrator import NotionOSXOrchestrator
from utils.logger import get_logger


async def main():
    """Main demo execution."""
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
    
    logger.info("SYSTEM", "Orchestrator initialized")
    
    # Demo task
    print("\n" + "-" * 80)
    print("DEMO: Processing Multi-Agent Task")
    print("-" * 80 + "\n")
    
    task_description = """
    Analyze emerging trends in AI and create a comprehensive report on their 
    practical applications, potential impacts, and strategic recommendations 
    for organizations.
    """
    
    print(f"📋 TASK: {task_description.strip()}\n")
    
    try:
        # Process the task through the multi-agent system
        result = await orchestrator.process_task(task_description.strip())
        
        # Display results
        print("\n" + "=" * 80)
        print("TASK EXECUTION COMPLETED")
        print("=" * 80 + "\n")
        
        print(f"Task ID: {result['task_id']}")
        print(f"Status: {result['status']}")
        print(f"Approved: {result['approved']}\n")
        
        print("CRITIC SCORES:")
        for critic_name, score in result['critic_scores'].items():
            bar_length = 40
            filled = int(bar_length * score)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"  {critic_name:20s} [{bar}] {score:.2%}")
        
        print("\nEXECUTION SUMMARY:")
        exec_summary = result['execution_summary']
        print(f"  Total Nodes: {exec_summary.get('total_nodes', 'N/A')}")
        print(f"  Completed: {exec_summary.get('completed', 'N/A')}")
        print(f"  Failed: {exec_summary.get('failed', 'N/A')}")
        print(f"  Duration: {exec_summary.get('total_execution_time', 0):.2f}s")
        
        # Print system status
        orchestrator.print_status()
        
        # Save detailed report
        report_path = Path("output") / f"task_report_{result['task_id']}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        logger.info(
            "SYSTEM",
            "Task execution completed successfully",
            {"task_id": result['task_id'], "report_path": str(report_path)}
        )
        
        print(f"📄 Detailed report saved to: {report_path}\n")
        
        return 0
    
    except Exception as e:
        logger.error("SYSTEM", f"Task execution failed: {str(e)}")
        print(f"\n❌ ERROR: {str(e)}\n")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
