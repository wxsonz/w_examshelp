#!/usr/bin/env python3
import sys
import os
import argparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.state import StateManager
from engine.evaluator import Evaluator
from engine.ui.terminal import TerminalUI

def run_interactive_loop(state_mgr, evaluator, ui):
    session_name = state_mgr.get_session_name()
    ui.print_banner(session_name)
    ui.console.print("[dim white]Type [bold cyan]status[/bold cyan], [bold cyan]grademe[/bold cyan], [bold cyan]subject[/bold cyan], [bold cyan]hint[/bold cyan], [bold cyan]skip[/bold cyan], [bold cyan]history[/bold cyan], [bold cyan]reset[/bold cyan], [bold cyan]list[/bold cyan], or [bold cyan]exit[/bold cyan].[/dim white]\n")
    
    # Show initial status on launch
    ui.display_status(state_mgr.get_progress_data())

    while True:
        try:
            cmd = input(f"\n[examshelp ({session_name})]> ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            ui.console.print("\n[yellow]Archiving session...[/yellow]")
            folder, meta = state_mgr.archive_current_session(clean_workspace=True)
            ui.display_archive_exit(meta["session_name"], folder)
            break

        if not cmd:
            continue

        if cmd in ["exit", "quit"]:
            folder, meta = state_mgr.archive_current_session(clean_workspace=True)
            ui.display_archive_exit(meta["session_name"], folder)
            ui.console.print("[bold cyan]Goodbye! All code and subjects archived safely. ⚡[/bold cyan]")
            break
        elif cmd == "status":
            ui.display_status(state_mgr.get_progress_data())
        elif cmd == "subject":
            ui.display_subject(state_mgr.get_current_exercise())
        elif cmd == "grademe":
            ex = state_mgr.get_current_exercise()
            if not ex:
                ui.console.print("[bold red]No active exercise found![/bold red]")
                continue
                
            ui.console.print(f"[bold cyan]Compiling and grading `rendu/{ex['name']}/{ex['expected_files']}`...[/bold cyan]")
            ui.console.print(f"[dim](Hint: No `git push` needed. Just save your file and run grademe!)[/dim]")
            result = evaluator.evaluate(ex)
            ui.display_eval_result(result)
            
            if result["success"]:
                state_mgr.complete_current_exercise()
        elif cmd == "hint":
            ex = state_mgr.get_current_exercise()
            ui.display_hints(ex)
        elif cmd == "skip":
            old_name, new_ex = state_mgr.skip_current_exercise()
            ui.display_skip(old_name, new_ex)
        elif cmd == "reset":
            state_mgr.reset_all_progress()
            session_name = state_mgr.get_session_name()
            ui.display_reset(state_mgr.get_current_exercise())
        elif cmd in ["history", "sessions"]:
            sessions = state_mgr.session_mgr.list_saved_sessions()
            ui.display_sessions_history(sessions)
        elif cmd == "list":
            ui.display_exercise_list(state_mgr.db, state_mgr.state)
        elif cmd == "help":
            ui.console.print("[bold cyan]Available Commands:[/bold cyan]")
            ui.console.print("  [bold green]status[/bold green]   - Show active session, level progress bar & assignment details")
            ui.console.print("  [bold green]grademe[/bold green]  - Compile and test your solution in `rendu/`")
            ui.console.print("  [bold green]subject[/bold green]  - Print current exercise assignment subject")
            ui.console.print("  [bold green]hint[/bold green]     - View targeted advice on what to look out for")
            ui.console.print("  [bold green]skip[/bold green]     - Skip the current question and advance to the next exercise")
            ui.console.print("  [bold green]history[/bold green]  - View all past saved sessions in `history/`")
            ui.console.print("  [bold green]reset[/bold green]    - Reset all progress back to Level 0 and 0 completed")
            ui.console.print("  [bold green]list[/bold green]     - List all 10 levels and unlocked exercises")
            ui.console.print("  [bold green]exit[/bold green]     - Save and archive session to `history/<session_name>` and quit")
        else:
            ui.console.print(f"[red]Unknown command: `{cmd}`. Type `help` for available commands.[/red]")

def main():
    parser = argparse.ArgumentParser(description="ExamsHelp CLI (Antigravity Edition)")
    parser.add_argument("command", nargs="?", choices=["status", "grademe", "subject", "hint", "skip", "history", "sessions", "reset", "list"], help="CLI command to execute")
    args = parser.parse_args()

    state_mgr = StateManager()
    evaluator = Evaluator()
    ui = TerminalUI()

    if args.command:
        if args.command == "status":
            ui.display_status(state_mgr.get_progress_data())
        elif args.command == "subject":
            ui.display_subject(state_mgr.get_current_exercise())
        elif args.command == "grademe":
            ex = state_mgr.get_current_exercise()
            if ex:
                ui.console.print(f"[bold cyan]Compiling and grading `rendu/{ex['name']}/{ex['expected_files']}`...[/bold cyan]")
                ui.console.print(f"[dim](Hint: No `git push` needed. Just save your file and run grademe!)[/dim]")
                result = evaluator.evaluate(ex)
                ui.display_eval_result(result)
                if result["success"]:
                    state_mgr.complete_current_exercise()
        elif args.command == "hint":
            ex = state_mgr.get_current_exercise()
            ui.display_hints(ex)
        elif args.command == "skip":
            old_name, new_ex = state_mgr.skip_current_exercise()
            ui.display_skip(old_name, new_ex)
        elif args.command == "reset":
            state_mgr.reset_all_progress()
            ui.display_reset(state_mgr.get_current_exercise())
        elif args.command in ["history", "sessions"]:
            sessions = state_mgr.session_mgr.list_saved_sessions()
            ui.display_sessions_history(sessions)
        elif args.command == "list":
            ui.display_exercise_list(state_mgr.db, state_mgr.state)
    else:
        run_interactive_loop(state_mgr, evaluator, ui)

if __name__ == "__main__":
    main()
