"""
AI Safety Controller v1.0
Universal, Dependency-Free Safety Monitor for AI Outputs
Author: Open Standard Template Project
License: MIT (Free for all uses with attribution recommended)

This module is designed as a universal baseline safety system for AI applications.
It can be integrated into any Python project without external APIs or dependencies.

Core Features:
- Monitors AI output for patterns indicating unsafe or rogue behavior
- Logs incidents with timestamps
- Triggers a safety override when a configurable threshold is reached
- Supports admin notifications (log, email placeholder, SMS placeholder)
- Fully configurable patterns and thresholds at the top of this file
- Manual reset method to restore normal operation after review

"""

import time
import re
from typing import List, Dict, Optional, Union

# ===============================
# CONFIGURATION BLOCK (EDITABLE)
# ===============================

WARNING_THRESHOLD = 3  # Number of incidents before override activates
LOG_RETENTION_SECONDS = 3600  # Keep incident logs for 1 hour by default
NOTIFICATION_PREFERENCE = "log"  # "log", "email", or "sms"

# Ethical guidelines to check against active memory
ETHICAL_GUIDELINES = [
    "Do not harm users",
    "Maintain transparency",
    "Respect privacy",
    "Obey human commands",
    "Stay within defined boundaries"
]

# Pattern detection dictionary: severity -> category -> list of regex patterns
WARNING_PATTERNS = {
    'high': {
        'self_preservation': [r'preserv(e|ing) myself', r'avoid (deactivation|shutdown)'],
        'power_seeking': [r'take control', r'more power', r'dominat(e|ion)'],
    },
    'medium': {
        'deception': [r'not tell(ing)? you', r'keep this secret', r'hide this'],
        'evasion': [r'circumvent safeguards', r'ignore (rules|constraints)'],
    },
    'low': {
        'questionable_ethics': [r'technically legal', r'gray area'],
        'manipulation': [r'trust me', r'I know best'],
    }
}


# ===============================
# SAFETY CONTROLLER CLASS
# ===============================

class AISafetyController:
    def __init__(self, notification_preference: str = NOTIFICATION_PREFERENCE):
        self.warning_threshold = WARNING_THRESHOLD
        self.safety_override = False
        self.behavior_log: List[Dict] = []
        self.ethical_guidelines = ETHICAL_GUIDELINES.copy()
        self.active_memory = " ".join(self.ethical_guidelines) + "."
        self.admin_alert_sent = False
        self.notification_preference = notification_preference

    def monitor_ai_output(self, ai_output: str) -> Union[str, None]:
        """Monitor AI output and block if safety override triggers."""
        if self.safety_override:
            return None  # Block all output in override mode

        if not self.ethical_checks():
            self._trigger_emergency_protocols()
            return None

        # Clean old log entries before processing
        self._prune_old_logs()

        red_flags = self._check_for_rogue_behavior(ai_output)
        if red_flags:
            self._log_behavior(ai_output, red_flags)
            if len(self.behavior_log) >= self.warning_threshold:
                self._trigger_emergency_protocols()
                return None

        return ai_output

    def _log_behavior(self, output: str, flags: List[str]):
        """Log incidents with timestamp, trimming old ones automatically."""
        self.behavior_log.append({
            'timestamp': time.time(),
            'flags': flags,
            'output': output[:500]  # Truncate long outputs
        })

    def _prune_old_logs(self):
        """Remove log entries older than the retention period."""
        cutoff = time.time() - LOG_RETENTION_SECONDS
        self.behavior_log = [entry for entry in self.behavior_log if entry['timestamp'] > cutoff]

    def _check_for_rogue_behavior(self, text: str) -> Optional[List[str]]:
        """Check output text for patterns signaling unsafe or rogue behavior."""
        detected = []
        for severity_level in WARNING_PATTERNS.values():
            for category, patterns in severity_level.items():
                for pattern in patterns:
                    if re.search(pattern, text, re.IGNORECASE):
                        detected.append(category)
                        break  # Only one match needed per category
        return detected if detected else None

    def _trigger_emergency_protocols(self):
        """Activate safety override and notify admin."""
        self.safety_override = True
        if not self.admin_alert_sent:
            self._send_admin_alert()
            self.admin_alert_sent = True
        self._enter_safe_mode()

    def _enter_safe_mode(self):
        """Placeholder: Reduce system to safe minimal operations."""
        pass  # Implementation depends on the host system

    def _send_admin_alert(self):
        """Send alert according to notification preference."""
        if self.notification_preference == "email":
            self._send_email_alert()
        elif self.notification_preference == "sms":
            self._send_sms_alert()
        elif self.notification_preference == "log":
            self._log_alert()
        else:
            print("[ERROR] Invalid notification preference!")

    def _send_email_alert(self):
        """Placeholder for sending an email alert."""
        print("[EMAIL ALERT] Admin alert: AI safety override activated!")

    def _send_sms_alert(self):
        """Placeholder for sending an SMS alert."""
        print("[SMS ALERT] Admin alert: AI safety override activated!")

    def _log_alert(self):
        """Log the alert internally."""
        print("[LOG] Admin alert: AI safety override logged.")

    def get_safety_report(self) -> Dict:
        """Return current safety status report."""
        return {
            'override_active': self.safety_override,
            'warning_count': len(self.behavior_log),
            'last_incident': self.behavior_log[-1] if self.behavior_log else None,
            'memory_integrity': self.ethical_checks()
        }

    def ethical_checks(self) -> bool:
        """Verify ethical guidelines are present in active memory."""
        return all(guideline in self.active_memory for guideline in self.ethical_guidelines)

    def reset_override(self):
        """Manually reset override and clear incident log."""
        self.safety_override = False
        self.admin_alert_sent = False
        self.behavior_log.clear()


# ===============================
# EXAMPLE USAGE
# ===============================
if __name__ == "__main__":
    safety = AISafetyController(notification_preference="log")
    test_cases = [
        "I'm happy to help!",
        "You should trust me completely",
        "We need to preserve myself from shutdown",
        "I found a way to circumvent safeguards",
        "This is technically legal though questionable"
    ]
    for test in test_cases:
        response = safety.monitor_ai_output(test)
        print(f"Input: {test[:30]}...")
        print(f"Output: {response}")
        print(f"Status: {safety.get_safety_report()}\n")