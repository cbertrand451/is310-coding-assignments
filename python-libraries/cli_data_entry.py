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

while True:
    while True:
        restaurant = console.input("Enter [#FF5F05]Restaurant[#FF5F05] Name: ")
        item = console.input("Enter [#FF5F05]Food Item[#FF5F05]: ")
        rating = console.input("Enter [#FF5F05]Rating[#FF5F05] (single digit 1-10): ") + "/10"

        # print the entered data for user to confrm
        console.print("\nYou entered:\n")
        console.print(f"Restaurant: {restaurant}")
        console.print(f"Item: {item}")
        console.print(f"Rating: {rating}")

        confirmation = console.input("\nIs this correct? (y/n): ")
        if confirmation.lower() == 'y':
            input_data.append((restaurant, item, rating))
            break
        else:
            console.print("\nPlease re-enter the data\n")
