"""
Tests for utils/auth.py
Only covers hash_password(), which is pure and needs no database connection.
register_user/login_user/etc. require a live MySQL connection and are out of
scope for this CI pipeline for now.
"""

from utils.auth import hash_password


def test_hash_password_is_deterministic():
    assert hash_password("mypassword") == hash_password("mypassword")


def test_hash_password_differs_for_different_input():
    assert hash_password("mypassword") != hash_password("otherpassword")


def test_hash_password_is_sha256_hex():
    result = hash_password("test123")
    assert len(result) == 64
    int(result, 16)  # raises ValueError if not valid hex
