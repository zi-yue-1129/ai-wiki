#!/usr/bin/env python3
"""Compatibility entry point for the source-based recommender checks."""
from test_recommender_new_motion_semantics import check
if __name__ == "__main__":
    check()
    print("OK: item-CF and NeuMF source semantics")
