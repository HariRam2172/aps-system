from tools.notes_tool import NotesTool

class NotesAgent:

    def __init__(self):
        self.notes_tool = NotesTool()

    def execute(self, task: str):

        existing = self.notes_tool.check_note_exists(task)

        if existing:
            return {
                "status": "already_exists",
                "details": "Note already exists in DB",
                "previous_notes": existing
            }

        previous_notes = self.notes_tool.get_notes()

        self.notes_tool.create_note(task)

        return {
            "status": "note_created",
            "details": f"Note saved via NotesTool: {task}",
            "previous_notes": previous_notes
        }