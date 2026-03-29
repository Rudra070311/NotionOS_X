import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    TODO = "Todo"
    IN_PROGRESS = "In Progress"
    PLANNING = "Planning"
    REVIEWING = "Reviewing"
    APPROVED = "Approved"
    EXECUTING = "Executing"
    COMPLETED = "Completed"
    FAILED = "Failed"
    AWAITING_APPROVAL = "Awaiting Approval"


class ApprovalStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    NEEDS_REVISION = "Needs Revision"


@dataclass
class NotionTask:
    task_id: str
    name: str
    description: str
    status: TaskStatus = TaskStatus.TODO
    approved: ApprovalStatus = ApprovalStatus.PENDING
    output: Optional[str] = None
    logs: List[str] = None
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if self.logs is None:
            self.logs = []
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


class NotionClient:
    
    def __init__(self, token: Optional[str] = None, simulate: bool = True):
        self.token = token
        self.simulate = simulate
        self.local_db = {}  # Local simulation of Notion database
        logger.info(f"🔗 [Notion] Initialized (simulate={simulate})")
    
    def fetch_tasks(self, filter_status: Optional[str] = None) -> List[NotionTask]:
        logger.info("📋 [Notion] Fetching tasks...")
        
        if self.simulate:
            return self._simulate_fetch_tasks(filter_status)
        
        # Real Notion API call would go here
        return []
    
    def fetch_task(self, task_id: str) -> Optional[NotionTask]:
        logger.info(f"📋 [Notion] Fetching task: {task_id}")
        
        if self.simulate:

            return NotionTask(
                task_id=task_id,
                name="Generate AI Dataset Pipeline",
                description="Create a complete data processing pipeline with validation",
                status=TaskStatus.TODO,
                approved=ApprovalStatus.PENDING
            )
        
        return None
    
    def create_task(self, task: NotionTask) -> str:
        logger.info(f"📝 [Notion] Creating task: {task.name}")
        
        if self.simulate:
            task_id = f"notion_{hash(task.name) % 100000}"
            self.local_db[task_id] = task
            return task_id
        
        return ""
    
    def update_task_status(self, task_id: str, status: TaskStatus, 
                          log_entry: Optional[str] = None) -> bool:
        logger.info(f"🔄 [Notion] Updating task {task_id}: {status.value}")
        
        if self.simulate:
            if task_id in self.local_db:
                self.local_db[task_id].status = status
                if log_entry:
                    self.local_db[task_id].logs.append(log_entry)
                self.local_db[task_id].updated_at = datetime.now().isoformat()
                return True
        
        return True
    
    def update_task_output(self, task_id: str, output: Dict, 
                          execution_trace: Optional[List] = None) -> bool:
        logger.info(f"💾 [Notion] Updating output for task {task_id}")
        
        if self.simulate:
            if task_id in self.local_db:
                self.local_db[task_id].output = json.dumps(output)
                if execution_trace:
                    for event in execution_trace:
                        self.local_db[task_id].logs.append(json.dumps(event))
                return True
        
        return True
    
    def update_approval_status(self, task_id: str, approved: ApprovalStatus) -> bool:
        logger.info(f"✅ [Notion] Setting approval status: {approved.value}")
        
        if self.simulate:
            if task_id in self.local_db:
                self.local_db[task_id].approved = approved
                return True
        
        return True
    
    def get_approval_status(self, task_id: str) -> ApprovalStatus:
        if self.simulate:
            if task_id in self.local_db:
                return self.local_db[task_id].approved
            return ApprovalStatus.PENDING
        
        return ApprovalStatus.PENDING
    
    def finalize_task(self, task_id: str, final_output: Dict) -> bool:
        logger.info(f"🏁 [Notion] Finalizing task {task_id}")
        
        if self.get_approval_status(task_id) != ApprovalStatus.APPROVED:
            logger.warning(f"⚠️ Task {task_id} not approved, cannot finalize")
            return False
        
        if self.simulate:
            self.update_task_status(task_id, TaskStatus.COMPLETED)
            self.update_task_output(task_id, final_output)
            return True
        
        return True
    
    def add_log_entry(self, task_id: str, entry: str) -> bool:
        if self.simulate:
            if task_id in self.local_db:
                self.local_db[task_id].logs.append(entry)
                return True
        
        return True
    
    def sync_execution_state(self, task_id: str, execution_state: Dict) -> bool:
        logger.info(f"🔄 [Notion] Syncing execution state for {task_id}")
        

        progress = execution_state.get("progress", {})
        stage = execution_state.get("stage", "unknown")
        
        log_entry = f"[{stage.upper()}] {progress}"
        
        return self.add_log_entry(task_id, log_entry)
    
    def _simulate_fetch_tasks(self, filter_status: Optional[str] = None) -> List[NotionTask]:
        tasks = [
            NotionTask(
                task_id="task_001",
                name="Generate AI Dataset Pipeline",
                description="Create end-to-end data processing with validation",
                status=TaskStatus.TODO,
                approved=ApprovalStatus.PENDING
            ),
            NotionTask(
                task_id="task_002",
                name="Optimize Model Inference",
                description="Reduce inference latency by 50%",
                status=TaskStatus.TODO,
                approved=ApprovalStatus.PENDING
            ),
            NotionTask(
                task_id="task_003",
                name="Document API Endpoints",
                description="Generate comprehensive API documentation",
                status=TaskStatus.TODO,
                approved=ApprovalStatus.PENDING
            )
        ]
        
        if filter_status:
            tasks = [t for t in tasks if t.status.value == filter_status]
        
        return tasks
    
    def export_database_snapshot(self) -> Dict:
        logger.info("📦 [Notion] Exporting database snapshot...")
        
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "task_count": len(self.local_db),
            "tasks": {
                task_id: {
                    "name": task.name,
                    "status": task.status.value,
                    "approved": task.approved.value,
                    "created_at": task.created_at,
                    "updated_at": task.updated_at
                }
                for task_id, task in self.local_db.items()
            }
        }
        
        return snapshot
    
    def search_tasks(self, query: str) -> List[NotionTask]:
        logger.info(f"🔍 [Notion] Searching for: {query}")
        
        results = []
        query_lower = query.lower()
        
        for task in self.local_db.values():
            if (query_lower in task.name.lower() or 
                query_lower in task.description.lower()):
                results.append(task)
        
        return results


