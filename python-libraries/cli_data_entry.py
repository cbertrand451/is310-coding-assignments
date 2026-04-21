from rich.console import Console
from rich.table import Table
import csv
import os


console = Console()

# function to build both the example table and the user inpput table
def build_food_table(title=None):
    table = Table(title=title)
    table.add_column("Restaurant", style="#FF5F05")
    table.add_column("Item", style="#FF5F05")
    table.add_column("Rating", style="#FF5F05", justify="right")
    return table


# display example data
def show_example_data():
    console.print("\nFAVORITE FOOD @ UIUC\n", style="bold #13294B")
    console.print("Here is some example data:\n", style="#13294B")

    table = build_food_table("Favorite Food")
    table.add_row("Jip Bap", "Combo Bowl", "9/10")
    table.add_row("Mia Za's", "Gluten Free Pizza", "6/10")
    table.add_row("Chipotle", "Chicken Bowl", "6/10")

    console.print(table)


# function to ask for user input
def get_food_entry():
    restaurant = console.input("Enter [#FF5F05]Restaurant[/#FF5F05] Name: ")
    item = console.input("Enter [#FF5F05]Food Item[/#FF5F05]: ")
    rating = console.input("Enter [#FF5F05]Rating[/#FF5F05] (single digit 1-10): ") + "/10"
    return restaurant, item, rating


# confirm the user's entry with a y or n 
def confirm_food_entry(restaurant, item, rating):
    console.print("\nYou entered:\n")

    user_table = build_food_table()
    user_table.add_row(restaurant, item, rating)
    console.print(user_table)

    confirmation = console.input("\nIs this correct? [#13294B](y/n)[/#13294B]: ")
    return confirmation.lower() == "y"


# put the confirmd user input into a list to save to csv, make sure that they are done as well
def collect_food_entries():
    console.print("\n[bold #13294B]Enter food data here[/bold #13294B]\n")
    input_data = []

    while True:
        while True:
            restaurant, item, rating = get_food_entry()

            if confirm_food_entry(restaurant, item, rating):
                input_data.append((restaurant, item, rating))
                break

            console.print("\nPlease re-enter the data\n")

        more_data = console.input("\nDo you want to add more data? [#13294B](y/n)[/#13294B]: ")
        if more_data.lower() != "y":
            return input_data

# path file for final csv
path = os.path.abspath("")
CSV_FILE = os.path.join(path, "uiuc_foods.csv")

# save user input into csv file
def save_food_entries(input_data, csv_file=CSV_FILE):
    with open(csv_file, "w", newline="") as f:
        build_data = csv.writer(f)
        build_data.writerow(["Restaurant", "Item", "Rating"])
        build_data.writerows(input_data)

    console.print(f"\nFile saved successfully to [#13294B]{csv_file}[/#13294B]\n")


def main():
    show_example_data()
    input_data = collect_food_entries()
    save_food_entries(input_data)


main()
