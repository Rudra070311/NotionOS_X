import json
import time
import random
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ToolResult:
    success: bool
    data: Any
    error: Optional[str] = None
    execution_time: float = 0.0

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "execution_time": self.execution_time,
        }

class BrowserTool:

    def __init__(self):
        self.search_results_cache = {}

    async def search(self, query: str, num_results: int = 5) -> ToolResult:
        start_time = time.time()

        try:
            await self._simulate_delay(0.5, 1.5)

            results = []
            keywords = query.split()

            for i in range(num_results):
                result = {
                    "title": f"Result: {' '.join(keywords)} - Article {i+1}",
                    "url": f"https://example.com/result-{i+1}",
                    "snippet": f"This is a synthetic result about {query}. "
                              f"Contains relevant information and details.",
                    "rank": i + 1
                }
                results.append(result)

            execution_time = time.time() - start_time
            return ToolResult(
                success=True,
                data={"query": query, "results": results, "count": len(results)},
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return ToolResult(
                success=False,
                data=None,
                error=str(e),
                execution_time=execution_time
            )

    async def fetch_content(self, url: str) -> ToolResult:
        start_time = time.time()

        try:
            await self._simulate_delay(0.3, 1.0)

            content = f"Fetched content from {url}:\n\n"
            content += "This is simulated page content with rich information about the topic. "
            content += "Contains multiple paragraphs, sections, and relevant data."

            execution_time = time.time() - start_time
            return ToolResult(
                success=True,
                data={"url": url, "content": content, "status": 200},
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return ToolResult(
                success=False,
                data=None,
                error=str(e),
                execution_time=execution_time
            )

    @staticmethod
    async def _simulate_delay(min_delay: float, max_delay: float):
        import asyncio
        delay = random.uniform(min_delay, max_delay)
        await asyncio.sleep(delay)

class FileTool:

    def __init__(self):
        self.virtual_filesystem: Dict[str, str] = {}

    async def write(self, filepath: str, content: str) -> ToolResult:
        start_time = time.time()

        try:
            await self._simulate_delay(0.1, 0.3)

            self.virtual_filesystem[filepath] = content

            execution_time = time.time() - start_time
            return ToolResult(
                success=True,
                data={
                    "filepath": filepath,
                    "size": len(content),
                    "status": "written"
                },
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return ToolResult(
                success=False,
                data=None,
                error=str(e),
                execution_time=execution_time
            )

    async def read(self, filepath: str) -> ToolResult:
        start_time = time.time()

        try:
            await self._simulate_delay(0.05, 0.2)

            if filepath not in self.virtual_filesystem:
                raise FileNotFoundError(f"File {filepath} not found")

            content = self.virtual_filesystem[filepath]

            execution_time = time.time() - start_time
            return ToolResult(
                success=True,
                data={
                    "filepath": filepath,
                    "content": content,
                    "size": len(content)
                },
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return ToolResult(
                success=False,
                data=None,
                error=str(e),
                execution_time=execution_time
            )

    @staticmethod
    async def _simulate_delay(min_delay: float, max_delay: float):
        import asyncio
        delay = random.uniform(min_delay, max_delay)
        await asyncio.sleep(delay)

class CodeTool:

    def __init__(self):
        self.execution_history: List[Dict] = []

    async def run(self, code: str, language: str = "python") -> ToolResult:
        start_time = time.time()

        try:
            await self._simulate_delay(0.5, 2.0)

            output = self._simulate_execution(code, language)

            execution_time = time.time() - start_time

            execution_record = {
                "code": code,
                "language": language,
                "output": output,
                "status": "success",
                "execution_time": execution_time
            }
            self.execution_history.append(execution_record)

            return ToolResult(
                success=True,
                data={
                    "language": language,
                    "code": code,
                    "output": output,
                    "status": "executed"
                },
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return ToolResult(
                success=False,
                data=None,
                error=str(e),
                execution_time=execution_time
            )

    @staticmethod
    def _simulate_execution(code: str, language: str) -> str:
        if "print" in code:
            return "Hello from simulated execution\nFunction returned successfully"
        if "calculate" in code.lower():
            return "Calculation result: 42"
        if "query" in code.lower():
            return json.dumps({"results": [1, 2, 3], "status": "success"})
        return f"Executed {language} code successfully"

    @staticmethod
    async def _simulate_delay(min_delay: float, max_delay: float):
        import asyncio
        delay = random.uniform(min_delay, max_delay)
        await asyncio.sleep(delay)

class ToolManager:

    def __init__(self):
        self.browser = BrowserTool()
        self.file = FileTool()
        self.code = CodeTool()

    async def execute_tool(self, tool: str, method: str,
                          **kwargs) -> ToolResult:
        try:
            if tool == "browser":
                if method == "search":
                    return await self.browser.search(**kwargs)
                elif method == "fetch":
                    return await self.browser.fetch_content(**kwargs)

            elif tool == "file":
                if method == "write":
                    return await self.file.write(**kwargs)
                elif method == "read":
                    return await self.file.read(**kwargs)

            elif tool == "code":
                if method == "run":
                    return await self.code.run(**kwargs)

            return ToolResult(
                success=False,
                data=None,
                error=f"Unknown tool/method: {tool}/{method}"
            )

        except Exception as e:
            return ToolResult(
                success=False,
                data=None,
                error=str(e)
            )
