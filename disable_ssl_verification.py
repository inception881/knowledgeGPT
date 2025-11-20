"""
Script to disable SSL verification in Python globally.
This is useful when working with self-signed certificates or in environments
where SSL verification is problematic.
"""

import ssl
import warnings

# Disable SSL verification warnings
try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    pass

# Store the original create_default_context function
original_create_default_context = ssl.create_default_context

# Create a monkey patch function that returns a context with verification disabled
def patched_create_default_context(*args, **kwargs):
    context = original_create_default_context(*args, **kwargs)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context

# Apply the monkey patch
ssl.create_default_context = patched_create_default_context

# Also patch _create_unverified_context to be sure
try:
    ssl._create_unverified_context = ssl.create_default_context
except AttributeError:
    pass

print("SSL verification disabled globally.")
