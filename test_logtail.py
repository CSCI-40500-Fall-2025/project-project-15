#!/usr/bin/env python3
"""Test script to verify Logtail connection"""
import os
import logging
from logtail import LogtailHandler

token = os.getenv("LOGTAIL_SOURCE_TOKEN")
if not token:
    print("ERROR: LOGTAIL_SOURCE_TOKEN not set")
    exit(1)

print(f"Token found (length: {len(token)})")
print(f"Token starts with: {token[:10]}...")

try:
    handler = LogtailHandler(source_token=token)
    logger = logging.getLogger("test")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    # Test different log levels
    print("\nSending test logs to Better Stack...")
    logger.debug("TEST DEBUG: This is a debug message from test script")
    logger.info("TEST INFO: This is an info message from test script")
    logger.warning("TEST WARNING: This is a warning message from test script")
    logger.error("TEST ERROR: This is an error message from test script")
    logger.critical("TEST CRITICAL: This is a critical message from test script")
    
    # Force flush
    handler.flush()
    
    print("\n✓ Logs sent! Check your Better Stack dashboard now.")
    print("  (It may take 10-30 seconds to appear)")
    
except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

