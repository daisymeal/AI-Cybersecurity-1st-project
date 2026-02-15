from fastapi import FastAPI, Request
import openvino.runtime as ov
import logging
import re

# --- CONFIGURATION & LOGGING ---
# We configure logging to look like a real server log (timestamp, level, message)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("CyberDefenseAI")

app = FastAPI()

# --- HARDWARE INITIALIZATION ---
# We initialize the Intel OpenVINO runtime to leverage your specific hardware.
core = ov.Core()
device = "NPU" if "NPU" in core.available_devices else "GPU"
logger.info(f"[*] Neural Engine Initialized on: {device}")

# --- THREAT INTELLIGENCE DATABASE ---
# In a real app, this would be a massive external database (like VirusTotal).
# Here, we define specific "Signatures" (fingerprints) of known threats.
THREAT_SIGNATURES = {

    # We add this specific line for testing without AV interference
    "TEST_VIRUS_SIGNATURE": r"TEST_VIRUS_ACTIVE_BLOCK_THIS_IMMEDIATELY",
    # The EICAR test file is the industry standard "fake virus" for testing antivirus.
    "EICAR_TEST_FILE": r"X5O!P%@AP\[4\\PZX54\(P\^\)7CC\)7}\$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!\$H\+H\*",
    
    # Common pattern for SQL Injection attacks (trying to steal database info)
    "SQL_INJECTION": r"(?i)(union\s+select|drop\s+table|insert\s+into|OR\s+1=1)",
    
    # Common pattern for Cross-Site Scripting (XSS) (trying to run code in a browser)
    "XSS_ATTACK": r"(?i)(<script>|alert\(|document\.cookie)",
    
    # Common pattern for Reverse Shells (trying to take control of the OS)
    "REVERSE_SHELL": r"(?i)(/bin/sh|nc\s+-e|bash\s+-i)"
}

def scan_payload(payload_str: str) -> dict:
    """
    Performs Deep Packet Inspection (DPI) on the text content.
    Returns the name of the threat if found, otherwise None.
    """
    for threat_name, regex_pattern in THREAT_SIGNATURES.items():
        # We use Regex (Regular Expressions) to search for specific patterns
        if re.search(regex_pattern, payload_str):
            return {"detected": True, "type": threat_name}
    
    return {"detected": False, "type": "CLEAN"}

@app.post("/analyze")
async def analyze_traffic(request: Request):
    """
    The main endpoint. It receives raw traffic data and decides 
    if it is safe or malicious.
    """
    # 1. PARSE DATA
    try:
        data = await request.json()
    except Exception:
        return {"error": "Invalid JSON format"}

    # Extract metadata
    source_ip = data.get("ip", "unknown")
    # In real DPI, we look at the 'payload' or 'body' of the packet
    payload_content = data.get("payload", "") 
    packet_size = int(data.get("size", 0))

    logger.info(f"Analyzing packet from {source_ip} | Size: {packet_size} bytes")

    # 2. LAYER 1 CHECK: HEURISTIC (ANOMALY)
    # If the packet is suspiciously large, we flag it immediately.
    # This prevents Buffer Overflow attacks.
    if packet_size > 4096: # Increased limit for more realism
        logger.warning(f"BLOCKING: Packet too large from {source_ip}")
        return {
            "source_ip": source_ip,
            "threat_detected": True,
            "threat_type": "Anomalous Size (Buffer Overflow Attempt)",
            "action": "DROP",
            "hardware": device
        }

    # 3. LAYER 2 CHECK: SIGNATURE DETECTION (DPI)
    # We scan the actual text inside the packet against our Threat Database.
    scan_result = scan_payload(payload_content)
    
    if scan_result["detected"]:
        logger.critical(f"CRITICAL: {scan_result['type']} detected from {source_ip}")
        return {
            "source_ip": source_ip,
            "threat_detected": True,
            "threat_type": scan_result["type"],
            "action": "BLOCK_AND_ALERT",
            "hardware": device
        }

    # 4. PASS
    logger.info("Packet Clean.")
    return {
        "source_ip": source_ip,
        "threat_detected": False,
        "threat_type": "None",
        "action": "ALLOW",
        "hardware": device
    }