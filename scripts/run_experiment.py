#!/usr/bin/env python3
"""Thin repository entry point for the canonical Python CLI."""

from tahmures.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["run", *__import__("sys").argv[1:]]))
