#!/usr/bin/env python3
"""
ZMK Keyboard Manager - Interactive CLI for Offsetkey keyboard
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Check dependencies
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich import box
except ImportError:
    print("Missing 'rich' library. Install with: pipx install rich")
    sys.exit(1)

# Constants - resolve symlinks to get actual repo location
REPO_DIR = Path(__file__).resolve().parent
CONFIG_DIR = REPO_DIR / "config"
KEYMAP_FILE = CONFIG_DIR / "offsetkey.keymap"
CONF_FILE = CONFIG_DIR / "offsetkey.conf"
DRAWER_CONFIG = REPO_DIR / "keymap_drawer.config.yaml"
PHYSICAL_LAYOUT = REPO_DIR / "boards" / "shields" / "offsetkey" / "offsetkey_physical_layout.dtsi"
SVG_OUTPUT = REPO_DIR / "keymap-drawer" / "offsetkey.svg"
YAML_OUTPUT = REPO_DIR / "keymap-drawer" / "offsetkey.yaml"
ZMK_REFERENCE = REPO_DIR / "docs" / "zmk-reference.md"

console = Console()


def header() -> None:
    """Display the header."""
    console.clear()
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]⌨  ZMK Keyboard Manager[/bold cyan]\n"
            "[dim]Offsetkey • Eyelash Nano • Split[/dim]",
            border_style="cyan",
            padding=(0, 2),
        )
    )
    console.print()


def show_menu() -> None:
    """Display the main menu."""
    table = Table(
        show_header=False,
        box=box.ROUNDED,
        border_style="dim cyan",
        padding=(0, 2),
    )
    table.add_column("Key", style="bold yellow", width=5)
    table.add_column("Action", style="white")

    menu_items = [
        ("1", "Regenerate keymap diagram"),
        ("2", "Open keymap diagram (SVG)"),
        ("3", "Edit keymap (.keymap) [dim]+ reference[/dim]"),
        ("4", "Edit config (.conf)"),
        ("5", "Show layer summary"),
        ("6", "Show current settings"),
        ("r", "View ZMK reference"),
        ("─", "───────────────────────────────────"),
        ("g", "Git: commit & push changes"),
        ("a", "Open GitHub Actions (firmware download)"),
        ("─", "───────────────────────────────────"),
        ("q", "Quit"),
    ]

    for key, action in menu_items:
        if key == "─":
            table.add_row("[dim]─[/dim]", f"[dim]{action}[/dim]")
        else:
            table.add_row(f"\\[{key}]", action)

    console.print(table)
    console.print()


def regenerate_svg() -> None:
    """Regenerate the keymap SVG diagram using two-step process: parse then draw."""
    console.print("[cyan]→[/cyan] Regenerating keymap diagram...")

    try:
        # Step 1: Parse ZMK keymap to YAML
        # Note: -c/--config goes BEFORE the subcommand (it's a global option)
        console.print("[dim]  Parsing keymap...[/dim]")
        parse_result = subprocess.run(
            [
                "keymap",
                "-c", str(DRAWER_CONFIG),
                "parse",
                "-z", str(KEYMAP_FILE),
            ],
            capture_output=True,
            text=True,
            cwd=REPO_DIR,
        )

        if parse_result.returncode != 0:
            console.print(f"[red]✗[/red] Parse error: {parse_result.stderr}")
            return

        # Save intermediate YAML
        YAML_OUTPUT.parent.mkdir(exist_ok=True)
        YAML_OUTPUT.write_text(parse_result.stdout)

        # Step 2: Draw SVG from YAML
        # Use -d to specify the DTS physical layout file for custom keyboards
        console.print("[dim]  Drawing SVG...[/dim]")
        draw_cmd = [
            "keymap",
            "-c", str(DRAWER_CONFIG),
            "draw",
        ]
        # Add physical layout if available
        if PHYSICAL_LAYOUT.exists():
            draw_cmd.extend(["-d", str(PHYSICAL_LAYOUT)])
        draw_cmd.append(str(YAML_OUTPUT))

        draw_result = subprocess.run(
            draw_cmd,
            capture_output=True,
            text=True,
            cwd=REPO_DIR,
        )

        if draw_result.returncode == 0:
            SVG_OUTPUT.write_text(draw_result.stdout)
            console.print(f"[green]✓[/green] Saved to [dim]{SVG_OUTPUT.relative_to(REPO_DIR)}[/dim]")
        else:
            console.print(f"[red]✗[/red] Draw error: {draw_result.stderr}")
    except FileNotFoundError:
        console.print("[red]✗[/red] 'keymap' command not found. Install with: [dim]pipx install keymap-drawer[/dim]")


def open_svg() -> None:
    """Open the SVG in the default viewer."""
    if not SVG_OUTPUT.exists():
        console.print("[yellow]⚠[/yellow] SVG not found. Regenerating first...")
        regenerate_svg()

    if SVG_OUTPUT.exists():
        console.print(f"[cyan]→[/cyan] Opening [dim]{SVG_OUTPUT.name}[/dim]...")
        subprocess.run(["xdg-open", str(SVG_OUTPUT)], stderr=subprocess.DEVNULL)
        console.print("[green]✓[/green] Opened in browser")


# Editor configurations: (split_args, wait_arg, supports_split)
EDITORS: dict[str, tuple[list[str] | None, str | None, bool]] = {
    "nvim": (["-O"], None, True),
    "vim": (["-O"], None, True),
    "vi": (["-O"], None, True),
    "zed": (None, "--wait", True),
    "code": (None, "--wait", True),
    "hx": (None, None, True),
    "emacs": (None, None, True),
    "nano": (None, None, False),
}


def get_editor() -> str:
    """Get the user's preferred editor."""
    if editor := os.environ.get("EDITOR"):
        return editor
    for ed in ("zed", "code", "nvim", "vim", "nano"):
        if shutil.which(ed):
            return ed
    return "nano"


