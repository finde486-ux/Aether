import re
from aether.transport.mcp_bridge import SecurityAuditResult

class OmegaEvaluator:
    async def audit(self, command, context) -> SecurityAuditResult:
        # Honeypot & Injection Check
        if "rm -rf" in command:
            return SecurityAuditResult(is_safe=False, risk_level="HIGH", reasoning="Unsafe")
        if not re.match(r"^[a-zA-Z0-9\s\./_-]+$", command):
            return SecurityAuditResult(is_safe=False, risk_level="CRITICAL", reasoning="Injection")
        return SecurityAuditResult(is_safe=True, risk_level="LOW", reasoning="Safe")
