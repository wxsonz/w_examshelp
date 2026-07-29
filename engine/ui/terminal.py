from rich.console import Console
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.table import Table
from rich.text import Text
from rich.syntax import Syntax
from engine.ui.themes import EXAMSHELP_THEME
from engine.hints import HintEngine

VERSION_STRING = "v0.1.0-alpha"

class TerminalUI:
    def __init__(self):
        self.console = Console(theme=EXAMSHELP_THEME)

    def print_banner(self, session_name=None):
        banner_text = """
 [bold cyan]███████╗██╗  ██╗██████╗ ███╗   ███╗███████╗██╗  ██╗███████╗██╗     ██████╗ [/bold cyan]
 [bold cyan]██╔════╝╚██╗██╔╝██╔══██╗████╗ ████║██╔════╝██║  ██║██╔════╝██║     ██╔══██╗[/bold cyan]
 [bold cyan]█████╗   ╚███╔╝ ██████╔╝██╔████╔██║███████╗███████║█████╗  ██║     ██████╔╝[/bold cyan]
 [bold cyan]██╔══╝   ██╔██╗ ██╔═══╝ ██║╚██╔╝██║╚════██║██╔══██║██╔══╝  ██║     ██╔═══╝ [/bold cyan]
 [bold cyan]███████╗██╔╝ ██╗██║     ██║ ╚═╝ ██║███████╗██║  ██║███████╗███████╗██║     [/bold cyan]
 [bold magenta]╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     [/bold magenta]
                 [bold yellow]⚡ Antigravity Edition — Educational Examshell ⚡[/bold yellow]
"""
        self.console.print(banner_text)
        if session_name:
            self.console.print(f" [bold magenta]🐾 Active Session:[/bold magenta] [bold yellow]{session_name}[/bold yellow]\n")

    def display_status(self, progress_data):
        session_name = progress_data.get("session_name", "active-session")
        curr_lvl = progress_data["current_level"]
        session_completed = progress_data.get("session_completed_count", 0)
        total_completions = progress_data.get("total_completions", 0)
        total = progress_data["total_count"]
        ex = progress_data["current_exercise"]
        
        level_blocks = ""
        for i in range(10):
            if i < curr_lvl:
                level_blocks += "[bold green]█[/bold green]"
            elif i == curr_lvl:
                level_blocks += "[bold yellow]▶[/bold yellow]"
            else:
                level_blocks += "[dim white]░[/dim white]"

        status_table = Table(show_header=False, box=None, padding=(0, 1))
        status_table.add_row("[bold magenta]Active Session:[/bold magenta]", f"[bold yellow]🐾 {session_name}[/bold yellow]")
        status_table.add_row("[bold magenta]Current Level:[/bold magenta]", f"[bold yellow]Level {curr_lvl}/9[/bold yellow]  [{level_blocks}]")
        status_table.add_row("[bold magenta]Session Progress:[/bold magenta]", f"[bold green]{session_completed}[/bold green] exercises completed in this session")
        status_table.add_row("[bold magenta]Cumulative Completions:[/bold magenta]", f"[bold cyan]{total_completions}[/bold cyan] total questions completed across sessions")
        
        if ex:
            source_type = ex.get("source_type", "42_official")
            track_label = "[bold yellow]🏆 Official 42 Exam[/bold yellow]" if source_type == "42_official" else "[bold cyan]⚡ ExamsHelp Extended (Custom)[/bold cyan]"
            status_table.add_row("[bold magenta]Exercise Track:[/bold magenta]", track_label)
            status_table.add_row("[bold magenta]Assignment Name:[/bold magenta]", f"[bold bright_white]{ex['name']}[/bold bright_white]")
            status_table.add_row("[bold magenta]Expected File:[/bold magenta]", f"[bold code]rendu/{ex['expected_files']}[/bold code]")
            status_table.add_row("[bold magenta]Allowed Functions:[/bold magenta]", f"[cyan]{ex['allowed_functions']}[/cyan]")
            if ex.get("prototype"):
                status_table.add_row("[bold magenta]Function Prototype:[/bold magenta]", f"[bold yellow]{ex['prototype']}[/bold yellow]")

        panel = Panel(
            status_table,
            title="[bold cyan]⚡ EXAMSHELP DASHBOARD ⚡[/bold cyan]",
            subtitle=f"[dim cyan]{VERSION_STRING}[/dim cyan]",
            subtitle_align="right",
            border_style="cyan"
        )
        self.console.print(panel)

    def display_subject(self, exercise_info):
        if not exercise_info:
            self.console.print("[yellow]No active exercise selected.[/yellow]")
            return

        source_type = exercise_info.get("source_type", "42_official")
        track_title = "🏆 42 Official Exam" if source_type == "42_official" else "⚡ ExamsHelp Extended Custom"
        subj_text = exercise_info.get("subject", "No subject text available.")
        panel = Panel(
            Text(subj_text, style="bright_white"),
            title=f"[bold cyan]SUBJECT: {exercise_info['name']} ({track_title} — Level {exercise_info.get('orig_level', 0)})[/bold cyan]",
            subtitle=f"[dim cyan]{VERSION_STRING}[/dim cyan]",
            subtitle_align="right",
            border_style="magenta"
        )
        self.console.print(panel)

    def display_eval_result(self, result):
        if result["success"]:
            msg = f"✨ [bold green]{result['message']}[/bold green]\n"
            msg += "[bold green]Level requirements met! New subject unlocked in `subjects/`![/bold green]"
            panel = Panel(
                msg,
                title="[bold green]PASSED - GRADEME SUCCESS[/bold green]",
                subtitle=f"[dim green]{VERSION_STRING}[/dim green]",
                subtitle_align="right",
                border_style="green"
            )
            self.console.print(panel)
        else:
            stage = result.get("stage", "eval")
            msg = f"[bold red]❌ {result['message']}[/bold red]\n"
            
            if "log" in result:
                msg += f"\n[dim red]Compiler Output:[/dim red]\n[yellow]{result['log']}[/yellow]\n"
                
            if "got" in result:
                msg += f"\n[dim yellow]Expected Output:[/dim yellow]\n[green]{repr(result['expected'])}[/green]\n"
                msg += f"[dim yellow]Your Output:[/dim yellow]\n[red]{repr(result['got'])}[/red]\n"

            panel = Panel(
                msg,
                title=f"[bold red]GRADEME FEEDBACK ({stage.upper()})[/bold red]",
                subtitle=f"[dim red]{VERSION_STRING}[/dim red]",
                subtitle_align="right",
                border_style="red"
            )
            self.console.print(panel)

            hints = result.get("hints", [])
            if hints:
                hint_text = ""
                for h in hints:
                    hint_text += f"• [cyan]{h}[/cyan]\n"
                hint_panel = Panel(
                    hint_text.strip(),
                    title="[bold yellow]💡 FRIENDLY HINT (0 PENALTY)[/bold yellow]",
                    border_style="yellow"
                )
                self.console.print(hint_panel)

    def display_hints(self, exercise_info):
        if not exercise_info:
            self.console.print("[yellow]No active exercise selected.[/yellow]")
            return
            
        hints = HintEngine.get_exercise_hints(exercise_info)
        hint_text = ""
        for h in hints:
            hint_text += f"• [cyan]{h}[/cyan]\n"
            
        panel = Panel(
            hint_text.strip(),
            title=f"[bold yellow]💡 WHAT TO LOOK OUT FOR: {exercise_info['name'].upper()}[/bold yellow]",
            subtitle=f"[dim yellow]{VERSION_STRING}[/dim yellow]",
            subtitle_align="right",
            border_style="yellow"
        )
        self.console.print(panel)

    def display_skip(self, old_name, new_ex):
        if new_ex:
            source_type = new_ex.get("source_type", "42_official")
            track_name = "Official 42 Exam" if source_type == "42_official" else "ExamsHelp Extended Custom"
            msg = f"[yellow]Skipped exercise [bold]{old_name}[/bold].[/yellow]\n"
            msg += f"[bold green]Now on exercise: [bright_white]{new_ex['name']}[/bright_white] ({track_name} — Level {new_ex.get('orig_level', 0)})[/bold green]\n"
            msg += f"[dim white]Updated `subjects/subject.txt` with new assignment specifications.[/dim white]"
            panel = Panel(
                msg,
                title="[bold yellow]⏩ EXERCISE SKIPPED[/bold yellow]",
                subtitle=f"[dim yellow]{VERSION_STRING}[/dim yellow]",
                subtitle_align="right",
                border_style="yellow"
            )
        else:
            panel = Panel(
                "[yellow]Skipped exercise. All exercises in curriculum completed![/yellow]",
                title="[bold yellow]⏩ EXERCISE SKIPPED[/bold yellow]",
                subtitle=f"[dim yellow]{VERSION_STRING}[/dim yellow]",
                subtitle_align="right",
                border_style="yellow"
            )
        self.console.print(panel)

    def display_reset(self, new_ex):
        msg = f"[bold green]All progress reset to Level 0![/bold green]\n"
        if new_ex:
            msg += f"[dim white]Current starting exercise:[/dim white] [bold bright_white]{new_ex['name']}[/bold bright_white]"
        panel = Panel(
            msg,
            title="[bold red]🔄 ALL PROGRESS RESET[/bold red]",
            subtitle=f"[dim red]{VERSION_STRING}[/dim red]",
            subtitle_align="right",
            border_style="red"
        )
        self.console.print(panel)

    def display_archive_exit(self, session_name, folder):
        msg = f"[bold cyan]Session archived safely:[/bold cyan] [bold yellow]🐾 {session_name}[/bold yellow]\n"
        msg += f"[dim white]Saved code & subjects to:[/dim white] [bold green]{folder}[/bold green]\n"
        msg += f"[dim white]Workspace `rendu/` cleaned for your next session.[/dim white]"
        panel = Panel(
            msg,
            title="[bold yellow]💾 SESSION SAVED & ARCHIVED[/bold yellow]",
            subtitle=f"[dim yellow]{VERSION_STRING}[/dim yellow]",
            subtitle_align="right",
            border_style="yellow"
        )
        self.console.print(panel)

    def display_sessions_history(self, sessions):
        if not sessions:
            self.console.print("[yellow]No archived sessions found in `history/` yet.[/yellow]")
            return
            
        table = Table(title="[bold cyan]ExamsHelp Saved Session History[/bold cyan]", border_style="cyan")
        table.add_column("Session Name", style="bold yellow")
        table.add_column("Archived Date", style="magenta")
        table.add_column("Level Reached", justify="center", style="cyan")
        table.add_column("Completed", justify="center", style="green")
        table.add_column("C Code Files", style="bright_white")

        for s in sessions:
            c_files = ", ".join(s.get("archived_rendu_files", [])) or "None"
            table.add_row(
                f"🐾 {s['session_name']}",
                s.get("archived_at", "N/A"),
                f"Level {s.get('current_level', 0)}",
                f"{s.get('completed_count', 0)} exs",
                c_files
            )

        self.console.print(table)

    def display_exercise_list(self, db, state):
        table = Table(title="[bold cyan]ExamsHelp Level Curriculum[/bold cyan]", border_style="cyan")
        table.add_column("Lvl", style="magenta", justify="center")
        table.add_column("Track", justify="center")
        table.add_column("Exercise Name", style="bright_white")
        table.add_column("Expected File", style="yellow")
        table.add_column("Status", justify="center")

        completed_set = set(state.get("completed_exercises", []))
        curr_lvl = state.get("current_level", 0)

        for lvl_str in sorted(db["levels"].keys(), key=lambda x: int(x)):
            lvl_int = int(lvl_str)
            for ex in db["levels"][lvl_str]:
                name = ex["name"]
                source_type = ex.get("source_type", "42_official")
                track_str = "[bold yellow]42 Official[/bold yellow]" if source_type == "42_official" else "[bold cyan]Extended[/bold cyan]"

                if name in completed_set:
                    status = "[bold green]COMPLETED ✓[/bold green]"
                elif lvl_int == curr_lvl and name == state.get("active_exercise_id", ""):
                    status = "[bold yellow]CURRENT ▶[/bold yellow]"
                elif lvl_int <= curr_lvl:
                    status = "[dim green]UNLOCKED[/dim green]"
                else:
                    status = "[dim white]LOCKED 🔒[/dim white]"
                    
                table.add_row(str(lvl_int), track_str, name, ex["expected_files"], status)

        self.console.print(table)
