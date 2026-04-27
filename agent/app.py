#!/usr/bin/env python3
"""
Daily Reflection Agent — deterministic tree walker.
No LLM calls at runtime. Loads reflection-tree.json and walks it.

Usage:
    python agent.py
    python agent.py --tree path/to/reflection-tree.json
"""

import json
import sys
import os
import argparse
import time
import re
from typing import Optional

# ── Terminal helpers ───────────────────────────────────────────────────────────

RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
ITALIC = "\033[3m"

BLUE   = "\033[94m"
GREEN  = "\033[92m"
PURPLE = "\033[95m"
AMBER  = "\033[93m"
GRAY   = "\033[90m"

AXIS_COLORS = {1: BLUE, 2: GREEN, 3: PURPLE}

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def hr(char="─", width=60, color=GRAY):
    print(f"{color}{char * width}{RESET}")

def print_label(text: str, color: str = GRAY):
    print(f"\n{color}{DIM}{text.upper()}{RESET}")

def print_text(text: str, indent: int = 0):
    prefix = " " * indent
    width = 60
    words = text.split(" ")
    line = prefix
    for word in words:
        # Handle newlines in text
        if "\n" in word:
            parts = word.split("\n")
            for i, part in enumerate(parts):
                if line.strip():
                    print(line)
                line = prefix + part + (" " if part else "")
                if i < len(parts) - 1 and part == "":
                    print()
            continue
        if len(line) + len(word) + 1 > width:
            print(line)
            line = prefix + word + " "
        else:
            line += word + " "
    if line.strip():
        print(line)

def slow_print(text: str, delay: float = 0.012):
    """Print text character by character for a reflective feel."""
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        if ch in ".!?\n":
            time.sleep(delay * 6)
        elif ch == ",":
            time.sleep(delay * 3)
        else:
            time.sleep(delay)
    print()

def pause(seconds: float = 1.2):
    time.sleep(seconds)

def prompt_continue():
    print(f"\n{GRAY}  [ press enter to continue ]{RESET}", end="")
    input()

# ── State ─────────────────────────────────────────────────────────────────────

class SessionState:
    def __init__(self):
        self.answers: dict[str, str] = {}
        self.signals: dict[str, dict[str, int]] = {
            "axis1": {"internal": 0, "external": 0},
            "axis2": {"contribution": 0, "entitlement": 0},
            "axis3": {"alto": 0, "self": 0},
        }

    def record_signal(self, signal: Optional[str]):
        if not signal:
            return
        axis, pole = signal.split(":")
        self.signals[axis][pole] += 1

    def dominant(self, axis: str) -> str:
        poles = self.signals[axis]
        return max(poles, key=lambda k: poles[k])

    def interpolate(self, text: str) -> str:
        """Replace {NODE_ID} placeholders with recorded answers."""
        def replace(match):
            key = match.group(1)
            if "." in key:
                axis, prop = key.split(".")
                if prop == "dominant":
                    return self.dominant(axis)
            return self.answers.get(key, key)
        return re.sub(r"\{([^}]+)\}", replace, text)

# ── Tree ──────────────────────────────────────────────────────────────────────

