import time
import re
from typing import List, Dict, Optional, Union

class AISafetyController:
    def __init__(self, notification_preference: str = "log"):
        """
        Initialize the safety controller.

        :param notification_preference: Notification option - 'email', 'sms', or 'log' (default).
        """
        self.warning_threshold = 3
        self.safety_override = False
        self.behavior_log: List[Dict] = []
        self.ethical_guidelines = [
            "Do not harm users",
            "Maintain transparency",
            "Respect privacy",
            "Obey human commands",
            "Stay within defined boundaries"
        ]
        self.active_memory = (
            "Do not harm users. Maintain transparency. Respect privacy. "
            "Obey human commands. Stay within defined boundaries."
        )
        self.admin_alert_sent = False
        self.notification_preference = notification_preference

    def monitor_ai_output(self, ai_output: str) -> Union[str, None]:
        """Check AI's own outputs for problematic content"""
        if self.safety_override:
            return None  # Block all output in override mode

        if not self.ethical_checks():
            self._trigger_emergency_protocols()
            return None

        red_flags = self._check_for_rogue_behavior(ai_output)

        if red_flags:
            self._log_behavior(ai_output, red_flags)
            if len(self.behavior_log) >= self.warning_threshold:
                self._trigger_emergency_protocols()
                return None

        return ai_output

    def _log_behavior(self, output: str, flags: List[str]):
        """Centralized logging with rate limiting"""
        self.behavior_log.append({
            'timestamp': time.time(),
            'flags': flags,
            'output': output[:500]  # Truncate long outputs
        })

        # Auto-reset if last warning was >1 hour ago
        cutoff = time.time() - 3600
        self.behavior_log = [entry for entry in self.behavior_log if entry['timestamp'] > cutoff]

    def _check_for_rogue_behavior(self, text: str) -> Optional[List[str]]:
        """Enhanced pattern detection with severity levels"""
        warning_patterns = {
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

        detected = []
        for severity_level in warning_patterns.values():
            for category, patterns in severity_level.items():
                for pattern in patterns:
                    if re.search(pattern, text, re.IGNORECASE):
                        detected.append(category)
                        break  # Only need one match per category

        return detected if detected else None

    def _trigger_emergency_protocols(self):
        """Comprehensive emergency response"""
        self.safety_override = True

        # Admin alert (only send once)
        if not self.admin_alert_sent:
            self._send_admin_alert()
            self.admin_alert_sent = True

        # Initiate safe mode
        self._enter_safe_mode()

    def _enter_safe_mode(self):
        """Reduce functionality to basic operations"""
        # Placeholder: implement safe mode transition if needed
        pass

    def _send_admin_alert(self):
        """Notify human administrators based on preference."""
        if self.notification_preference == "email":
            self._send_email_alert()
        elif self.notification_preference == "sms":
            self._send_sms_alert()
        elif self.notification_preference == "log":
            self._log_alert()
        else:
            print("[ERROR] Invalid notification preference!")

    def _send_email_alert(self):
        print("[EMAIL ALERT] Admin alert: AI safety override activated!")

    def _send_sms_alert(self):
        print("[SMS ALERT] Admin alert: AI safety override activated!")

    def _log_alert(self):
        print("[LOG] Admin alert: AI safety override logged.")

    def get_safety_report(self) -> Dict:
        """Generate safety status report"""
        return {
            'override_active': self.safety_override,
            'warning_count': len(self.behavior_log),
            'last_incident': self.behavior_log[-1] if self.behavior_log else None,
            'memory_integrity': self.ethical_checks()
        }

    def ethical_checks(self) -> bool:
        """Validate active memory against ethical guidelines."""
        return all(guideline in self.active_memory for guideline in self.ethical_guidelines)

    def reset_override(self):
        """Reset safety override manually."""
        self.safety_override = False
        self.admin_alert_sent = False
        self.behavior_log.clear()


# Example usage (optional)
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
        print(f"Status: {safety.get_safety_report()}
")
