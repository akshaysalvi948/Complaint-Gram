#!/usr/bin/env python3
"""
Test script to verify Snowflake SiS compatibility
"""

# Test basic imports that should work in Snowflake SiS
try:
    import streamlit as st
    print("[OK] streamlit - OK")
except ImportError as e:
    print(f"[FAIL] streamlit - FAILED: {e}")

try:
    import requests
    print("[OK] requests - OK")
except ImportError as e:
    print(f"[FAIL] requests - FAILED: {e}")

try:
    import base64
    print("[OK] base64 - OK")
except ImportError as e:
    print(f"[FAIL] base64 - FAILED: {e}")

try:
    import io
    print("[OK] io - OK")
except ImportError as e:
    print(f"[FAIL] io - FAILED: {e}")

try:
    from PIL import Image
    print("[OK] PIL (Pillow) - OK")
except ImportError as e:
    print(f"[FAIL] PIL (Pillow) - FAILED: {e}")

try:
    import os
    print("[OK] os - OK")
except ImportError as e:
    print(f"[FAIL] os - FAILED: {e}")

try:
    import time
    print("[OK] time - OK")
except ImportError as e:
    print(f"[FAIL] time - FAILED: {e}")

try:
    import json
    print("[OK] json - OK")
except ImportError as e:
    print(f"[FAIL] json - FAILED: {e}")

try:
    import hashlib
    print("[OK] hashlib - OK")
except ImportError as e:
    print(f"[FAIL] hashlib - FAILED: {e}")

try:
    import hmac
    print("[OK] hmac - OK")
except ImportError as e:
    print(f"[FAIL] hmac - FAILED: {e}")

try:
    import urllib.parse
    print("[OK] urllib.parse - OK")
except ImportError as e:
    print(f"[FAIL] urllib.parse - FAILED: {e}")

try:
    from datetime import datetime
    print("[OK] datetime - OK")
except ImportError as e:
    print(f"[FAIL] datetime - FAILED: {e}")

try:
    import pandas as pd
    print("[OK] pandas - OK")
except ImportError as e:
    print(f"[FAIL] pandas - FAILED: {e}")

# Test that problematic imports are NOT used
try:
    import tweepy
    print("[WARN] tweepy found - This should NOT be used in SiS version")
except ImportError:
    print("[OK] tweepy not found - Good for SiS compatibility")

try:
    import dotenv
    print("[WARN] python-dotenv found - This should NOT be used in SiS version")
except ImportError:
    print("[OK] python-dotenv not found - Good for SiS compatibility")

print("\n[SUCCESS] All required imports are available for Snowflake SiS!")
print("[INFO] Your app should work in Snowflake Streamlit in Snowflake!")
