#!/usr/bin/env python3
"""
Test the black color selection issue through the Flask server
"""

import requests
import json
import time

def test_flask_black_selection():
    """Test black selection through Flask server"""

    session_id = "test-black-flask"

    # Step 1: Start new session (should go to INITIATED -> WAITING_CONFIRM)
    print("Step 1: Starting new session...")
    data1 = {
        "meta": {"locale": "ru-RU", "timezone": "UTC", "client_id": "ru.yandex.searchplugin/7.16",
                "interfaces": {"screen": {}, "payments": {}, "account_linking": {}}},
        "session": {"message_id": 0, "session_id": session_id, "skill_id": "alice-chess-local",
                   "user": {"user_id": "test-user"}, "application": {"application_id": "test-app"},
                   "user_id": "test-user", "skill_id": "alice-chess-local", "new": True, "message_id": 0},
        "request": {"command": "", "original_utterance": "", "type": "SimpleUtterance",
                   "markup": {"dangerous_context": False}, "payload": {}, "nlu": {"tokens": [], "entities": [], "intents": {}}, "version": "1.0"}
    }

    response1 = requests.post("http://localhost:5000", json=data1, timeout=30)
    result1 = response1.json()
    print(f"Response: {result1['response']['tts']}")
    user_state = result1.get('user_state_update', {}).get('game_state', {})

    # Step 2: Say "да" (should go to WAITING_COLOR)
    print("\nStep 2: Saying 'да'...")
    data2 = {
        "meta": {"locale": "ru-RU", "timezone": "UTC", "client_id": "ru.yandex.searchplugin/7.16",
                "interfaces": {"screen": {}, "payments": {}, "account_linking": {}}},
        "session": {"message_id": 1, "session_id": session_id, "skill_id": "alice-chess-local",
                   "user": {"user_id": "test-user"}, "application": {"application_id": "test-app"},
                   "user_id": "test-user", "skill_id": "alice-chess-local", "new": False, "message_id": 1},
        "state": {"user": user_state},
        "request": {"command": "да", "original_utterance": "да", "type": "SimpleUtterance",
                   "markup": {"dangerous_context": False}, "payload": {}, "nlu": {"tokens": ["да"], "entities": [], "intents": {}}, "version": "1.0"}
    }

    response2 = requests.post("http://localhost:5000", json=data2, timeout=30)
    result2 = response2.json()
    print(f"Response: {result2['response']['tts']}")
    user_state = result2.get('user_state_update', {}).get('game_state', {})

    # Step 3: Say "черные" (should trigger the error)
    print("\nStep 3: Saying 'черные'...")
    data3 = {
        "meta": {"locale": "ru-RU", "timezone": "UTC", "client_id": "ru.yandex.searchplugin/7.16",
                "interfaces": {"screen": {}, "payments": {}, "account_linking": {}}},
        "session": {"message_id": 2, "session_id": session_id, "skill_id": "alice-chess-local",
                   "user": {"user_id": "test-user"}, "application": {"application_id": "test-app"},
                   "user_id": "test-user", "skill_id": "alice-chess-local", "new": False, "message_id": 2},
        "state": {"user": user_state},
        "request": {"command": "черные", "original_utterance": "черные", "type": "SimpleUtterance",
                   "markup": {"dangerous_context": False}, "payload": {}, "nlu": {"tokens": ["черные"], "entities": [], "intents": {}}, "version": "1.0"}
    }

    response3 = requests.post("http://localhost:5000", json=data3, timeout=30)
    result3 = response3.json()
    print(f"Response: {result3['response']['tts']}")

    if "ошибка" in result3['response']['tts'].lower():
        print("\n❌ ERROR REPRODUCED!")
        return False
    else:
        print("\n✅ SUCCESS!")
        return True

if __name__ == "__main__":
    test_flask_black_selection()
