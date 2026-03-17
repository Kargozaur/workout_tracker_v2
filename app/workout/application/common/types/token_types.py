from typing import NewType


AccessToken = NewType("AccessToken", str)
"""Access Token type for the dishka."""

RefreshToken = NewType("RefreshToken", str)
"""Refresh Token type for the dishka."""
