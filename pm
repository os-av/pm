#!/usr/bin/env python3

"""
Entry point for CLI application.
"""

from cli import cli

def main():
    run = cli.CLI()
    run.run()

if __name__ == "__main__":
    main()
