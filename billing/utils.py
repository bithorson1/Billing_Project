from decimal import Decimal


def calculate_denomination_breakdown(balance: Decimal, shop_notes: dict) -> dict:
    denominations = [500, 50, 20, 10, 5, 2, 1]
    remaining = int(balance)
    result = {}

    for d in denominations:
        if remaining <= 0:
            break

        available = shop_notes.get(d, 0)
        if available <= 0:
            continue

        needed = remaining // d
        use = min(needed, available)

        if use > 0:
            result[d] = use
            remaining -= d * use

    return result
