from rich.console import Console
from rich.table import Table
import csv
import os

console = Console()

# show example data first 
console.print("\nFAVORITE FOOD @ UIUC\n", style="bold #13294B")
console.print("Here is some example data:\n", style="#13294B")

table = Table(title="Favorite Food")
table.add_column("Restaurant", style="#FF5F05")
table.add_column("Item", style="#FF5F05")
table.add_column("Rating", style="#FF5F05", justify="right")

table.add_row("Jip Bap", "Combo Bowl", "9/10")
table.add_row("Mia Za's", "Gluten Free Pizza", "6/10")
table.add_row("Chipotle", "Chicken Bowl", "6/10")

console.print(table)

# start prompting for new user input data
console.print("\n[bold #13294B]Now enter your own movie data![/bold #13294B]\n")

input_data = []



