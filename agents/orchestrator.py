import re

class OrchestratorAgent:

    def process(self, user_input: str):
        text = user_input.lower()

        tasks = []

        # 🔥 SPLIT MULTI TASK
        parts = re.split(r'and', user_input)

        for part in parts:
            p = part.strip().lower()

            if "schedule" in p:
                tasks.append({"agent": "scheduling", "task": part.strip()})

            elif "note" in p:
                tasks.append({"agent": "notes", "task": part.strip()})

            elif "summarize" in p:
                tasks.append({"agent": "summarization", "task": part.strip()})

        if not tasks:
            tasks.append({"agent": "general", "task": user_input})

        return {
            "tasks": tasks,
            "reasoning": f"Detected {len(tasks)} task(s): {[t['agent'] for t in tasks]}",
            "input_analyzed": user_input
        }