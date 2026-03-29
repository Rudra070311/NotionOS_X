import asyncio
import json
import time
import logging
import sys
from typing import Dict, List


logger = logging.getLogger(__name__)


async def run_advanced_demo():
    print("\n" + "=" * 80)
    print("🚀 NotionOS X - ADVANCED DEMONSTRATION SCENARIO")
    print("=" * 80)
    
    sys.path.insert(0, '.')
    
    try:
        from orchestrator import Orchestrator
        from utils.dashboard import print_beautiful_banner, print_summary_report
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return
    
    print_beautiful_banner()
    
    # Initialize orchestrator
    print("\n⚙️ INITIALIZING NOTIONOS X...")
    orchestrator = Orchestrator()
    await orchestrator.initialize()
    
    print("\n✅ System initialized successfully\n")
    
    scenarios = [
        {
            "title": "Scenario 1: Data Processing Pipeline",
            "task": "Create a comprehensive data processing pipeline with validation,"
                   " error handling, and quality assurance checks",
            "complexity": "HIGH"
        },
        {
            "title": "Scenario 2: Model Optimization",
            "task": "Optimize machine learning model for inference latency"
                   " while maintaining accuracy thresholds",
            "complexity": "MEDIUM"
        },
        {
            "title": "Scenario 3: Documentation Generation",
            "task": "Generate comprehensive API documentation with examples,"
                   " usage patterns, and troubleshooting guides",
            "complexity": "MEDIUM"
        }
    ]
    
    completed_tasks = []
    failed_tasks = []
    
    for scenario in scenarios:
        print("\n" + "=" * 80)
        print(f"📌 {scenario['title']}")
        print("=" * 80)
        print(f"Task: {scenario['task']}")
        print(f"Complexity: {scenario['complexity']}")
        print("-" * 80)
        
        try:
            print("\n[1/7] FETCHING TASK FROM NOTION")
            tasks = orchestrator.notion.fetch_tasks()
            if tasks:
                notion_task = tasks[0]
                task_id = notion_task.task_id
                print(f"✅ Fetched task: {task_id}")
            else:
                print("⚠️ No tasks in Notion, creating simulation")
                task_id = f"task_{hash(scenario['task']) % 100000}"
            
            print("\n[2/7] GENERATING EXECUTION DAG")
            from agents.planner_v2 import PlannerV2
            
            planner = PlannerV2()
            dag_plan = planner.plan_task_advanced(scenario['task'], {"complexity": scenario['complexity']})
            
            print(f"✅ DAG Generated:")
            print(f"   Nodes: {len(dag_plan['nodes'])}")
            print(f"   Edges: {len(dag_plan['edges'])}")
            print(f"   Parallelization Factor: {dag_plan['parallelization_metadata']['levels']}")
            print(f"   Estimated Duration: {dag_plan['estimated_total_duration_ms']}ms")
            
            print("\n[3/7] REQUESTING HUMAN APPROVAL (via Notion)")
            approval_msg = orchestrator.governance.request_approval(
                task_id,
                dag_plan,
                {"estimated_compute": "moderate", "estimated_memory": "2GB"}
            )
            print(approval_msg)
            
            print("\n[4/7] AWAITING APPROVAL...")
            await asyncio.sleep(0.5)
            orchestrator.notion.update_approval_status(
                task_id,
                __import__('notion.advanced_client', fromlist=['ApprovalStatus']).ApprovalStatus.APPROVED
            )
            print("✅ Task approved!")
            
            print("\n[5/7] EXECUTING DAG")
            start_time = time.time()
            
            execution_result = {
                "task_id": task_id,
                "executed_nodes": len(dag_plan['nodes']),
                "tools_used": ["browser.search", "code.run", "file.write"],
                "results": {}
            }
            
            # Simulate node execution with logging
            print("   Executing nodes in parallel levels...")
            
            for i, node in enumerate(dag_plan['nodes'], 1):
                level = node.get("execution_level", 0)
                print(f"   ├─ Level {level}: {node['id'][:20]}... ({node['complexity']})")
                await asyncio.sleep(0.3)
            
            execution_time_ms = int((time.time() - start_time) * 1000)
            print(f"✅ Execution completed in {execution_time_ms}ms")
            
            execution_result["execution_time_ms"] = execution_time_ms
            execution_result["success"] = True
            
            print("\n[6/7] MULTI-DIMENSIONAL CRITIC EVALUATION")
            from agents.critics_ensemble import CriticEnsemble
            
            critics = CriticEnsemble()
            evaluation = critics.evaluate_result(
                execution_result,
                {"complexity": scenario['complexity']},
                []
            )
            
            print(f"   Individual Scores:")
            for critic_name, score in evaluation['individual_scores'].items():
                stars = "⭐" * int(score * 5)
                print(f"     {critic_name.title()}: {score:.2f}/1.00 {stars}")
            
            aggregate = evaluation['aggregate_score']
            print(f"\n   🎯 AGGREGATE SCORE: {aggregate:.2f}/1.00")
            
            if evaluation['needs_improvement']:
                print(f"   ⚠️ Score below threshold, improvements needed:")
                for rec in evaluation['recommendations'][:2]:
                    print(f"      • {rec}")
            else:
                print(f"   ✅ Excellent! No improvements needed")
            
            print("\n[7/7] STORING IN MEMORY & FINALIZING")
            
            memory_entry = {
                "task_id": task_id,
                "task_description": scenario['task'],
                "execution_time_ms": execution_time_ms,
                "success": True,
                "output_summary": f"Successfully executed with aggregate score {aggregate:.2f}",
                "scores": evaluation['individual_scores'],
                "dag": dag_plan,
                "tools_used": execution_result["tools_used"],
                "patterns": ["parallel_execution", "multi_critic_validation"]
            }
            
            exec_id = orchestrator.memory.store_execution(memory_entry)
            print(f"✅ Stored in memory: {exec_id}")
            
            # Finalize in Notion
            success = orchestrator.governance.finalize_and_archive(task_id, {
                "status": "completed",
                "score": aggregate,
                "execution_time_ms": execution_time_ms
            })
            
            if success:
                print(f"✅ Task finalized and archived")
                completed_tasks.append({
                    "task_id": task_id,
                    "score": aggregate,
                    "time_ms": execution_time_ms
                })
            else:
                print(f"⚠️ Could not finalize (not approved)")
        except Exception as e:
            print(f"\n❌ Scenario failed: {e}")
            failed_tasks.append(scenario['title'])
            continue
        
        await asyncio.sleep(1)
    
    print("\n" + "=" * 80)
    print("📊 ADVANCED DEMONSTRATION - FINAL SUMMARY")
    print("=" * 80)
    print(f"\n✅ Completed Tasks: {len(completed_tasks)}")
    for task in completed_tasks:
        print(f"   • {task['task_id']}: Score {task['score']:.2f}, Time {task['time_ms']}ms")
    
    if failed_tasks:
        print(f"\n❌ Failed Tasks: {len(failed_tasks)}")
        for task in failed_tasks:
            print(f"   • {task}")
    
    # Display system statistics
    stats = orchestrator.memory.get_execution_statistics()
    print(f"\n📈 SYSTEM STATISTICS")
    print(f"   Total Executions: {stats['total_executions']}")
    print(f"   Success Rate: {stats['success_rate']:.1%}")
    print(f"   Avg Quality: {stats['avg_quality_score']:.2f}")
    
    # Display improvement opportunities
    improvements = orchestrator.memory.get_improvement_opportunities()
    if improvements:
        print(f"\n💡 TOP IMPROVEMENTS")
        for imp in improvements[:2]:
            print(f"   • {imp['pattern']}: {imp['avg_effectiveness']:.1%} effective")
    
    # Display learned strategies
    strategies = orchestrator.memory.get_strategy_effectiveness()
    if strategies:
        print(f"\n🎓 LEARNED STRATEGIES")
        for strategy_name, data in list(strategies.items())[:2]:
            print(f"   • {strategy_name}: {data['success_rate']:.1%} success rate")
    
    # Display Notion snapshot
    print(f"\n📦 NOTION DATABASE SNAPSHOT")
    snapshot = orchestrator.notion.export_database_snapshot()
    print(f"   Tasks in DB: {snapshot['task_count']}")
    
    # Display governance audit trail
    governance_log = orchestrator.governance.get_governance_log()
    print(f"\n🔐 GOVERNANCE AUDIT TRAIL ({len(governance_log)} events)")
    for event in governance_log[-3:]:
        print(f"   {event['timestamp']}: {event['event_type']} - {event['details'][:40]}")
    
    print("\n" + "=" * 80)
    print("✅ ADVANCED DEMONSTRATION COMPLETE")
    print("=" * 80 + "\n")
    
    # Export complete memory
    memory_export = orchestrator.memory.export_memory_snapshot()
    
    print("📊 Memory System Export:")
    print(json.dumps(memory_export, indent=2)[:500] + "...\n")
    
    return orchestrator


if __name__ == "__main__":
    # Run the demonstration
    try:
        orchestrator = asyncio.run(run_advanced_demo())
        print("\n🎉 NotionOS X Ready for Interactive Dashboard")
        print("   Run 'python -i advanced_demo.py' to access dashboard")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
