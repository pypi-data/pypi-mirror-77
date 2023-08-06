# lrucli

A command line client that provides python's `lru_cache` to the terminal for inline deduping repeated lines coming through stdin.

This is helpful when you want to see a deduped view of some long input stream but don't want to wait for something like `sort | uniq`.
