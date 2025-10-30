#!/usr/bin/env python3
"""
Script to check Gemini API usage and quota
"""
import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if not GOOGLE_API_KEY:
    print("❌ No Google API key found in environment variables")
    exit(1)

print(f"🔑 Using API key: {GOOGLE_API_KEY[:10]}...")

# Configure Gemini API
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    print("✅ Gemini API configured successfully")
    
    # List available models to test API access
    print("\n📋 Available models:")
    models = genai.list_models()
    for model in models:
        print(f"  - {model.name}")
        if hasattr(model, 'input_token_limit'):
            print(f"    Input token limit: {model.input_token_limit:,}")
        if hasattr(model, 'output_token_limit'):
            print(f"    Output token limit: {model.output_token_limit:,}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"    Methods: {model.supported_generation_methods}")
        print()
    
    # Try to get quota information using the REST API
    print("🔍 Checking API quota...")
    
    # Make a simple request to test the API
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hello")
    print(f"✅ Test request successful: {response.text[:50]}...")
    
    # Check if we can access usage info via REST API
    quota_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GOOGLE_API_KEY}"
    
    try:
        response = requests.get(quota_url)
        if response.status_code == 200:
            print("✅ API is accessible")
            print(f"Response headers: {dict(response.headers)}")
            
            # Look for rate limit headers
            rate_limit_headers = {k: v for k, v in response.headers.items() 
                                 if 'limit' in k.lower() or 'quota' in k.lower() or 'usage' in k.lower()}
            
            if rate_limit_headers:
                print("\n📊 Rate limit information:")
                for header, value in rate_limit_headers.items():
                    print(f"  {header}: {value}")
            else:
                print("\n❓ No rate limit headers found in response")
                
        else:
            print(f"❌ API request failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error checking quota via REST API: {e}")
    
    print("\n📈 General Gemini API Free Tier Limits:")
    print("  - Gemini 1.5 Flash: 15 requests per minute")
    print("  - Gemini 1.5 Pro: 2 requests per minute") 
    print("  - Daily quota: Varies based on model")
    print("  - Monthly quota: Check Google AI Studio for exact numbers")
    
    print("\n💡 To check detailed usage:")
    print("  1. Visit: https://aistudio.google.com/")
    print("  2. Sign in with your Google account")
    print("  3. Go to 'API Keys' section")
    print("  4. View usage statistics for your API key")
    
except Exception as e:
    print(f"❌ Error configuring Gemini API: {e}")
    print("Make sure your API key is valid and has the necessary permissions")
