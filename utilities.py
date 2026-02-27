"""
Utilities
=========

* python functions/classes that solve very common/recurring
    programming problems & provide a reusable ( mostly generic ) 
    logic that can be used application wide .
    NOTE : strictly take care of not specific to any module/sub-module
    - for e.g :
        1. datetime formatting
        2. specific file parser ( json, csv etc ...)
        3. calculating no. of weeks in a particular month .
 
* assistive processing
    - for e.g :
        1. check for a connection establishment & raising error 
            in case of negetive scenario
    
NOTE : try to follow `seperation of concerns` rule , mostly
        by keeping the inter-related functions as static functions
        within classes or using object builder approach .
"""
import redis
import logging
from typing import Final
from datetime import datetime

def info(message: str, logger=None, also_print: bool = True, **print_kwargs)->None:
    """ outputs the message on device ( logger object / console )

    if logger object is provide , the message is logged to it 
        in INFO category
    if also_print argument is set to True , the message is
        printed on console in bule color 
    all the keyword arguments are supported that are supported
        by the print function .
    """
    if logger and isinstance(logger, logging.Logger):
        logger.info(message)
    if also_print:
        print(f"\033[94m INFO: {message} \033[0m", **print_kwargs)

def check_redis_connection(redis_connection, logger=None, on_exception_raise=Exception):
    """ checks if redis connection is in usable state or not
    """
    try:
        # Send a PING command and check the response
        if redis_connection.ping():
            info("Successfully connected to Redis!", logger)
        else:
            info("Failed to connect to Redis.", logger)
    except redis.exceptions.ConnectionError as e:
        raise on_exception_raise(f"Redis Connection error: {e}")
    

class CredentialsKey:

    def __init__(self, value: str = "credentials"):
        self._value = value
    
    @property
    def value(self):
        return self._value


def is_authenticated() -> bool:
    """
    Checks if user is currently authenticated based on Google OAuth session.
    
    Validates that:
    1. 'state' key exists in session (OAuth state from login flow)
    2. 'id_info' key exists in session (User identity info from Google)
    3. 'credentials' key exists in session (OAuth credentials with tokens)
    4. Access token is present and not empty
    5. Access token has not expired based on expiry timestamp
    
    Returns:
        bool: True if user session is active and token is still valid, False otherwise
    """
    from flask import session
    
    # Check if all required session keys exist
    required_keys = ['state', 'id_info', 'credentials']
    
    for key in required_keys:
        if key not in session:
            return False
    
    # Verify that the values are not None or empty
    if not session.get('state') or not session.get('id_info') or not session.get('credentials'):
        return False
    
    # Check if credentials dictionary has required token information
    credentials = session.get('credentials', {})
    
    # Verify access token exists
    if not credentials.get('token'):
        return False
    
    # Check if expiry information exists in credentials
    # Google credentials include 'expiry' field that contains token expiration time
    if 'expiry' in credentials:
        try:
            # Parse expiry timestamp if it's a string (ISO format)
            if isinstance(credentials['expiry'], str):
                expiry_time = datetime.fromisoformat(credentials['expiry'].replace('Z', '+00:00'))
            else:
                expiry_time = credentials['expiry']
            
            # Check if token has expired
            if expiry_time <= datetime.now(expiry_time.tzinfo):
                return False
        except (ValueError, TypeError, AttributeError):
            # If we can't parse expiry, assume token is still valid
            pass
    
    return True

