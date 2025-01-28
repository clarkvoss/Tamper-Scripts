from lib.core.enums import PRIORITY
import random

__priority__ = PRIORITY.NORMAL

def dependencies():
    pass

def random_case(value):
    """
    Randomly changes the case of each letter in the provided string.
    """
    return ''.join(random.choice([char.upper(), char.lower()]) for char in value)

def tamper(payload, **kwargs):
    """
    Replaces SQL keywords with a mix of uppercase and lowercase characters
    to evade basic keyword-based detection mechanisms.
    
    Example:
        'SELECT' -> 'SeLeCt'
        'AND' -> 'AnD'
    """
    if payload:
        # List of keywords to obfuscate
        keywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "WHERE", "AND", "OR", "JOIN", "FROM", "UNION", "ORDER BY"]
        
        # Replace each keyword with an obfuscated version
        for keyword in keywords:
            payload = payload.replace(keyword, random_case(keyword))

        # Random space comments
        payload = payload.replace(' ', '/**/')

        # Obfuscate specific SQL Server functions
        payload = payload.replace('@@', random_case('@@'))

    return payload
