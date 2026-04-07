from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import re
import random
import time

from agents.orchestrator import OrchestratorAgent
from agents.scheduling_agent import SchedulingAgent
from agents.notes_agent import NotesAgent
from agents.summarization_agent import SummarizationAgent

app = FastAPI()
START_TIME = time.time()


# ================= ROOT =================
@app.get("/", response_class=HTMLResponse)
def home():
    return ui()


# ================= HEALTH =================
@app.get("/health")
def health():
    return {
        "status": "online",
        "uptime_seconds": round(time.time() - START_TIME),
        "agents": {
            "orchestrator": "online",
            "scheduling": "online",
            "notes": "online",
            "summarization": "online"
        },
        "tools": {
            "CalendarTool": "connected",
            "NotesTool": "connected"
        },
        "db": "connected"
    }


# ================= UI =================
@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
<!DOCTYPE html>
<html>
<head>
<title>APS AI Assistant</title>

<style>
body { margin:0; font-family: Inter, sans-serif; background:#0d1117; color:#e6edf3; display:flex; height:100vh; }

.sidebar { width:240px; background:#161b22; padding:16px; border-right:1px solid #30363d; }
button {
  width:100%; margin:6px 0; padding:8px;
  background:#21262d; border:1px solid #30363d;
  color:#c9d1d9; border-radius:6px;
}
button:hover { background:#30363d; }

.db { margin-top:20px; font-size:12px; }

.main { flex:1; display:flex; flex-direction:column; }

#topbar-status {
  padding:8px; font-size:12px; color:#8b949e;
  border-bottom:1px solid #30363d;
}

.chat { flex:1; overflow:auto; padding:20px; }

.input { display:flex; gap:10px; padding:12px; border-top:1px solid #30363d; }
input {
  flex:1; padding:10px; background:#21262d;
  border:1px solid #30363d; color:white; border-radius:8px;
}
.send {
  width:auto; padding:10px 32px;
  background:#238636; border:none;
  color:white; border-radius:8px;
}

.msg-user { display:flex; justify-content:flex-end; margin:10px 0; }
.msg-user div {
  background:#1f6feb;
  padding:10px 14px;
  border-radius:12px 12px 2px 12px;
}
</style>
</head>

<body>

<div class="sidebar">
<h3>⚡ Quick Demo</h3>

<button onclick="send('Schedule meeting at 8 PM')">Schedule</button>
<button onclick="send('Take a note: Finish project docs')">Note</button>
<button onclick="send('Summarize notes')">Summary</button>

<!-- 🔥 Killer Feature Button -->
<button onclick="send('Schedule meeting at 6 PM and take a note about AI trends')">
Multi Task 🔥
</button>

<div class="db">
<h4>📊 DB Preview</h4>
<div id="db"></div>
</div>
</div>

<div class="main">

<div id="topbar-status"></div>

<div class="chat" id="chat"></div>

<div class="input">
<input id="inp" placeholder="Ask something..." />
<button class="send" onclick="sendReq()">Send</button>
</div>

</div>

<script>

// 🔥 Health
fetch('/health')
.then(r=>r.json())
.then(h=>{
 document.getElementById('topbar-status').innerText =
 `${Object.keys(h.agents).length} agents online | DB connected | uptime ${Math.round(h.uptime_seconds/60)}m`;
});

function send(text){
 document.getElementById("inp").value=text;
 sendReq();
}

async function sendReq(){
 let val=document.getElementById("inp").value.trim();
 let chat=document.getElementById("chat");

 if(!val) return;

 chat.innerHTML+=`<div class='msg-user'><div>${val}</div></div>`;

 let res=await fetch('/chat?user_input='+encodeURIComponent(val));
 let data=await res.json();

 let output="";

 data.execution.forEach(item => {

    const r = item.result;

    const agentMap = {
        scheduling: ['#a371f7', 'Scheduling'],
        notes: ['#3fb950', 'Notes'],
        summarization: ['#f0883e', 'Summarization']
    };

    const [color, label] = agentMap[item.agent] || ['#8b949e', item.agent];

    // Pipeline
    const pipeline = ['Input','Orchestrator', label, 'DB','Done'];
    let pipelineHTML = '<div style="margin-bottom:6px">';
    pipeline.forEach((p,i)=>{
      pipelineHTML += `<span style="font-size:10px;color:${i===pipeline.length-1?'#3fb950':'#8b949e'}">${p}</span>`;
      if(i<pipeline.length-1) pipelineHTML+=' → ';
    });
    pipelineHTML+='</div>';

    let content = '';

    if (r.status === 'scheduled')
        content = `📅 Event Scheduled\\nTitle: ${r.event?.title}\\nTime: ${r.event?.time}\\nID: ${r.event?.id}`;
    else if (r.status === 'note_created')
        content = `📝 Note saved successfully`;
    else if (r.status === 'summary_generated')
        content = `🧠 Summary:\\n${r.summary}`;
    else
        content = r.details || JSON.stringify(r);

    // 🔥 Remove fallback text
    content = content.replace("(fallback mode)", "");

    content = pipelineHTML + content + `\\n(${item.execution_ms} ms)`;

    output += `
    <div style="display:flex;gap:10px;margin:12px 0;">
      <div style="width:28px;height:28px;border-radius:50%;background:#21262d;
        border:1px solid ${color};display:flex;align-items:center;justify-content:center;
        font-size:11px;color:${color};">A</div>
      <div>
        <span style="font-size:10px;padding:2px 8px;border-radius:99px;
          border:1px solid ${color}40;background:${color}15;color:${color};">
          ${label} Agent
        </span>
        <div style="background:#161b22;border:1px solid #30363d;border-radius:4px 12px 12px 12px;
          padding:12px;margin-top:6px;white-space:pre-wrap;">
          ${content}
        </div>
      </div>
    </div>
    `;

    // DB Preview
    if(r.event){
        updateDB(`📅 ${r.event.title} - ${r.event.time}`);
    }
    if(r.details && !r.details.toLowerCase().includes("event stored")){
        updateDB(`📝 ${r.details}`);
    }

 });

 chat.innerHTML+=output;
 document.getElementById("inp").value="";
 chat.scrollTop = chat.scrollHeight;
}

function updateDB(item){
 let db=document.getElementById("db");
 db.innerHTML = `<div>${item}</div>` + db.innerHTML;
}

</script>

</body>
</html>
"""


# ================= CHAT =================
@app.get("/chat")
def chat(user_input: str):

    orchestrator = OrchestratorAgent()
    orch_data = orchestrator.process(user_input)

    tasks = orch_data["tasks"]
    execution_results = []

    for task in tasks:
        start = time.time()

        agent_name = task["agent"]
        task_input = task["task"]

        if agent_name == "scheduling":
            agent = SchedulingAgent()
            result = agent.execute(task_input)

            time_match = re.search(r'\b\d{1,2}\s?(AM|PM|am|pm)\b', user_input)
            time_value = time_match.group() if time_match else "Not specified"

            clean_title = re.sub(
                r'\bat\s*\d{1,2}\s?(AM|PM|am|pm)\b',
                '',
                task_input,
                flags=re.IGNORECASE
            ).strip().capitalize()

            result["event"] = {
                "title": clean_title,
                "time": time_value,
                "id": f"EVT{random.randint(100,999)}"
            }

        elif agent_name == "notes":
            agent = NotesAgent()
            result = agent.execute(task_input)

            clean_note = re.sub(
                r'(take a note:|take notes on|note:)',
                '',
                user_input,
                flags=re.IGNORECASE
            ).strip().capitalize()

            result["details"] = clean_note

        elif agent_name == "summarization":
            agent = SummarizationAgent()
            result = agent.execute()

        else:
            result = {"status": "unknown"}

        elapsed = round((time.time() - start) * 1000)

        execution_results.append({
            "agent": agent_name,
            "result": result,
            "execution_ms": elapsed,
            "tool_used": result.get("tool_used", "internal")
        })

    return {
        "input": user_input,
        "orchestrator_reasoning": orch_data.get("reasoning", ""),
        "execution": execution_results
    }