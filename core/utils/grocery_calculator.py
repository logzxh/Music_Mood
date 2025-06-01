def calculate_groceries(recipe):
    """
    Given a recipe object with an 'ingredients' field (list of dicts with 'name' and 'quantity'),
    returns a groceries dictionary mapping ingredient names to their quantities.
    """
    groceries = {}
    for item in recipe.ingredients:
        name = item.get('name')
        qty = item.get('quantity')
        if name is not None and qty is not None:
            groceries[name] = qty
    return groceries