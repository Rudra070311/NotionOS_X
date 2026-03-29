# NotionOS X - Production-Grade AI Operating System

An advanced, fully-functional multi-agent AI operating system that simulates autonomous
execution with persistent intelligence, memory systems, and human-in-the-loop governance.

## Features

### 1. Task Graph Engine (DAG)

- Converts natural language tasks into Directed Acyclic Graphs
- Supports sequential and parallel execution stages
- Validates for cycles and structural integrity
- Optimizes for efficient execution order

### 2. Multi-Agent System

- **Planner Agent**: Generates execution plans and DAGs
- **Executor Agent**: Executes tasks and manages tool calls
- **Researcher Agent**: Gathers external knowledge and context
- **Critic Agents** (3 variants):
  - Quality Critic: Evaluates correctness and completeness
  - Creativity Critic: Assesses novelty and innovation
  - Practicality Critic: Measures applicability and feasibility

### 3. Execution Engine

- Async execution with configurable parallelism
- Respects DAG dependencies automatically
- Handles failures gracefully
- Tracks execution metrics

### 4. Persistent Memory System

- **Episodic Memory**: Records past task executions
- **Feedback Memory**: Stores critic scores and improvements
- **Strategy Memory**: Maintains learned patterns and best practices
- All memory stored as JSON for inspection

### 5. Self-Improvement Loop

- Critic agents evaluate output
- Automatic refinement if scores below threshold
- Records improvements for future use
- Iterative enhancement

### 6. Tool Simulation

- **Browser Tool**: Web search and content fetching
- **File Tool**: Virtual file system operations
- **Code Tool**: Simulated code execution
- Extensible tool interface

### 7. Notion MCP Integration

- Fetch tasks from Notion database
- Update task status and outputs
- Human approval workflow
- Simulated Notion MCP client

### 8. Human Governance

- All final outputs require human approval
- Approval tracked in Notion
- Tasks stay in "Awaiting Approval" until approved
- Only approved tasks are finalized

### 9. Comprehensive Observability

- Structured logging with color output
- Agent decision tracking
- Execution metrics
- Event-based logging

## Architecture

```text
NotionOS_X/
├── main.py                 # Entry point and demo
├── orchestrator.py         # Central coordinator
├── task_graph.py          # DAG engine
├── execution_engine.py    # Async executor
├── config.py              # Configuration
│
├── agents/
│   ├── base_agent.py      # Abstract base class
│   ├── planner.py         # Planner agent
│   ├── executor.py        # Executor agent
│   ├── researcher.py      # Researcher agent
│   └── critic_agents.py   # Quality/Creativity/Practicality critics
│
├── memory/
│   └── memory_system.py   # Episodic, feedback, strategy memory
│
├── tools/
│   └── tools_interface.py # Browser, File, Code tools
│
├── notion/
│   └── notion_client.py   # Notion MCP client
│
├── utils/
│   └── logger.py          # Structured logging
│
└── output/
    └── task_reports_*.json # Generated reports
```

## How to Run

### Basic Execution
```bash
python main.py
```

### System Flow

1. **Task Input** → User provides task description
2. **Planning** → Planner agent generates DAG
3. **Research** → Researcher gathers context
4. **Execution** → Executor processes nodes in parallel
5. **Evaluation** → Critics score output from multiple dimensions
6. **Refinement** → If scores below threshold, refine iteratively
7. **Approval** → Request human approval via Notion
8. **Finalization** → Complete task only if approved
9. **Memory** → Record in episodic, feedback, and strategy memory

## Example Task Processing

Input:
```
"Analyze emerging trends in AI and create a comprehensive report on their 
practical applications, potential impacts, and strategic recommendations 
for organizations."
```

System Output:
- Task ID and status
- Execution DAG with 6 stages
- Research sources and context
- Critic scores on quality, creativity, practicality
- Refinement iterations if needed
- Human approval workflow
- Detailed JSON report

## Memory System

### Episodic Memory (episodic_memory.json)
- Stores all past task executions
- Includes: task ID, description, output, status, duration
- Searchable by keyword

### Feedback Memory (feedback_memory.json)
- Records critic evaluations
- Tracks improvements made
- Links feedback to task IDs

### Strategy Memory (strategy_memory.json)
- Stores successful strategies
- Patterns discovered
- Effectiveness metrics

## Configuration

Edit `config.py` to customize:
- Max parallel nodes
- Execution timeouts
- Critic thresholds
- Memory limits
- Tool settings

## Key Design Patterns

1. **Agent Pattern**: Autonomous decision-making agents
2. **DAG Pattern**: Explicit dependency management
3. **Memory Pattern**: Persistent learning
4. **Governance Pattern**: Human approval gates
5. **Tool Pattern**: Extensible tool interface
6. **Async Pattern**: Non-blocking execution

## Production Readiness

This implementation includes:
- ✅ Full async/await support
- ✅ Error handling and recovery
- ✅ Structured logging
- ✅ Agent decision tracking
- ✅ Memory persistence
- ✅ Notion integration
- ✅ Extensible architecture
- ✅ Comprehensive documentation

## Future Enhancements

1. Real LLM integration (OpenAI, Claude API)
2. Distributed execution across multiple machines
3. Real Notion API integration
4. Web UI for monitoring
5. Slack/Teams integration for approvals
6. Advanced scheduling and orchestration
7. A/B testing for strategy comparison
8. Cost tracking and optimization

## Notes

- All data is persisted to disk (memory/)
- Tool execution is simulated but extensible
- Notion integration is mocked for demo purposes
- Agents use mock reasoning (can swap for real LLM)
- Execution is fully async for high concurrency
- System is designed for 24/7 autonomous operation

---

Built as a demonstration of advanced AI systems architecture with multi-agent
coordination, persistent memory, and production-grade software engineering practices.
