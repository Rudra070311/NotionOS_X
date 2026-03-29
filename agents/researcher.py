import time
from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent, AgentDecision
from tools.tools_interface import ToolManager

class ResearcherAgent(BaseAgent):

    def __init__(self, tool_manager: Optional[ToolManager] = None):
        super().__init__(
            name="Researcher",
            role="Information Gathering and Context Analysis"
        )
        self.tool_manager = tool_manager or ToolManager()
        self.research_conducted = []

    async def execute(self, input_data: Dict[str, Any],
                     context: Optional[Dict[str, Any]] = None) -> AgentDecision:
        start_time = time.time()

        task_description = input_data.get("task_description", "")
        query = input_data.get("research_query", task_description)

        try:
            search_result = await self.tool_manager.browser.search(
                query=query,
                num_results=5
            )

            research_data = {
                "query": query,
                "search_success": search_result.success,
                "results_count": 0,
                "sources": []
            }

            if search_result.success:
                results = search_result.data.get("results", [])
                research_data["results_count"] = len(results)

                for result in results[:3]:
                    fetch_result = await self.tool_manager.browser.fetch_content(
                        url=result.get("url", "")
                    )

                    if fetch_result.success:
                        research_data["sources"].append({
                            "title": result.get("title", ""),
                            "url": result.get("url", ""),
                            "preview": result.get("snippet", "")[:100],
                        })

            self.research_conducted.append({
                "query": query,
                "data": research_data
            })

            reasoning = f"Researched topic: '{query[:40]}...'. "
            reasoning += f"Found {research_data['results_count']} relevant sources. "
            reasoning += f"Extracted knowledge for {len(research_data['sources'])} sources."

            decision_data = {
                "query": query,
                "research_data": research_data,
            }

            execution_time = time.time() - start_time
            decision = AgentDecision(
                agent_name=self.name,
                decision="RESEARCH_COMPLETE",
                reasoning=reasoning,
                confidence=0.85,
                execution_time=execution_time,
                data=decision_data
            )

            self.record_decision(decision)
            self.execution_count += 1

            return decision

        except Exception as e:
            execution_time = time.time() - start_time
            error_decision = AgentDecision(
                agent_name=self.name,
                decision="RESEARCH_FAILED",
                reasoning=f"Research failed: {str(e)}",
                confidence=0.0,
                execution_time=execution_time,
            )
            self.record_decision(error_decision)
            self.execution_count += 1

            return error_decision
