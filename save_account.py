#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Save Cursor account information to a text file
"""

import os
import sys
import json
import datetime
from pathlib import Path

def save_account_info(email, password):
    """
    Save account info to a text file in the accounts directory
    
    Args:
        email (str): Account email address
        password (str): Account password
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    try:
        # Create accounts directory if it doesn't exist
        accounts_dir = "accounts"
        if not os.path.exists(accounts_dir):
            os.makedirs(accounts_dir)
        
        # Create filename based on email (remove invalid chars)
        filename = email.replace('@', '_at_').replace('.', '_dot_') + '.txt'
        filepath = os.path.join(accounts_dir, filename)
        
        # Get current date and time
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create account data
        account_data = f"""Cursor Account Information
==============================
Date Created: {current_time}
Email: {email}
Password: {password}
==============================
"""
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(account_data)
        
        # Also save as JSON for programmatic use
        json_filepath = os.path.join(accounts_dir, filename.replace('.txt', '.json'))
        account_json = {
            "email": email,
            "password": password,
            "created_at": current_time
        }
        
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(account_json, f, indent=4)
        
        print(f"Account information saved successfully to {filepath}")
        print(f"JSON data saved to {json_filepath}")
        return True
    
    except Exception as e:
        print(f"Error saving account information: {str(e)}")
        return False

# Direct usage
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python save_account.py <email> <password>")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    save_account_info(email, password) 