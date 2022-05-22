from pathlib import Path

import typer

from shoppingcart.shopping_cart import ShoppingCart

app = typer.Typer()


@app.command()
def create(file: Path = typer.Argument(..., help="the file to create")):
    """
    Create an empty shopping cart file.
    """
    with file.open(mode="wb"):
        shopping_cart = ShoppingCart([])
        shopping_cart.save_to_path(file)


@app.command()
def import_csv(
    csv_file: Path = typer.Argument(..., help="the CSV file to import"),
    file: Path = typer.Argument(..., help="the shopping cart file to save"),
):
    """
    Import a CSV file and save it to a shopping-cart file.
    """
    shopping_cart = ShoppingCart.from_csv_path(csv_file)
    shopping_cart.save_to_path(file)


@app.command()
def add(
    file: Path = typer.Argument(..., help="a file containing the shopping cart"),
    item_id: str = typer.Argument(..., help="the item ID"),
    name: str = typer.Argument(..., help="the item name"),
    price: float = typer.Argument(..., help="the price per item"),
    num: int = typer.Option(1, help="the number of items to add"),
):
    """
    Add an item to the shopping cart.
    """
    shopping_cart = ShoppingCart.load_from_path(file)
    shopping_cart.add(
        {
            "article_number": item_id,
            "article_name": name,
            "price_per_item": price,
            "number_of_items": num,
        }
    )
    shopping_cart.save_to_path(file)


@app.command()
def delete(
    file: Path = typer.Argument(..., help="a file containing the shopping cart"),
    item_id: str = typer.Argument(..., help="the item ID"),
    name: str = typer.Argument(..., help="the item name"),
    price: float = typer.Argument(..., help="the price per item"),
    num: int = typer.Option(1, help="the number of items to add"),
):
    """
    Delete an item from the shopping cart.
    """
    shopping_cart = ShoppingCart.load_from_path(file)
    shopping_cart.delete(
        {
            "article_number": item_id,
            "article_name": name,
            "price_per_item": price,
            "number_of_items": num,
        }
    )
    shopping_cart.save_to_path(file)


@app.command()
def list(file: Path = typer.Argument(..., help="a file containing the shopping cart")):
    """
    Print the contents of the shopping cart.
    """
    shopping_cart = ShoppingCart.load_from_path(file)
    print(shopping_cart)


if __name__ == "__main__":
    app()
