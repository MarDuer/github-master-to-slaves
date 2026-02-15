import json
from datetime import datetime
from pathlib import Path

class ChangeLogger:
    def __init__(self, logs_dir):
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.logs_dir / f"sync_{timestamp}.jsonl"
    
    def log(self, repo_name, setting_type, action, details, status="success", error=None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "repository": repo_name,
            "setting_type": setting_type,
            "action": action,
            "details": details,
            "status": status
        }
        if error:
            entry["error"] = str(error)
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
    
    def get_log_file(self):
        return self.log_file
