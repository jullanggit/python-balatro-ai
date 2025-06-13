#!/usr/bin/env python3
"""
Basic test script to verify imports and structure work correctly
"""

import sys
import os

# Add parent directory to path for balatro imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_balatro_imports():
    """Test that we can import balatro module"""
    print("Testing balatro imports...")
    
    try:
        from balatro import Deck, Stake, Run, Blind, State
        print("✓ Basic balatro imports successful")
        
        # Test creating a simple run
        run = Run(Deck.RED, stake=Stake.WHITE)
        print(f"✓ Run creation successful: Ante {run.ante}")
        
        return True
    except Exception as e:
        print(f"✗ Balatro import test failed: {e}")
        return False

def test_encode_imports():
    """Test that we can import encoding utilities"""
    print("\nTesting encode imports...")
    
    try:
        from encode import SIZE_ENCODED, encode
        print(f"✓ Encode imports successful")
        print(f"  - Encoded state size: {SIZE_ENCODED}")
        
        # Test encoding a simple run
        from balatro import Deck, Stake, Run
        run = Run(Deck.RED, stake=Stake.WHITE)
        encoded_state = encode(run)
        print(f"✓ State encoding successful: shape {encoded_state.shape}")
        
        return True
    except Exception as e:
        print(f"✗ Encode test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_env_structure():
    """Test environment structure without full torch dependencies"""
    print("\nTesting environment structure...")
    
    try:
        from env import ActionType, PARAM1_LENGTH, PARAM2_LENGTH
        print(f"✓ Action space imports successful")
        print(f"  - Number of action types: {len(ActionType)}")
        print(f"  - Param1 length: {PARAM1_LENGTH}")
        print(f"  - Param2 length: {PARAM2_LENGTH}")
        
        # Test action types
        action_names = [action.name for action in ActionType]
        print(f"  - Action types: {action_names[:5]}...")
        
        return True
    except Exception as e:
        print(f"✗ Environment structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_game_mechanics():
    """Test basic game mechanics work"""
    print("\nTesting basic game mechanics...")
    
    try:
        from balatro import Deck, Stake, Run
        
        # Create a run and test basic operations
        run = Run(Deck.RED, stake=Stake.WHITE, seed=42)
        print(f"✓ Created run with seed 42")
        print(f"  - Initial money: ${run.money}")
        print(f"  - Initial ante: {run.ante}")
        print(f"  - Hand size: {len(run.hand) if run.hand else 0}")
        
        # Try selecting blind
        run.select_blind()
        print(f"✓ Selected blind: {run.blind}")
        
        # Try playing a hand (first 3 cards)
        if run.hand and len(run.hand) >= 3:
            initial_score = run.round_score
            run.play_hand([0, 1, 2])
            print(f"✓ Played hand - Score: {initial_score} -> {run.round_score}")
        
        return True
    except Exception as e:
        print(f"✗ Game mechanics test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all basic tests"""
    print("=" * 50)
    print("BASIC SETUP VERIFICATION")
    print("=" * 50)
    
    tests = [
        ("Balatro Imports", test_balatro_imports),
        ("Encode Module", test_encode_imports), 
        ("Environment Structure", test_env_structure),
        ("Game Mechanics", test_basic_game_mechanics)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*15} {test_name} {'='*15}")
        success = test_func()
        results.append((test_name, success))
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    all_passed = True
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{test_name:20}: {status}")
        if not success:
            all_passed = False
    
    print("-" * 50)
    if all_passed:
        print("🎉 All basic tests passed!")
        print("\nNext steps:")
        print("1. Install PyTorch and TorchRL dependencies")
        print("2. Run the full PPO setup test")
        print("3. Start training with: python ppo_balatro.py")
    else:
        print("❌ Some basic tests failed.")
        print("Please fix the import issues before proceeding.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())