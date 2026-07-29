import os
import sys

VERSION_STRING = "v0.1.0-alpha"

# Standard ANSI Color Tokens
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_DIM = "\033[2m"

C_CYAN = "\033[1;36m"
C_MAGENTA = "\033[1;35m"
C_YELLOW = "\033[1;33m"
C_GREEN = "\033[1;32m"
C_RED = "\033[1;31m"
C_WHITE = "\033[1;37m"
C_BLUE = "\033[1;34m"

from engine.hints import HintEngine

class TerminalUI:
    def __init__(self):
        pass

    def _draw_panel(self, title, content_lines, border_color=C_CYAN, subtitle=None):
        width = 76
        inner_w = width - 4
        
        # Header border
        title_str = f" {title} "
        left_pad = (inner_w - len(title)) // 2
        right_pad = inner_w - len(title) - left_pad
        header = f"{border_color}╭" + "─" * (left_pad + 1) + title_str + "─" * (right_pad + 1) + f"╮{C_RESET}"
        print(header)

        # Content lines
        for line in content_lines:
            # Simple stripping of ANSI codes to measure printable length accurately
            clean_line = line
            for code in [C_RESET, C_BOLD, C_DIM, C_CYAN, C_MAGENTA, C_YELLOW, C_GREEN, C_RED, C_WHITE, C_BLUE]:
                clean_line = clean_line.replace(code, "")
            
            pad = inner_w - len(clean_line)
            if pad < 0:
                pad = 0
            print(f"{border_color}│{C_RESET} {line}" + " " * pad + f" {border_color}│{C_RESET}")

        # Footer border
        if subtitle:
            sub_str = f" {subtitle} "
            left_pad = width - 3 - len(subtitle)
            footer = f"{border_color}╰" + "─" * (left_pad - 1) + sub_str + f"╯{C_RESET}"
        else:
            footer = f"{border_color}╰" + "─" * (width - 2) + f"╯{C_RESET}"
        print(footer)

    def print_banner(self, session_name=None):
        banner = f"""
{C_CYAN} ███████╗██╗  ██╗██████╗ ███╗   ███╗███████╗██╗  ██╗███████╗██╗     ██████╗ {C_RESET}
{C_CYAN} ██╔════╝╚██╗██╔╝██╔══██╗████╗ ████║██╔════╝██║  ██║██╔════╝██║     ██╔══██╗{C_RESET}
{C_CYAN} █████╗   ╚███╔╝ ██████╔╝██╔████╔██║███████╗███████║█████╗  ██║     ██████╔╝{C_RESET}
{C_CYAN} ██╔══╝   ██╔██╗ ██╔═══╝ ██║╚██╔╝██║╚════██║██╔══██║██╔══╝  ██║     ██╔═══╝ {C_RESET}
{C_CYAN} ███████╗██╔╝ ██╗██║     ██║ ╚═╝ ██║███████╗██║  ██║███████╗███████╗██║     {C_RESET}
{C_MAGENTA} ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     {C_RESET}
                 {C_YELLOW}⚡ Antigravity Edition — Educational Examshell ⚡{C_RESET}
"""
        print(banner)
        if session_name:
            print(f" {C_MAGENTA}🐾 Active Session:{C_RESET} {C_YELLOW}{session_name}{C_RESET}\n")

    def display_status(self, progress_data):
        session_name = progress_data.get("session_name", "active-session")
        curr_lvl = progress_data["current_level"]
        session_completed = progress_data.get("session_completed_count", 0)
        total_completions = progress_data.get("total_completions", 0)
        ex = progress_data["current_exercise"]

        level_blocks = ""
        for i in range(10):
            if i < curr_lvl:
                level_blocks += f"{C_GREEN}█{C_RESET}"
            elif i == curr_lvl:
                level_blocks += f"{C_YELLOW}▶{C_RESET}"
            else:
                level_blocks += f"{C_DIM}░{C_RESET}"

        lines = [
            f"{C_MAGENTA}Active Session:{C_RESET}      {C_YELLOW}🐾 {session_name}{C_RESET}",
            f"{C_MAGENTA}Current Level:{C_RESET}       {C_YELLOW}Level {curr_lvl}/9{C_RESET}  [{level_blocks}]",
            f"{C_MAGENTA}Session Progress:{C_RESET}    {C_GREEN}{session_completed}{C_RESET} exercises completed in this session",
            f"{C_MAGENTA}Cumulative Total:{C_RESET}    {C_CYAN}{total_completions}{C_RESET} total questions completed across sessions"
        ]

        if ex:
            source_type = ex.get("source_type", "42_official")
            track_label = f"{C_YELLOW}🏆 Official 42 Exam{C_RESET}" if source_type == "42_official" else f"{C_CYAN}⚡ ExamsHelp Extended (Custom){C_RESET}"
            lines.append(f"{C_MAGENTA}Exercise Track:{C_RESET}     {track_label}")
            lines.append(f"{C_MAGENTA}Assignment Name:{C_RESET}    {C_WHITE}{ex['name']}{C_RESET}")
            lines.append(f"{C_MAGENTA}Expected File:{C_RESET}      {C_YELLOW}rendu/{ex['expected_files']}{C_RESET}")
            lines.append(f"{C_MAGENTA}Allowed Functions:{C_RESET}  {C_CYAN}{ex['allowed_functions']}{C_RESET}")
            if ex.get("prototype"):
                lines.append(f"{C_MAGENTA}Function Prototype:{C_RESET} {C_YELLOW}{ex['prototype']}{C_RESET}")

        self._draw_panel(f"{C_CYAN}⚡ EXAMSHELP DASHBOARD ⚡{C_RESET}", lines, border_color=C_CYAN, subtitle=f"{C_DIM}{VERSION_STRING}{C_RESET}")

    def display_subject(self, exercise_info):
        if not exercise_info:
            print("No active exercise selected.")
            return

        source_type = exercise_info.get("source_type", "42_official")
        track_title = "🏆 42 Official Exam" if source_type == "42_official" else "⚡ ExamsHelp Extended Custom"
        subj_text = exercise_info.get("subject", "No subject text available.")

        subj_lines = subj_text.strip().split("\n")
        lines = [f"{C_WHITE}{line}{C_RESET}" for line in subj_lines]

        self._draw_panel(
            f"{C_CYAN}SUBJECT: {exercise_info['name']} ({track_title}){C_RESET}",
            lines,
            border_color=C_MAGENTA,
            subtitle=f"{C_DIM}{VERSION_STRING}{C_RESET}"
        )

    def display_eval_result(self, result):
        if result["success"]:
            lines = [
                f"{C_GREEN}✨ {result['message']}{C_RESET}",
                f"{C_GREEN}Level requirements met! New subject unlocked in `subjects/`!{C_RESET}"
            ]
            self._draw_panel(f"{C_GREEN}PASSED - GRADEME SUCCESS{C_RESET}", lines, border_color=C_GREEN, subtitle=f"{C_DIM}{VERSION_STRING}{C_RESET}")
        else:
            stage = result.get("stage", "eval")
            lines = [f"{C_RED}❌ {result['message']}{C_RESET}"]
            
            if "log" in result:
                lines.append("")
                lines.append(f"{C_YELLOW}Compiler Output:{C_RESET}")
                for log_l in result["log"].split("\n"):
                    lines.append(f"  {C_YELLOW}{log_l}{C_RESET}")

            if "got" in result:
                lines.append("")
                lines.append(f"{C_GREEN}Expected Output: {repr(result['expected'])}{C_RESET}")
                lines.append(f"{C_RED}Your Output:     {repr(result['got'])}{C_RESET}")

            self._draw_panel(f"{C_RED}GRADEME FEEDBACK ({stage.upper()}){C_RESET}", lines, border_color=C_RED, subtitle=f"{C_DIM}{VERSION_STRING}{C_RESET}")

            hints = result.get("hints", [])
            if hints:
                hint_lines = [f"• {C_CYAN}{h}{C_RESET}" for h in hints]
                self._draw_panel(f"{C_YELLOW}💡 FRIENDLY HINT (0 PENALTY){C_RESET}", hint_lines, border_color=C_YELLOW)

    def display_hints(self, exercise_info):
        if not exercise_info:
            print("No active exercise selected.")
            return

        hints = HintEngine.get_exercise_hints(exercise_info)
        hint_lines = [f"• {C_CYAN}{h}{C_RESET}" for h in hints]
        self._draw_panel(
            f"{C_YELLOW}💡 WHAT TO LOOK OUT FOR: {exercise_info['name'].upper()}{C_RESET}",
            hint_lines,
            border_color=C_YELLOW,
            subtitle=f"{C_DIM}{VERSION_STRING}{C_RESET}"
        )

    def display_skip(self, old_name, new_ex):
        if new_ex:
            source_type = new_ex.get("source_type", "42_official")
            track_name = "Official 42 Exam" if source_type == "42_official" else "ExamsHelp Extended Custom"
            lines = [
                f"{C_YELLOW}Skipped exercise '{old_name}'.{C_RESET}",
                f"{C_GREEN}Now on exercise: {new_ex['name']} ({track_name} — Level {new_ex.get('orig_level', 0)}){C_RESET}",
                f"{C_DIM}Updated `subjects/subject.txt` with new assignment specifications.{C_RESET}"
            ]
        else:
            lines = [f"{C_YELLOW}Skipped exercise. All exercises in curriculum completed!{C_RESET}"]

        self._draw_panel(f"{C_YELLOW}⏩ EXERCISE SKIPPED{C_RESET}", lines, border_color=C_YELLOW, subtitle=f"{C_DIM}{VERSION_STRING}{C_RESET}")

    def display_reset(self, new_ex):
        lines = [f"{C_GREEN}All progress reset to Level 0!{C_RESET}"]
        if new_ex:
            lines.append(f"{C_DIM}Current starting exercise:{C_RESET} {C_WHITE}{new_ex['name']}{C_RESET}")

        self._draw_panel(f"{C_RED}🔄 ALL PROGRESS RESET{C_RESET}", lines, border_color=C_RED, subtitle=f"{C_DIM}{VERSION_STRING}{C_RESET}")

    def display_archive_exit(self, session_name, folder):
        lines = [
            f"{C_CYAN}Session archived safely:{C_RESET} {C_YELLOW}🐾 {session_name}{C_RESET}",
            f"{C_DIM}Saved code & subjects to:{C_RESET} {C_GREEN}{folder}{C_RESET}",
            f"{C_DIM}Workspace `rendu/` cleaned for your next session.{C_RESET}"
        ]
        self._draw_panel(f"{C_YELLOW}💾 SESSION SAVED & ARCHIVED{C_RESET}", lines, border_color=C_YELLOW, subtitle=f"{C_DIM}{VERSION_STRING}{C_RESET}")

    def display_sessions_history(self, sessions):
        if not sessions:
            print(f"{C_YELLOW}No archived sessions found in `history/` yet.{C_RESET}")
            return

        print(f"\n{C_CYAN}======================== ExamsHelp Saved Session History ========================{C_RESET}")
        print(f"{C_YELLOW}Session Name             Date & Time          Level     Completed  Files{C_RESET}")
        print("-" * 76)
        for s in sessions:
            c_files = ", ".join(s.get("archived_rendu_files", [])) or "None"
            print(f"🐾 {s['session_name']:<22} {s.get('archived_at', 'N/A'):<20} Level {s.get('current_level', 0):<3} {s.get('completed_count', 0):<2} exs     {c_files}")
        print("-" * 76 + "\n")

    def display_exercise_list(self, db, state):
        print(f"\n{C_CYAN}======================== ExamsHelp Level Curriculum ========================{C_RESET}")
        print(f"{C_MAGENTA}Lvl  Track         Exercise Name        Expected File         Status{C_RESET}")
        print("-" * 76)

        completed_set = set(state.get("completed_exercises", []))
        curr_lvl = state.get("current_level", 0)

        for lvl_str in sorted(db["levels"].keys(), key=lambda x: int(x)):
            lvl_int = int(lvl_str)
            for ex in db["levels"][lvl_str]:
                name = ex["name"]
                source_type = ex.get("source_type", "42_official")
                track_str = "42 Official" if source_type == "42_official" else "Extended"

                if name in completed_set:
                    status = f"{C_GREEN}COMPLETED ✓{C_RESET}"
                elif lvl_int == curr_lvl and name == state.get("active_exercise_id", ""):
                    status = f"{C_YELLOW}CURRENT ▶{C_RESET}"
                elif lvl_int <= curr_lvl:
                    status = f"{C_GREEN}UNLOCKED{C_RESET}"
                else:
                    status = f"{C_DIM}LOCKED 🔒{C_RESET}"
                    
                print(f"{lvl_int:<4} {track_str:<13} {name:<20} {ex['expected_files']:<21} {status}")
        print("-" * 76 + "\n")
