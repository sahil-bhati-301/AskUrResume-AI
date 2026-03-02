#!/usr/bin/env python3
"""
Setup script to create .env file for Gemini API key
Run this script to configure your API key
"""
import os


def create_env_file():
    """Create .env file with Gemini API key"""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    
    if os.path.exists(env_path):
        response = input(".env file already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
    
    api_key = input("Enter your Gemini API key: ").strip()
    
    if not api_key:
        print("Error: API key cannot be empty")
        return
    
    with open(env_path, 'w') as f:
        f.write(f"GEMINI_API_KEY={api_key}\n")
    
    print(f"Successfully created .env file at {env_path}")
    print("You can now run the backend with: uvicorn app.main:app --reload")


if __name__ == "__main__":
    create_env_file()
