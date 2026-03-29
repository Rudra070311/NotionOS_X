# Quick Start Guide for NotionOS X

## Installation

1. Navigate to NotionOS_X directory:
   cd NotionOS_X

2. No external dependencies required! Uses only Python standard library.
   (All components are simulated for demo purposes)

## Running the System

### Option 1: Run demo with multiple tasks

```bash
python run_demo.py
```

### Option 2: Run main with single task

```bash
python main.py
```

### Option 3: Interactive usage in Python

```python
import asyncio
from orchestrator import NotionOSXOrchestrator

async def run():
    orchestrator = NotionOSXOrchestrator()
    result = await orchestrator.process_task("Your task here")
    print(result)

asyncio.run(run())
```

## System Output

All outputs are saved to:
- output/task_reports_*.json - Detailed task reports
- output/system_report_final.json - Final system status
- memory/episodic_memory.json - Historical tasks
- memory/feedback_memory.json - Critic scores
- memory/strategy_memory.json - Learned strategies
- logs/notionos_x.log - Detailed logs
- logs/events.json - Structured event log

## Understanding the Demo

The system will:

1. **Generate a DAG** - Convert your task into a structured execution graph
2. **Research** - Simulate searching for relevant information
3. **Execute** - Process the DAG nodes (some in parallel)
4. **Evaluate** - Run 3 critic agents to score the output
5. **Refine** - If scores are low, automatically improve
6. **Approve** - Request human approval (auto-approved in demo)
7. **Record** - Store everything in memory for learning

## Key Files

- main.py - Simple single-task demo
- run_demo.py - Multiple tasks demonstration
- orchestrator.py - Central coordinator
- task_graph.py - DAG engine
- execution_engine.py - Async executor
- agents/ - All agent implementations
- memory/ - Persistent storage
- tools/ - Tool interface
- notion/ - Notion integration
- utils/ - Utilities and logging

## Monitoring

During execution, watch for:

- [INFO] logs in color-coded format
- Agent decision messages
- Critic score outputs (0-100%)
- Memory usage summaries
- Execution timings

## Customization

Edit `config.py` to:
- Adjust parallel execution limits
- Change critic score thresholds
- Set timeout values
- Modify memory settings

## Architecture Highlights

✓ Fully async/await Python 3.8+
✓ Structured logging
✓ DAG-based execution
✓ Multi-agent decision making
✓ Persistent memory system
✓ Self-improvement loops
✓ Human governance gates
✓ Tool extensibility
✓ No external dependencies required

## Performance Expectations

- Task processing: 5-15 seconds (simulated)
- Memory persistence: Instant
- DAG generation: <100ms
- Critic evaluation: ~1 second per critic
- Full pipeline: 30-60 seconds depending on complexity

## Troubleshooting

Q: Import errors?
A: Ensure you're running from NotionOS_X directory
   Use: python -m run_demo (if in parent directory)

Q: File not found?
A: Check that all files are in the correct subdirectories
   Verify directory structure matches the architecture diagram

Q: Slow execution?
A: Normal - includes simulated delays for realistic behavior
   Adjust delays in tools_interface.py if needed

## Next Steps

See README.md for:
- Full system architecture
- Component descriptions
- Design patterns used
- Future enhancement ideas

---

Happy autonomous AI systems building! 🚀
"""
