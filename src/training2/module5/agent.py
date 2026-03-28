import json
import os
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import DefaultAzureCredential


def _agent_reference(agent_name: str) -> dict[str, str]:
    return {"name": agent_name, "type": "agent_reference"}


def _extract_json(text: str) -> dict[str, Any]:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw_response": text.strip()}


def _ask_agent(openai_client: Any, agent: Any, prompt: str) -> str:
    conversation = openai_client.conversations.create()
    openai_client.conversations.items.create(
        conversation_id=conversation.id,
        items=[{"type": "message", "role": "user", "content": prompt}],
    )

    response = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent_reference": _agent_reference(agent.name)},
    )

    if response.status == "failed":
        raise RuntimeError(f"Agent '{agent.name}' failed: {response.error}")

    return response.output_text.strip()


def _print_specialist_result(agent_label: str, text: str) -> None:
    print(f"\n{agent_label}:\n{text}")


def main() -> None:
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT")

    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
        project_client.get_openai_client() as openai_client,
    ):
        priority_agent = project_client.agents.create_version(
            agent_name="ticket-priority-agent",
            definition=PromptAgentDefinition(
                model=model_deployment,
                instructions="""
You assess how urgent an IT support ticket is.

Return valid JSON with this schema:
{
  "priority": "High|Medium|Low",
  "reason": "short explanation"
}

Decision rules:
- High: production outage, security issue, customer-facing failure, or blocked revenue work
- Medium: important issue with workaround or time sensitivity
- Low: cosmetic, informational, or non-urgent task

Return JSON only.
""".strip(),
            ),
        )

        team_agent = project_client.agents.create_version(
            agent_name="ticket-team-agent",
            definition=PromptAgentDefinition(
                model=model_deployment,
                instructions="""
You assign IT support tickets to the best owning team.

Available teams:
- Frontend
- Backend
- Infrastructure
- Security
- Data

Return valid JSON with this schema:
{
  "team": "one team from the list",
  "reason": "short explanation"
}

Return JSON only.
""".strip(),
            ),
        )

        effort_agent = project_client.agents.create_version(
            agent_name="ticket-effort-agent",
            definition=PromptAgentDefinition(
                model=model_deployment,
                instructions="""
You estimate delivery effort for an IT support ticket.

Return valid JSON with this schema:
{
  "effort": "Small|Medium|Large",
  "reason": "short explanation"
}

Scale:
- Small: less than 1 day
- Medium: 1 to 3 days
- Large: more than 3 days, risky, or cross-team

Return JSON only.
""".strip(),
            ),
        )

        triage_agent = project_client.agents.create_version(
            agent_name="ticket-triage-agent",
            definition=PromptAgentDefinition(
                model=model_deployment,
                instructions="""
You are the lead triage agent for incoming support tickets.
You receive the original ticket plus specialist findings for priority,
ownership, and effort. Produce a clean final triage decision.

Return valid JSON with this schema:
{
  "summary": "one sentence summary of the issue",
  "priority": "High|Medium|Low",
  "assigned_team": "team name",
  "effort": "Small|Medium|Large",
  "recommended_next_step": "short actionable next step"
}

Use the specialist findings unless they clearly conflict with the ticket text.
Return JSON only.
""".strip(),
            ),
        )

        created_agents = [triage_agent, priority_agent, team_agent, effort_agent]

        try:
            while True:
                ticket = input(
                    "Enter a support ticket description. Use 'quit' to exit.\nUSER: "
                ).strip()
                if ticket.lower() == "quit":
                    print("Exiting chat.")
                    break
                if not ticket:
                    print("Please enter a ticket description.")
                    continue

                print("\nRunning specialist agents. Please wait.")

                priority_text = _ask_agent(
                    openai_client,
                    priority_agent,
                    f"Ticket:\n{ticket}",
                )
                team_text = _ask_agent(
                    openai_client,
                    team_agent,
                    f"Ticket:\n{ticket}",
                )
                effort_text = _ask_agent(
                    openai_client,
                    effort_agent,
                    f"Ticket:\n{ticket}",
                )

                _print_specialist_result("PRIORITY AGENT", priority_text)
                _print_specialist_result("TEAM AGENT", team_text)
                _print_specialist_result("EFFORT AGENT", effort_text)

                priority_data = _extract_json(priority_text)
                team_data = _extract_json(team_text)
                effort_data = _extract_json(effort_text)

                triage_prompt = json.dumps(
                    {
                        "ticket": ticket,
                        "specialist_findings": {
                            "priority_agent": priority_data,
                            "team_agent": team_data,
                            "effort_agent": effort_data,
                        },
                    },
                    indent=2,
                )

                triage_text = _ask_agent(openai_client, triage_agent, triage_prompt)
                triage_data = _extract_json(triage_text)

                print("\nTRIAGE AGENT:")
                print(json.dumps(triage_data, indent=2))

        finally:
            print("\nCleaning up agents:")
            for agent in created_agents:
                project_client.agents.delete_version(
                    agent_name=agent.name,
                    agent_version=agent.version,
                )
                print(f"Deleted {agent.name} version {agent.version}.")


if __name__ == "__main__":
    main()
