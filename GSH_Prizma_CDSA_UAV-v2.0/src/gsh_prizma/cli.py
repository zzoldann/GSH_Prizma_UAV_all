import argparse
from .ui.app import run as run_gui

def main():
    p = argparse.ArgumentParser(prog="prizma-cdsa", description="GSH Prizma CDSA UAV")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("gui", help="Запустить GUI")
    args = p.parse_args()
    if args.cmd in (None, "gui"):
        run_gui()
    else:
        p.print_help()