def edit_file(filepath: Path, description: str, *, with_reference: bool = False) -> None:
    """Open a file in the user's editor, optionally with reference doc."""
    editor = get_editor()
    editor_name = Path(editor).name
    split_args, wait_arg, supports_split = EDITORS.get(editor_name, (None, None, True))

    files = [str(filepath)]
    if with_reference and ZMK_REFERENCE.exists():
        if supports_split:
            files.insert(0, str(ZMK_REFERENCE))
            console.print(f"[cyan]→[/cyan] Opening {description} + reference in [dim]{editor_name}[/dim]...")
        else:
            console.print(f"[dim]  Reference: {ZMK_REFERENCE}[/dim]")
            console.print(f"[cyan]→[/cyan] Opening {description} in [dim]{editor_name}[/dim]...")
    else:
        console.print(f"[cyan]→[/cyan] Opening {description} in [dim]{editor_name}[/dim]...")

    cmd = [editor]
    if split_args and len(files) > 1:
        cmd.extend(split_args)
    if wait_arg:
        cmd.append(wait_arg)
    cmd.extend(files)

    subprocess.run(cmd)
    console.print("[green]✓[/green] Editor closed")


def parse_layers() -> list[dict]:
    """Parse layer definitions from keymap file.

    ZMK keymap structure:
        keymap {
            compatible = "zmk,keymap";

            layer_name {
                bindings = <...>;
                label = "LABEL";  // optional
            };
        };
    """
    content = KEYMAP_FILE.read_text()
    layers = []

    # Parse #define macros for layer indices (e.g., #define BASE 0)
    layer_defines = {}
    for match in re.finditer(r'#define\s+(\w+)\s+(\d+)', content):
        layer_defines[match.group(1)] = int(match.group(2))

    # Find the keymap block
    keymap_match = re.search(r'keymap\s*\{[^}]*compatible\s*=\s*"zmk,keymap"\s*;(.+)', content, re.DOTALL)
    if not keymap_match:
        return layers

    keymap_content = keymap_match.group(1)

    # Find layer blocks - match layer_name { ... }; pattern
    # Use a more robust approach: find each layer block by matching balanced braces
    layer_pattern = r'(\w+)\s*\{((?:[^{}]|\{[^{}]*\})*)\}'
    matches = re.finditer(layer_pattern, keymap_content, re.DOTALL)

    for match in matches:
        node_name = match.group(1)
        layer_content = match.group(2)

        # Skip non-layer blocks (like behaviors, combos)
        if 'bindings' not in layer_content:
            continue

        # Extract bindings
        bindings_match = re.search(r'bindings\s*=\s*<([^>]+)>', layer_content, re.DOTALL)
        if not bindings_match:
            continue

        bindings = bindings_match.group(1)

        # Extract optional label
        label_match = re.search(r'label\s*=\s*"([^"]+)"', layer_content)
        label = label_match.group(1) if label_match else None

        # Count key bindings by counting '&' prefixed behaviors
        keys = re.findall(r'&\w+', bindings)
        key_count = len(keys)

        # Determine display name and index
        display_name = label if label else node_name
        layer_idx = layer_defines.get(display_name, layer_defines.get(node_name, len(layers)))

        layers.append({
            'name': display_name,
            'node': node_name,
            'index': layer_idx,
            'key_count': key_count,
        })

    # Sort by index
    layers.sort(key=lambda x: x['index'])
    return layers


