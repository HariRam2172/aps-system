from db.database import events_collection

class CalendarTool:

    def get_events(self):
        return list(events_collection.find({}, {"_id": 0}))

    def check_event_exists(self, task: str):
        return list(events_collection.find({"event": task}, {"_id": 0}))

    def create_event(self, task: str):
        event_data = {
            "event": task,
            "status": "scheduled"
        }
        events_collection.insert_one(event_data)
        return event_data