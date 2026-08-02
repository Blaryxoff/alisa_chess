#!/usr/bin/env python3
"""
Test script to reproduce the black color selection issue
"""

import requests
import json

def test_black_selection():
    """Test selecting black pieces to reproduce the error."""

    # Initialize session
    session_id = "test-session-black"

    # First request: Say "давай сыграем в шахматы" - should go to INITIATED -> WAITING_CONFIRM
    data1 = {
        "meta": {
            "locale": "ru-RU",
            "timezone": "UTC",
            "client_id": "ru.yandex.searchplugin/7.16",
            "interfaces": {
                "screen": {},
                "payments": {},
                "account_linking": {}
            }
        },
        "session": {
            "message_id": 0,
            "session_id": session_id,
            "skill_id": "alice-chess-local",
            "user": {
                "user_id": "test-user"
            },
            "application": {
                "application_id": "test-app"
            },
            "user_id": "test-user",
            "skill_id": "alice-chess-local",
            "new": True,
            "message_id": 0
        },
        "request": {
            "command": "давай сыграем в шахматы",
            "original_utterance": "давай сыграем в шахматы",
            "type": "SimpleUtterance",
            "markup": {
                "dangerous_context": False
            },
            "payload": {},
            "nlu": {
                "tokens": ["давай", "сыграем", "в", "шахматы"],
                "entities": [],
                "intents": {}
            }
        },
        "version": "1.0"
    }

    print("Step 1: Saying 'давай сыграем в шахматы'...")
    response1 = requests.post("http://localhost:5000", json=data1, timeout=30)
    result1 = response1.json()
    print(f"Response: {result1['response']['tts']}")
    print(f"State after step 1: {result1.get('user_state_update', {}).get('game_state', {})}")

    # Extract user state for next request
    user_state = result1.get('user_state_update', {}).get('game_state', {})

    # Second request: Say "да" to confirm - should go to WAITING_COLOR
    data2 = {
        "meta": {
            "locale": "ru-RU",
            "timezone": "UTC",
            "client_id": "ru.yandex.searchplugin/7.16",
            "interfaces": {
                "screen": {},
                "payments": {},
                "account_linking": {}
            }
        },
        "session": {
            "message_id": 1,
            "session_id": session_id,
            "skill_id": "alice-chess-local",
            "user": {
                "user_id": "test-user"
            },
            "application": {
                "application_id": "test-app"
            },
            "user_id": "test-user",
            "skill_id": "alice-chess-local",
            "new": False,
            "message_id": 1
        },
        "state": {
            "user": user_state
        },
        "request": {
            "command": "да",
            "original_utterance": "да",
            "type": "SimpleUtterance",
            "markup": {
                "dangerous_context": False
            },
            "payload": {},
            "nlu": {
                "tokens": ["да"],
                "entities": [],
                "intents": {}
            }
        },
        "version": "1.0"
    }

    print("\nStep 2: Saying 'да' to confirm...")
    response2 = requests.post("http://localhost:5000", json=data2, timeout=30)
    result2 = response2.json()
    print(f"Response: {result2['response']['tts']}")
    print(f"State after step 2: {result2.get('user_state_update', {}).get('game_state', {})}")

    # Extract user state for next request
    user_state = result2.get('user_state_update', {}).get('game_state', {})

    # Third request: Select black pieces
    data3 = {
        "meta": {
            "locale": "ru-RU",
            "timezone": "UTC",
            "client_id": "ru.yandex.searchplugin/7.16",
            "interfaces": {
                "screen": {},
                "payments": {},
                "account_linking": {}
            }
        },
        "session": {
            "message_id": 2,
            "session_id": session_id,
            "skill_id": "alice-chess-local",
            "user": {
                "user_id": "test-user"
            },
            "application": {
                "application_id": "test-app"
            },
            "user_id": "test-user",
            "skill_id": "alice-chess-local",
            "new": False,
            "message_id": 2
        },
        "state": {
            "user": user_state
        },
        "request": {
            "command": "черные",
            "original_utterance": "черные",
            "type": "SimpleUtterance",
            "markup": {
                "dangerous_context": False
            },
            "payload": {},
            "nlu": {
                "tokens": ["черные"],
                "entities": [],
                "intents": {}
            }
        },
        "version": "1.0"
    }

    print("\nStep 3: Selecting black pieces...")
    response3 = requests.post("http://localhost:5000", json=data3, timeout=30)
    result3 = response3.json()
    print(f"Response: {result3['response']['tts']}")
    print(f"State after step 3: {result3.get('user_state_update', {}).get('game_state', {})}")

    if "ошибка" in result3['response']['tts'].lower():
        print("\n❌ ERROR REPRODUCED: The same error occurs when selecting black pieces!")
        return False
    else:
        print("\n✅ SUCCESS: Black piece selection worked!")
        return True

if __name__ == "__main__":
    test_black_selection()
