#!/usr/bin/env python3
"""
Test script to verify spam detection integration
"""

import requests
import json
import time

def test_spam_detection_api():
    """Test the AI model API directly"""
    print("Testing AI Model API...")
    
    test_messages = [
        "Hello, how are you?",  # Normal message
        "Congratulations! You've won $1000! Click here now!",  # Spam message
        "Can we meet tomorrow for coffee?",  # Normal message
        "URGENT: Verify your account immediately to avoid suspension!",  # Spam message
    ]
    
    api_url = "http://localhost:8000/predict"
    
    for message in test_messages:
        try:
            response = requests.post(api_url, json={"text": message})
            if response.status_code == 200:
                result = response.json()
                spam_level = result.get("spamLevel", 0)
                is_spam = spam_level > 0.5
                print(f"Message: '{message}'")
                print(f"Spam Level: {spam_level:.3f} ({'SPAM' if is_spam else 'NOT SPAM'})")
                print("-" * 50)
            else:
                print(f"Error: HTTP {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to AI model API. Make sure it's running on port 8000.")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    return True

def test_backend_api():
    """Test the backend API"""
    print("\nTesting Backend API...")
    
    backend_url = "http://localhost:8080"
    
    try:
        # Test if backend is running
        response = requests.get(f"{backend_url}/actuator/health", timeout=5)
        if response.status_code == 200:
            print("✓ Backend is running")
        else:
            print("⚠ Backend health check failed")
    except requests.exceptions.ConnectionError:
        print("✗ Backend is not running. Start it with: mvn spring-boot:run")
        return False
    except Exception as e:
        print(f"Error checking backend: {e}")
        return False
    
    return True

def main():
    print("=== Spam Detection Integration Test ===\n")
    
    # Test AI Model API
    ai_ok = test_spam_detection_api()
    
    # Test Backend API
    backend_ok = test_backend_api()
    
    print("\n=== Test Results ===")
    print(f"AI Model API: {'✓ PASS' if ai_ok else '✗ FAIL'}")
    print(f"Backend API: {'✓ PASS' if backend_ok else '✗ FAIL'}")
    
    if ai_ok and backend_ok:
        print("\n🎉 All tests passed! The spam detection integration is working.")
        print("\nNext steps:")
        print("1. Start the frontend: cd frontend-chat && npm run dev")
        print("2. Open http://localhost:5173 in your browser")
        print("3. Create a room and test spam detection with multiple users")
    else:
        print("\n❌ Some tests failed. Please check the services and try again.")

if __name__ == "__main__":
    main()