class NotionGovernanceEngine:
    
    def __init__(self, notion_client: NotionClient):
        self.notion = notion_client
        self.governance_log = []
    
    def check_approval_gate(self, task_id: str) -> bool:
        approval = self.notion.get_approval_status(task_id)
        
        if approval == ApprovalStatus.APPROVED:
            self._log_governance_event(task_id, "APPROVED", "Proceeding with execution")
            return True
        elif approval == ApprovalStatus.REJECTED:
            self._log_governance_event(task_id, "REJECTED", "Task rejected, stopping execution")
            return False
        else:
            self._log_governance_event(task_id, "PENDING", "Awaiting human approval")
            return False
    
    def request_approval(self, task_id: str, dag: Dict, estimated_resource_usage: Dict) -> str:
        logger.info(f"🙋 [Governance] Requesting approval for task {task_id}")
        
        approval_request = {
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "nodes": len(dag.get("nodes", {})),
            "estimated_duration_ms": dag.get("estimated_total_duration_ms", 0),
            "estimated_resources": estimated_resource_usage,
            "status": "AWAITING_APPROVAL"
        }
        
        status_msg = (
            f"⏳ Task {task_id} awaiting human approval in Notion\n"
            f"   Nodes: {approval_request['nodes']}\n"
            f"   Est. Duration: {approval_request['estimated_duration_ms']}ms"
        )
        
        self.notion.update_task_status(
            task_id,
            TaskStatus.AWAITING_APPROVAL,
            f"Awaiting approval - {approval_request['nodes']} nodes, "
            f"{approval_request['estimated_duration_ms']}ms"
        )
        
        return status_msg
    
    def notify_execution_milestone(self, task_id: str, milestone: str, 
                                   status: str = "ON_TRACK") -> None:
        logger.info(f"📍 [Governance] Milestone: {milestone}")
        
        self.notion.add_log_entry(
            task_id,
            f"MILESTONE: {milestone} (Status: {status})"
        )
        
        self._log_governance_event(task_id, "MILESTONE", milestone)
    
    def handle_execution_failure(self, task_id: str, error: str, 
                                recovery_plan: Optional[str] = None) -> None:
        logger.error(f"❌ [Governance] Execution failure: {error}")
        
        self.notion.update_task_status(
            task_id,
            TaskStatus.FAILED,
            f"Failed: {error}"
        )
        
        if recovery_plan:
            self.notion.add_log_entry(task_id, f"Recovery Plan: {recovery_plan}")
        
        self._log_governance_event(task_id, "FAILURE", error)
    
    def finalize_and_archive(self, task_id: str, final_output: Dict) -> bool:
        logger.info(f"📦 [Governance] Finalizing task {task_id}")
        
        if not self.check_approval_gate(task_id):
            logger.warning("Cannot finalize - not approved")
            return False
        
        success = self.notion.finalize_task(task_id, final_output)
        
        if success:
            self._log_governance_event(
                task_id,
                "FINALIZED",
                "Task successfully completed and archived"
            )
        
        return success
    
    def _log_governance_event(self, task_id: str, event_type: str, details: str) -> None:
        event = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
            "event_type": event_type,
            "details": details
        }
        
        self.governance_log.append(event)
    
    def get_governance_log(self) -> List[Dict]:
        return self.governance_log
