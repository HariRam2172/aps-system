from db.database import notes_collection

class NotesTool:

    def get_notes(self):
        return list(notes_collection.find({}, {"_id": 0}))

    def check_note_exists(self, task: str):
        return list(notes_collection.find({"note": task}, {"_id": 0}))

    def create_note(self, task: str):
        note_data = {
            "note": task,
            "status": "saved"
        }
        notes_collection.insert_one(note_data)
        return note_data