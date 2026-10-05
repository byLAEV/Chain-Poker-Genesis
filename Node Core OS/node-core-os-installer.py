#!/usr/bin/env python3
"""First-stage Linux terminal installer for Node Core OS.

This installer establishes the Node Core OS terminal entry point.
The first stage intentionally provides only the main architectural menu.
"""

from __future__ import annotations


def print_main_menu() -> None:
    print("Trilema Project Presents")
    print("Node Core Network by LAEV")
    print("& The Chain Poker Genesis Protocol")
    print()
    print("[In Memory of Satoshi Nakamoto's Legacy,")
    print("Trilema.com (MP), Hannah Wiggins (Hanbot),")
    print("Lerry Alexander (LAEV) & The Bitcoin Network]")
    print()
    print()
    print("---")
    print()
    print("1. Node Core BIOS")
    print()
    print("2. Node Core")
    print()
    print("3. Protocols")
    print()
    print("4. Exit")


def run() -> int:
    print_main_menu()

    while True:
        try:
            choice = input().strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if choice == "4":
            print("Exiting.")
            return 0

        if choice in {"1", "2", "3"}:
            print()
            print("This Node Core OS section is not implemented yet.")
            print()
            print_main_menu()
            continue

        print()
        print("Please select 1, 2, 3, or 4.")
        print()
        print_main_menu()


if __name__ == "__main__":
    raise SystemExit(run())
