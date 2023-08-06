1.1.0 (released 2020-08-26)
---------------------------

- Fixed deprecation warnings when running under Python 3.6+
- Added SameSite attribute for cookies

1.0.0 (released 2020-01-15)
---------------------------

- Dropped Python 2.7 support
- Bugfix: allow sessions to be saved when empty

0.2 (released 2018-03-12)
-------------------------

- Added JSON serializer
- Bugfix: session ids ending in periods are no longer silently dropped
- Only set a session id cookie when new session are created or when the id has
  changed, avoiding unnecessary Set-Cookie headers being sent.

0.1
----

- Initial release
