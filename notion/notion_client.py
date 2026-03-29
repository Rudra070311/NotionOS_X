import json
import uuid
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class NotionTask:
    id: str
    title: str
    status: str
    approved: bool
    output: Optional[str] = None
    logs: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "approved": self.approved,
            "output": self.output,
            "logs": self.logs,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

class NotionClient:

    def __init__(self, api_key: str = "mock_api_key"):
        self.api_key = api_key
        self.database_id = "mock_database_id"

        self.tasks_db: Dict[str, NotionTask] = {}
        self._initialize_mock_data()

    def _initialize_mock_data(self):
        mock_task = NotionTask(
            id=str(uuid.uuid4()),
            title="Process and analyze dataset",
            status="Submitted",
            approved=False,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )
        self.tasks_db[mock_task.id] = mock_task

    async def fetch_tasks(self, status: str = "Submitted") -> List[NotionTask]:
        tasks = [
            task for task in self.tasks_db.values()
            if task.status == status
        ]
        return tasks

    async def fetch_task(self, task_id: str) -> Optional[NotionTask]:
        return self.tasks_db.get(task_id)

    async def update_task_status(self, task_id: str, status: str) -> bool:
        if task_id in self.tasks_db:
            self.tasks_db[task_id].status = status
            self.tasks_db[task_id].updated_at = datetime.now().isoformat()
            return True
        return False

    async def update_task_output(self, task_id: str, output: str,
                                logs: Optional[str] = None) -> bool:
        if task_id in self.tasks_db:
            self.tasks_db[task_id].output = output
            if logs:
                self.tasks_db[task_id].logs = logs
            self.tasks_db[task_id].updated_at = datetime.now().isoformat()
            return True
        return False

    async def set_task_approved(self, task_id: str, approved: bool) -> bool:
        if task_id in self.tasks_db:
            self.tasks_db[task_id].approved = approved
            self.tasks_db[task_id].updated_at = datetime.now().isoformat()
            return True
        return False

    async def create_task(self, title: str, description: str = "") -> NotionTask:
        task = NotionTask(
            id=str(uuid.uuid4()),
            title=title,
            status="Created",
            approved=False,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )
        self.tasks_db[task.id] = task
        return task

    def get_all_tasks(self) -> List[NotionTask]:
        return list(self.tasks_db.values())

    def get_task_summary(self) -> Dict[str, Any]:
        tasks = self.get_all_tasks()
        return {
            "total": len(tasks),
            "by_status": self._group_by_field(tasks, "status"),
            "approved_count": sum(1 for t in tasks if t.approved),
            "pending_approval": sum(1 for t in tasks if not t.approved),
        }

    @staticmethod
    def _group_by_field(tasks: List[NotionTask], field: str) -> Dict[str, int]:
        groups: Dict[str, int] = {}
        for task in tasks:
            value = getattr(task, field)
            groups[value] = groups.get(value, 0) + 1
        return groups

class NotionMCPAdapter:

    def __init__(self, notion_client: NotionClient):
        self.client = notion_client

    async def get_pending_tasks(self) -> List[Dict[str, Any]]:
        tasks = await self.client.fetch_tasks(status="Submitted")
        return [task.to_dict() for task in tasks]

    async def report_execution(self, task_id: str, status: str,
                               output: Any, logs: str):
        output_str = json.dumps(output) if isinstance(output, dict) else str(output)

        await self.client.update_task_status(task_id, status)
        await self.client.update_task_output(task_id, output_str, logs)

    async def request_approval(self, task_id: str,
                               output_summary: str) -> bool:
        task = await self.client.fetch_task(task_id)
        if task:
            print(f"\n{'='*60}")
            print(f"HUMAN APPROVAL REQUIRED")
            print(f"{'='*60}")
            print(f"Task: {task.title}")
            print(f"Output Summary: {output_summary}")
            print(f"{'='*60}")

            response = "APPROVED"

            if response == "APPROVED":
                await self.client.set_task_approved(task_id, True)
                await self.client.update_task_status(task_id, "Approved")
                return True
            else:
                await self.client.update_task_status(task_id, "Rejected")
                return False

        return False

    async def finalize_task(self, task_id: str) -> bool:
        task = await self.client.fetch_task(task_id)
        if task and task.approved:
            await self.client.update_task_status(task_id, "Completed")
            return True
        return False
