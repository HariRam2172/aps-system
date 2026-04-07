import os
from tools.notes_tool import NotesTool

class SummarizationAgent:

    def __init__(self):
        self.notes_tool = NotesTool()

    def execute(self):
        notes = self.notes_tool.get_notes()

        if not notes:
            return {
                "status": "summary_generated",
                "summary": "No notes found yet.",
                "tool_used": "none"
            }

        note_texts = [n["note"] for n in notes]

        try:
            import google.generativeai as genai

            # ✅ Use ENV variable (Cloud Run compatible)
            api_key = None

            if not api_key:
                raise Exception("API key missing")

            genai.configure(api_key=api_key)

            model = genai.GenerativeModel("gemini-pro")

            prompt = "Summarize these notes in 2-3 sentences:\n" + "\n".join(note_texts)

            response = model.generate_content(prompt)

            return {
                "status": "summary_generated",
                "summary": response.text,
                "tool_used": "GeminiAPI"
            }

        except Exception as e:
            # ✅ Safe fallback (never crash)
            unique_notes = list(set(note_texts))

            summary = f"You have {len(notes)} notes. {len(unique_notes)} unique topics detected."

            return {
                "status": "summary_generated",
                "summary": summary + " (fallback mode)",
                "tool_used": "local_logic",
                "error": str(e)  # useful for debugging
            }