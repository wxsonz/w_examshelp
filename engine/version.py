"""The one place the version number is written down.

It lives in its own module so the update check can fetch just this file from the
repository -- a few hundred bytes -- instead of downloading the renderer to read
one string out of it.
"""

VERSION = "v0.6.0"