def show_layers() -> None:
    """Display a summary of layers parsed from keymap file."""
    console.print("[cyan]→[/cyan] Parsing keymap...")

    layers = parse_layers()

    if not layers:
        console.print("[yellow]⚠[/yellow] No layers found in keymap")
        return

    table = Table(
        title="Layers",
        box=box.ROUNDED,
        border_style="cyan",
    )
    table.add_column("Index", style="yellow", justify="center", width=5)
    table.add_column("Name", style="bold cyan")
    table.add_column("Node", style="dim")
    table.add_column("Keys", style="white", justify="right")

    for layer in layers:
        table.add_row(
            str(layer['index']),
            layer['name'],
            layer['node'] if layer['node'] != layer['name'] else "",
            str(layer['key_count']),
        )

    console.print(table)
    console.print()

    # Parse and show combos
    content = KEYMAP_FILE.read_text()
    combos = parse_combos(content)
    if combos:
        combo_table = Table(
            title="Combos",
            box=box.ROUNDED,
            border_style="yellow",
        )
        combo_table.add_column("Name", style="yellow")
        combo_table.add_column("Keys", style="white")
        combo_table.add_column("Action", style="cyan")

        for combo in combos:
            combo_table.add_row(combo['name'], combo['keys'], combo['action'])

        console.print(combo_table)


def parse_combos(content: str) -> list:
    """Parse combo definitions from keymap content."""
    combos = []

    # Find combos block
    combos_match = re.search(r'combos\s*\{[^}]*compatible\s*=\s*"zmk,combos"\s*;(.+?)\n\s*\};', content, re.DOTALL)
    if not combos_match:
        return combos

    combos_content = combos_match.group(1)

    # Find individual combo definitions
    combo_pattern = r'(\w+)\s*\{[^{}]*bindings\s*=\s*<([^>]+)>[^{}]*key-positions\s*=\s*<([^>]+)>[^{}]*\}'
    for match in re.finditer(combo_pattern, combos_content, re.DOTALL):
        name = match.group(1)
        action = match.group(2).strip()
        keys = match.group(3).strip()

        combos.append({
            'name': name,
            'action': action,
            'keys': keys,
        })

    return combos


def show_settings() -> None:
    """Display current keyboard settings from .conf file."""
    console.print("[cyan]→[/cyan] Reading config...")

    content = CONF_FILE.read_text()

    def get_setting(pattern, default="?"):
        match = re.search(pattern, content)
        return match.group(1) if match else default

    table = Table(
        title="Keyboard Settings",
        box=box.ROUNDED,
        border_style="cyan",
    )
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="bold white")
    table.add_column("Notes", style="dim")

    # Parse and display settings
    sleep_timeout = int(get_setting(r'CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=(\d+)', '3600000'))
    idle_timeout = int(get_setting(r'CONFIG_ZMK_IDLE_TIMEOUT=(\d+)', '15000'))

    table.add_row("Sleep timeout", f"{sleep_timeout // 60000} min", "Deep sleep")
    table.add_row("Idle timeout", f"{idle_timeout // 1000} sec", "Screen off")
    table.add_row("Display", get_setting(r'CONFIG_ZMK_DISPLAY=(\w)', 'n'), "OLED enabled")
    table.add_row("RGB Underglow", get_setting(r'CONFIG_ZMK_RGB_UNDERGLOW=(\w)', 'n'), "LED strip")
    table.add_row("RGB on start", get_setting(r'CONFIG_ZMK_RGB_UNDERGLOW_ON_START=(\w)', 'n'), "")
    table.add_row("Pointing device", get_setting(r'CONFIG_ZMK_POINTING=(\w)', 'n'), "Trackpoint")
    table.add_row("Debounce (press)", f"{get_setting(r'CONFIG_ZMK_KSCAN_DEBOUNCE_PRESS_MS=(\d+)', '5')} ms", "")
    table.add_row("Debounce (release)", f"{get_setting(r'CONFIG_ZMK_KSCAN_DEBOUNCE_RELEASE_MS=(\d+)', '5')} ms", "")
    table.add_row("BT TX Power", "+8 dBm" if "TX_PWR_PLUS_8=y" in content else "default", "Range")

    console.print(table)


