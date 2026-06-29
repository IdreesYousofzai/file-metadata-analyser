"""Shared output formatting helpers for the CLI."""

WIDTH = 60


def print_header(title: str) -> None:
    print()
    print("=" * WIDTH)
    print(f" {title}".upper())
    print("=" * WIDTH)


def print_fields(data: dict) -> None:
    """Print a dict of metadata fields neatly aligned as 'key : value'."""
    if not data:
        print("  (no metadata found)")
        return

    max_key_len = max(len(key) for key in data.keys())
    for key, value in data.items():
        print(f"  {key.ljust(max_key_len)} : {value}")
    print("-" * WIDTH)


def print_error(message: str) -> None:
    print(f"\n  [!] {message}\n")
