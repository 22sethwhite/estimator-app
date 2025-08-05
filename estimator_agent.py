
"""
Estimator Agent
----------------

This module provides a simple command‑line estimator tool for small construction
or service jobs. It helps you calculate the total cost of a job by asking for
inputs such as materials, labor hours, hourly labor rates, overhead percentage
and desired profit margin. The goal of this script is to offer a minimal
example that can be extended or integrated into a larger system. It's ideal
for validating the core estimating logic before investing in a full‑fledged
application.

Usage
~~~~~
Run the script directly from the command line:

    python estimator_agent.py

You will be prompted to enter quantities for each material in the default
catalog, as well as labor hours, labor rate, overhead percentage, and profit
margin. The script will then print out a breakdown and total estimate.

Extending
~~~~~~~~~
To customize or expand this estimator, you can:

* Add more materials to the `MATERIAL_CATALOG` dictionary, along with their
  unit prices. Prices can be updated to reflect local market conditions.
* Modify `estimate_job` to read materials from a CSV or database instead of
  the hardcoded dictionary.
* Replace the `input()` calls with a graphical interface or web form if you
  choose to integrate this into an application.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Tuple


@dataclass
class MaterialEstimate:
    """Dataclass to hold the quantity and cost of a material."""

    quantity: float
    cost_per_unit: float

    def total_cost(self) -> float:
        return self.quantity * self.cost_per_unit


# Default catalog of materials with approximate unit prices.
# These prices are illustrative; update them according to your local market.
MATERIAL_CATALOG: Dict[str, float] = {
    "2x4": 3.50,        # price per linear foot in USD
    "drywall sheet": 13.00,  # price per 4x8 sheet in USD
    "nails (per lb)": 2.50,
    "paint (per gallon)": 25.00,
    "concrete (per bag)": 6.50,
}


def collect_materials() -> Dict[str, MaterialEstimate]:
    """
    Prompt the user for quantities of each material defined in the catalog.

    Returns a dictionary mapping material names to MaterialEstimate objects.
    """
    print("\n=== MATERIAL QUANTITIES ===")
    materials_needed: Dict[str, MaterialEstimate] = {}
    for name, price in MATERIAL_CATALOG.items():
        while True:
            try:
                qty_input = input(f"Enter quantity for {name} (or press Enter to skip): ").strip()
                if not qty_input:
                    quantity = 0.0
                else:
                    quantity = float(qty_input)
                materials_needed[name] = MaterialEstimate(quantity=quantity, cost_per_unit=price)
                break
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
    return materials_needed


def calculate_material_costs(materials: Dict[str, MaterialEstimate]) -> Tuple[float, Dict[str, float]]:
    """
    Calculate the total material cost and return breakdown per material.

    Parameters
    ----------
    materials: Dict[str, MaterialEstimate]
        A dictionary of materials mapped to their estimate objects.

    Returns
    -------
    Tuple[float, Dict[str, float]]
        Total material cost and a breakdown per material.
    """
    total = 0.0
    breakdown = {}
    for name, estimate in materials.items():
        cost = estimate.total_cost()
        breakdown[name] = cost
        total += cost
    return total, breakdown


def prompt_float(prompt: str, default: float = 0.0) -> float:
    """
    Prompt the user for a floating‑point number with an optional default.

    If the user enters nothing, the default value is returned.
    """
    while True:
        try:
            value_str = input(prompt).strip()
            if not value_str:
                return default
            return float(value_str)
        except ValueError:
            print("Please enter a numeric value.")


def estimate_job() -> None:
    """
    Drive the interactive job estimator via the command line.

    This function prompts for material quantities, labor hours and rate,
    overhead percentage, and desired profit margin. It then displays a
    detailed cost breakdown.
    """
    print("Welcome to the Estimator Agent!")
    # Collect materials
    materials = collect_materials()
    material_total, material_breakdown = calculate_material_costs(materials)
    # Collect labor inputs
    print("\n=== LABOR ===")
    labor_hours = prompt_float("Enter total labor hours needed: ")
    labor_rate = prompt_float("Enter labor rate per hour (in USD): ")
    labor_cost = labor_hours * labor_rate
    # Overhead and profit inputs
    print("\n=== OVERHEAD & PROFIT ===")
    overhead_percentage = prompt_float(
        "Enter overhead percentage (e.g., 10 for 10%): ", default=0.0
    )
    profit_percentage = prompt_float(
        "Enter profit margin percentage (e.g., 30 for 30% profit): ", default=0.0
    )
    # Compute overhead and profit amounts
    subtotal = material_total + labor_cost
    overhead_amount = subtotal * (overhead_percentage / 100.0)
    profit_amount = (subtotal + overhead_amount) * (profit_percentage / 100.0)
    total_estimate = subtotal + overhead_amount + profit_amount
    # Print results
    print("\n=== ESTIMATE SUMMARY ===")
    print(f"Material costs: ${material_total:.2f}")
    for name, cost in material_breakdown.items():
        if cost > 0:
            print(f"  - {name}: ${cost:.2f}")
    print(f"Labor cost (@ ${labor_rate:.2f}/hr for {labor_hours:.2f} hrs): ${labor_cost:.2f}")
    print(f"Overhead ({overhead_percentage:.2f}%): ${overhead_amount:.2f}")
    print(f"Profit ({profit_percentage:.2f}%): ${profit_amount:.2f}")
    print(f"\nTotal Estimate: ${total_estimate:.2f}")


if __name__ == "__main__":
  

