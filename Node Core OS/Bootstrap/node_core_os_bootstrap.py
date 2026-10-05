#!/usr/bin/env python3
"""Node Core OS terminal bootstrap.

First-stage responsibility:
    Start the Node Core OS terminal interface and present its main menu.

This bootstrap intentionally does not implement the internal BIOS, Node Core,
or Protocols menus yet. Those are subsequent implementation stages.
"""

from __future__ import annotations

import sys


def display_main_menu() -> None:
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
    print()
    print("2. Node Core")
    print()
    print()
    print("3. Protocols")
    print()
    print()
    print("4. Exit")


def main() -> int:
    display_main_menu()

    while True:
        try:
            choice = input().strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if choice == "4":
            return 0

        if choice in {"1", "2", "3"}:
            print()
            print("This Node Core OS section is not implemented yet.")
            print()
            display_main_menu()
            continue

        print()
        print("Please select 1, 2, 3, or 4.")
        print()
        display_main_menu()


if __name__ == "__main__":
    sys.exit(main())