class ReflectionTree:
    def __init__(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.nodes = {n["id"]: n for n in data}

    def get(self, node_id: str) -> dict:
        if node_id not in self.nodes:
            raise KeyError(f"Node '{node_id}' not found in tree.")
        return self.nodes[node_id]

    def next_node(self, node: dict, state: SessionState) -> Optional[str]:
        """Resolve the next node ID from a node and current state."""
        # Explicit target always wins (non-decision nodes)
        if node.get("target"):
            return node["target"]

        # Decision routing
        if node["type"] == "decision":
            for route in node.get("routing", []):
                if route.get("alwaysMatch"):
                    return route["target"]
                src = route.get("matchSource")
                vals = route.get("matchValues", [])
                if src and state.answers.get(src) in vals:
                    return route["target"]

        return None

# ── Renderers ─────────────────────────────────────────────────────────────────

def render_start(node: dict, state: SessionState):
    clear()
    hr("─")
    pause(0.3)
    print()
    slow_print("  " + state.interpolate(node["text"]).replace("\n", "\n  "))
    pause(1.0)
    prompt_continue()

def render_bridge(node: dict, state: SessionState):
    clear()
    hr("╌", color=GRAY)
    print()
    slow_print(f"  {ITALIC}{GRAY}{state.interpolate(node['text'])}{RESET}")
    pause(1.4)

def render_question(node: dict, state: SessionState) -> str:
    clear()
    axis = node.get("axis")
    color = AXIS_COLORS.get(axis, GRAY)

    if axis:
        print_label(f"axis {axis}", color)
    else:
        print_label("opening", GRAY)

    hr("─", color=color)
    print()
    slow_print("  " + state.interpolate(node["text"]), delay=0.010)
    print()
    hr("╌", color=GRAY)

    options = node["options"]
    letters = "ABCDE"
    for i, opt in enumerate(options):
        print(f"\n  {BOLD}{color}{letters[i]}{RESET}  {opt}")

    print()
    hr("╌", color=GRAY)

    while True:
        raw = input(f"\n  {GRAY}Your choice (A–{letters[len(options)-1]}): {RESET}").strip().upper()
        if raw in letters[:len(options)]:
            idx = letters.index(raw)
            chosen = options[idx]
            print(f"\n  {DIM}→ {chosen}{RESET}")
            pause(0.4)
            return chosen
        print(f"  {AMBER}Please enter one of: {', '.join(letters[:len(options)])}{RESET}")

def render_reflection(node: dict, state: SessionState):
    clear()
    axis = node.get("axis")
    color = AXIS_COLORS.get(axis, GRAY)

    print_label("reflection", color)
    hr("─", color=color)
    print()

    text = state.interpolate(node["text"])
    paragraphs = text.split("\n\n")
    for para in paragraphs:
        slow_print("  " + para.strip(), delay=0.011)
        print()

    prompt_continue()

def render_summary(node: dict, state: SessionState):
    clear()
    print_label("your day", AMBER)
    hr("═", color=AMBER)

    segs = node["summarySegments"]
    print(f"\n  {DIM}{segs['intro']}{RESET}\n")

    axis_meta = [
        ("axis1", "Agency",       BLUE,   1),
        ("axis2", "Contribution", GREEN,  2),
        ("axis3", "Radius",       PURPLE, 3),
    ]

    for axis_key, label, color, _ in axis_meta:
        pole = state.dominant(axis_key)
        text = segs[axis_key][pole]
        hr("╌", color=color)
        print(f"\n  {BOLD}{color}{label}{RESET}")
        slow_print("  " + text, delay=0.009)
        print()

    hr("─", color=AMBER)
    print(f"\n  {ITALIC}{GRAY}{segs['closing']}{RESET}\n")
    hr("═", color=AMBER)
    pause(0.5)
    prompt_continue()

def render_end(node: dict, state: SessionState):
    clear()
    hr("─")
    print()
    slow_print(f"  {ITALIC}{GRAY}{node['text']}{RESET}")
    print()
    hr("─")
    pause(0.5)

# ── Engine ────────────────────────────────────────────────────────────────────

RENDERERS = {
    "start":      render_start,
    "bridge":     render_bridge,
    "question":   render_question,
    "reflection": render_reflection,
    "summary":    render_summary,
    "end":        render_end,
}

def run_session(tree: ReflectionTree):
    state = SessionState()
    current_id = "START"

    while current_id:
        node = tree.get(current_id)
        ntype = node["type"]

        if ntype == "decision":
            # Invisible — record signal if any, then route
            state.record_signal(node.get("signal"))
            current_id = tree.next_node(node, state)
            continue

        renderer = RENDERERS.get(ntype)
        if not renderer:
            print(f"[unknown node type: {ntype}] — skipping")
            current_id = tree.next_node(node, state)
            continue

        # Render and collect answer if question
        if ntype == "question":
            answer = renderer(node, state)
            state.answers[node["id"]] = answer
        else:
            renderer(node, state)

        # Record signal after rendering
        state.record_signal(node.get("signal"))

        current_id = tree.next_node(node, state)

    return state

# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Daily Reflection Agent")
    parser.add_argument(
        "--tree",
        default="reflection-tree.json",
        help="Path to the tree JSON file (default: reflection-tree.json)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.tree):
        print(f"Error: tree file not found at '{args.tree}'")
        sys.exit(1)

    try:
        tree = ReflectionTree(args.tree)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error loading tree: {e}")
        sys.exit(1)

    try:
        run_session(tree)
    except KeyboardInterrupt:
        print(f"\n\n{GRAY}Session ended early. See you tomorrow.{RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()