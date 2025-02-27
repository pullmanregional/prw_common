"""
Utility functions for loading environment variables based on PRW_ENV
"""

import os
from dotenv import load_dotenv

def load_prw_env(parent_script: str):
    """
    Load env vars from a .env file. Default to prod.
    The actual .env file loaded (eg .env.dev) depends on value of PRW_ENV.

    parent_script: str - should be the value of __file__ from the script that is calling this function.
    
    NOTE: load_dotenv() does NOT overwrite existing env vars that are set before running this script.
    If settings don't seem to be taking effect, look for the .env file in this file's directory that's 
    setting env vars before this function is called.
    """
    PRW_ENV = os.getenv("PRW_ENV", "prod")
    ENV_FILES = {
        "dev": ".env.dev",
        "prod": ".env.prod",
    }
    ENV_PATH = os.path.join(os.path.dirname(parent_script), ENV_FILES.get(PRW_ENV))
    print(f"Using environment: {ENV_PATH}")
    load_dotenv(dotenv_path=ENV_PATH)

    return PRW_ENV


