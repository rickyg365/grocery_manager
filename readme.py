import os 

from rich.console import Console
from rich.markdown import Markdown
# reader


def read_readme(filepath="README.md"):
	with open(filepath, "r") as in_file:
		markdown = Markdown(in_file.read())
	
	return markdown



if __name__ == "__main__":
	my_console = Console()

	my_console.print(read_readme())
