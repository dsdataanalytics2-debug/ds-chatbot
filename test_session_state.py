#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test session state for expert mode
"""

def test_session_state():
    """Test session state logic"""
    
    print("=" * 60)
    print("🔍 Session State Test for Expert Mode")
    print("=" * 60)
    
    # Simulate session state
    session_state = {}
    
    # Test default values
    expert_default = session_state.get('expert_mode', False)
    strict_default = session_state.get('strict_mode', True)
    
    print(f"📊 Default values:")
    print(f"  expert_mode: {expert_default}")
    print(f"  strict_mode: {strict_default}")
    print()
    
    # Test mode priority logic
    print("🔍 Mode Priority Logic Test:")
    
    # Case 1: Expert mode True
    session_state['expert_mode'] = True
    session_state['strict_mode'] = False
    
    if session_state.get('expert_mode', False):
        print("✅ Expert Mode: True -> Should use format_expert_response")
    elif session_state.get('strict_mode', False):
        print("❌ Strict Mode: True -> Should use format_strict_response")
    else:
        print("❌ Default Mode -> Should use format_structured_response")
    
    # Case 2: Expert mode False, Strict mode True
    session_state['expert_mode'] = False
    session_state['strict_mode'] = True
    
    if session_state.get('expert_mode', False):
        print("❌ Expert Mode: True -> Should use format_expert_response")
    elif session_state.get('strict_mode', False):
        print("✅ Strict Mode: True -> Should use format_strict_response")
    else:
        print("❌ Default Mode -> Should use format_structured_response")
    
    # Case 3: Both False
    session_state['expert_mode'] = False
    session_state['strict_mode'] = False
    
    if session_state.get('expert_mode', False):
        print("❌ Expert Mode: True -> Should use format_expert_response")
    elif session_state.get('strict_mode', False):
        print("❌ Strict Mode: True -> Should use format_strict_response")
    else:
        print("✅ Default Mode -> Should use format_structured_response")
    
    print()
    print("💡 Troubleshooting Tips:")
    print("1. Make sure Expert Mode checkbox is checked in sidebar")
    print("2. Check if st.session_state.expert_mode is True")
    print("3. Verify the checkbox value is being saved to session state")
    print("4. Ensure the mode priority logic is working correctly")
    print()
    
    print("🎯 Expected Behavior:")
    print("When Expert Mode is checked:")
    print("  st.session_state.expert_mode = True")
    print("  Response should use format_expert_response()")
    print("  Output should be in Dibedex format")
    print("=" * 60)

if __name__ == "__main__":
    test_session_state()
