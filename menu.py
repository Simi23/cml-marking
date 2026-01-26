from rich.console import Console
from rich.text import Text
from virl2_client.virl2_client import Lab
import questionary
from questionary import Choice
import configuration
from configuration import Aspect, AspectType


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

    def choose_labs(self, labs: list[Lab]):
        self.console.clear()
        self.console.line(2)
        choices = [Choice(x.title, x.id) for x in labs]
        result = questionary.select("Choose the lab you want to mark!", choices).ask()
        return result

    def separator(self, length, char="="):
        self.console.print(char * length, style="bold bright_white")

    def length(self, text):
        return Text.from_markup(text).cell_len

    def announce_sc(self, sc_name: str):
        text = f"|  Sub criterion [bold aquamarine3]{sc_name}[/bold aquamarine3]  |"
        length = self.length(text)
        self.separator(length)
        self.console.print(text)
        self.separator(length)
        self.console.line(1)

    def announce_aspect(self, aspect: configuration.Aspect):
        text1 = f"  Aspect [yellow]{aspect.aspect_id}[/yellow] - [orange1]{aspect_type(aspect.aspect_type)}[/orange1]  "
        text2 = f"  [yellow]{aspect.description}[/yellow]  "
        length = max(self.length(text1), self.length(text2))
        self.separator(length, "-")
        self.console.print(text1)
        self.console.print(text2)
        self.separator(length, "-")
        return
