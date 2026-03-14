"""
Paytm Checksum Utility
This module generates and verifies Paytm checksums using HMAC SHA256
Note: For production, it's recommended to use Paytm's official Python SDK
"""

import hashlib
import hmac


def generate_checksum(param_dict, merchant_key, salt_length=4):
    """
    Generate Paytm checksum
    Note: This is a simplified version. For production, use Paytm's official SDK
    """
    # Convert dictionary to string and sort
    param_string = '|'.join([f"{key}={value}" for key, value in sorted(param_dict.items()) if key != 'CHECKSUMHASH'])
    param_string += f"|{merchant_key}"
    
    # Generate hash
    hash_string = hashlib.sha256(param_string.encode()).hexdigest()
    
    return hash_string.upper()


def verify_checksum(param_dict, merchant_key, checksum):
    """
    Verify Paytm checksum
    Note: This is a simplified version. For production, use Paytm's official SDK
    """
    # Generate checksum from parameters
    calculated_checksum = generate_checksum(param_dict, merchant_key)
    
    # Compare with received checksum
    return calculated_checksum == checksum.upper()


# Alternative implementation using HMAC (more secure)
def generate_checksum_hmac(param_dict, merchant_key):
    """Generate checksum using HMAC SHA256"""
    param_string = '|'.join([f"{key}={value}" for key, value in sorted(param_dict.items()) if key != 'CHECKSUMHASH'])
    param_string += f"|{merchant_key}"
    
    checksum = hmac.new(
        merchant_key.encode(),
        param_string.encode(),
        hashlib.sha256
    ).hexdigest().upper()
    
    return checksum


def verify_checksum_hmac(param_dict, merchant_key, checksum):
    """Verify checksum using HMAC SHA256"""
    calculated_checksum = generate_checksum_hmac(param_dict, merchant_key)
    return calculated_checksum == checksum.upper()