def git_commit_push() -> None:
    """Commit and push changes to GitHub."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True, cwd=REPO_DIR,
    )

    if not result.stdout.strip():
        console.print("[yellow]⚠[/yellow] No changes to commit")
        return

    console.print("[cyan]→[/cyan] Changed files:")
    for line in result.stdout.strip().split('\n'):
        status, filepath = line[:2], line[3:]
        color = "green" if "A" in status else "yellow" if "M" in status else "red"
        console.print(f"  [{color}]{status}[/{color}] {filepath}")
    console.print()

    if not Confirm.ask("Commit and push these changes?"):
        console.print("[dim]Cancelled[/dim]")
        return

    msg = Prompt.ask("Commit message", default="Update keymap")

    console.print("[cyan]→[/cyan] Committing...")
    subprocess.run(["git", "add", "-A"], check=True, cwd=REPO_DIR)
    subprocess.run(["git", "commit", "-m", msg], check=True, cwd=REPO_DIR)

    console.print("[cyan]→[/cyan] Pushing to GitHub...")
    result = subprocess.run(["git", "push"], capture_output=True, text=True, cwd=REPO_DIR)

    if result.returncode == 0:
        console.print("[green]✓[/green] Pushed! GitHub Actions will build firmware.")
        console.print("[dim]  Download from: Actions → latest run → firmware artifact[/dim]")
    else:
        console.print(f"[red]✗[/red] Push failed: {result.stderr}")


def open_github_actions() -> None:
    """Open the GitHub Actions page."""
    # Get remote URL
    result = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )

    remote = result.stdout.strip()

    # Convert to HTTPS URL
    if remote.startswith("git@"):
        # git@github.com:user/repo.git -> https://github.com/user/repo
        remote = remote.replace("git@github.com:", "https://github.com/").replace(".git", "")
    elif remote.endswith(".git"):
        remote = remote[:-4]

    actions_url = f"{remote}/actions"
    console.print(f"[cyan]→[/cyan] Opening [dim]{actions_url}[/dim]")
    subprocess.run(["xdg-open", actions_url], stderr=subprocess.DEVNULL)
    console.print("[green]✓[/green] Opened in browser")


def main() -> None:
    """Main loop."""
    while True:
        header()
        show_menu()

        choice = Prompt.ask(
            "Select",
            choices=["1", "2", "3", "4", "5", "6", "r", "g", "a", "q"],
            show_choices=False,
        )

        console.print()

        if choice == "1":
            regenerate_svg()
        elif choice == "2":
            open_svg()
        elif choice == "3":
            edit_file(KEYMAP_FILE, "keymap", with_reference=True)
        elif choice == "4":
            edit_file(CONF_FILE, "config")
        elif choice == "5":
            show_layers()
        elif choice == "6":
            show_settings()
        elif choice == "r":
            edit_file(ZMK_REFERENCE, "ZMK reference")
        elif choice == "g":
            git_commit_push()
        elif choice == "a":
            open_github_actions()
        elif choice == "q":
            console.print("[dim]Goodbye![/dim]")
            break

        if choice != "q":
            console.print()
            Prompt.ask("[dim]Press Enter to continue[/dim]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[dim]Interrupted[/dim]")
