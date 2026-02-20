from rich.console import Console, Group
from rich.panel import Panel
from rich.align import Align
from rich import box
from virl2_client.virl2_client import Lab
import questionary
from questionary import Choice
import configuration
from configuration import Aspect, AspectType
from rich.markdown import Markdown
import json
from typing import LiteralString, Literal
from rich_pyfiglet import RichFiglet


def aspect_type(input: AspectType) -> str:
    if input == AspectType.judgement:
        return "Judgement"
    elif input == AspectType.measurement:
        return "Measurement"
    elif input == AspectType.measurement_count:
        return "Calculated measurement"
    return ""


class Menu:
    def __init__(self):
        self.console = Console()
        self.console.clear()

    def main_title(self):
        self.console.clear()
        self.console.line(1)
        figlet = RichFiglet(
            "CML Marking",
            colors=["#45bae9", "#45bae9", "#ffffff", "#ffffff", "#ffffff", "#ffffff"],
            horizontal=True,
            font="ansi_shadow",
        )
        # title = "[bold turquoise2]CML[/bold turquoise2] [bold bright_white]Marking[/bold bright_white]"
        self.console.print(
            Align(Panel.fit(figlet, box=box.DOUBLE, padding=(1, 4)), "center")
        )

    def choose_labs(self, labs: list[Lab]):
        self.console.line(2)
        choices = [Choice(x.title, x.id) for x in labs]
        result = questionary.select("Choose the lab you want to mark!", choices).ask()
        return result

    def announce_sc(self, sc_name: str):
        text = f"Sub criterion [bold aquamarine3]{sc_name}[/bold aquamarine3]"
        self.console.print(Align(Panel.fit(text, box=box.DOUBLE), "center"))
        self.console.line(1)

    def announce_aspect(self, aspect: configuration.Aspect):
        text1 = f"Aspect [yellow]{aspect.aspect_id}[/yellow] - [orange1]{aspect_type(aspect.aspect_type)}[/orange1]"
        text2 = f"[yellow]{aspect.description}[/yellow]"
        if aspect.extra_description:
            text2 += f"\n{aspect.extra_description}"
        self.console.print(Panel.fit(text2, title=text1, title_align="left"))

    def announce_check_command(
        self,
        check_command: configuration.CheckCommand,
        index: int,
        subindex: int,
        run_result: tuple[str, str, str, dict],
        marks: list[int],
    ):
        result_text = ["[red3]FAIL[/red3]", "[green4]PASS[/green4]"]

        title = f"Check [dodger_blue1]#{index + 1}.{subindex + 1}[/dodger_blue1]"
        text = f"""Device: [cyan3]{run_result[0]}[/cyan3]
Check type: [cyan3]{run_result[1]}[/cyan3]
Check {run_result[1]}: [grey70]'[/grey70][cyan3]{run_result[2]}[/cyan3][grey70]'[/grey70]
{'Expected results:' if len(check_command.expected_results) > 0 else ''}
"""
        for i, er in enumerate(check_command.expected_results):
            text += f" - {result_text[marks[i]]} {er.description}\n"

        panel = Group(
            text,
            Panel.fit(
                (
                    run_result[3]["output"]
                    if check_command.command
                    else json.dumps(run_result[3], indent=4)
                ),
                title="Output",
                padding=(0, 4, 0, 1),
            ),
        )
        self.console.print(Panel.fit(panel, title=title))

    def announce_check_command_error(
        self,
        check_command: configuration.CheckCommand,
        index: int,
        subindex: int,
        scheduled_runs: list[tuple[str, str, str, list[list[str] | str], bool, bool]],
        e: Exception,
    ):
        _, mode, mode_command, _, _, _ = scheduled_runs[0]
        devices = ", ".join([x[0] for x in scheduled_runs])
        title = f"Check [dodger_blue1]#{index + 1}.{subindex + 1}[/dodger_blue1] - [red3]ERROR[/red3]"
        text = f"""Device(s): [cyan3]{devices}[/cyan3]
Check type: [cyan3]{mode}[/cyan3]
Check {mode}: [grey70]'[/grey70][cyan3]{mode_command}[/cyan3][grey70]'[/grey70]
{'Expected results:' if len(check_command.expected_results) > 0 else ''}
"""
        for i, er in enumerate(check_command.expected_results):
            text += f" - {er.description}\n"

        text += f"""
[red3]An error occured during execution. Please retry the aspect or mark manually.[/red3]
This may also indicate that there was no output to parse.
"""

        panel = Group(
            text,
            Panel.fit(
                str(e),
                title="Error message",
                padding=(0, 4, 0, 1),
            ),
        )

        self.console.print(Panel.fit(panel, title=title))

    def announce_mark_error(
        self,
        check_command: configuration.CheckCommand,
        index: int,
        subindex: int,
        scheduled_runs: tuple[str, str, str, list[list[str] | str], bool, bool],
        e: Exception,
    ):
        device, mode, mode_command, _, _, _ = scheduled_runs

        title = f"Check [dodger_blue1]#{index + 1}.{subindex + 1}[/dodger_blue1] - [red3]ERROR[/red3]"
        text = f"""Device(s): [cyan3]{device}[/cyan3]
Check type: [cyan3]{mode}[/cyan3]
Check {mode}: [grey70]'[/grey70][cyan3]{mode_command}[/cyan3][grey70]'[/grey70]
{'Expected results:' if len(check_command.expected_results) > 0 else ''}
"""
        for i, er in enumerate(check_command.expected_results):
            text += f" - {er.description}\n"

        text += f"""
[red3]The command executed but marking failed. Please retry the aspect or mark manually.[/red3]
"""

        panel = Group(
            text,
            Panel.fit(
                str(e),
                title="Error message",
                padding=(0, 4, 0, 1),
            ),
        )

        self.console.print(Panel.fit(panel, title=title))

    def aspect_finish(self) -> Literal["continue", "retry"]:
        choices = [
            Choice("Continue", "continue", shortcut_key="c"),
            Choice("Rerun aspect", "retry", shortcut_key="r"),
        ]

        result = questionary.select(
            "Aspect finished", choices=choices, use_shortcuts=True
        ).ask()

        return result
