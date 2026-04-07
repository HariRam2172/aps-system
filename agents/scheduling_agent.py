from tools.calendar_tool import CalendarTool

class SchedulingAgent:

    def __init__(self):
        self.calendar_tool = CalendarTool()

    def execute(self, task: str):

        # 🔍 Check duplicate via TOOL
        existing = self.calendar_tool.check_event_exists(task)

        if existing:
            return {
                "status": "already_exists",
                "details": "Event already exists in DB",
                "previous_events": existing
            }

        # 📥 Get history
        previous_events = self.calendar_tool.get_events()

        # 💾 Create event via TOOL
        self.calendar_tool.create_event(task)

        return {
            "status": "scheduled",
            "details": f"Event stored via CalendarTool: {task}",
            "previous_events": previous_events
        }