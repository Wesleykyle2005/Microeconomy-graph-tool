"""
Mathematical functions for microeconomic analysis.

This module provides functions for linear regression, equilibrium calculation,
and surplus computation for supply and demand curves.
"""

import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np


def calculate_sums(independent_variable, dependent_variable, data_points_count):
    """
    Calculate sums needed for linear regression.

    Args:
        independent_variable: List of independent variable values
        dependent_variable: List of dependent variable values
        data_points_count: Number of data points

    Returns:
        tuple: (sum_independent, sum_dependent, sum_independent_squared,
                sum_independent_dependent_product, sum_dependent_squared)

    Raises:
        ValueError: If arrays have different lengths or insufficient data points
    """
    if (
        len(independent_variable) != len(dependent_variable)
        or len(independent_variable) != data_points_count
    ):
        raise ValueError("All arrays must have the same length")

    if data_points_count < 2:
        raise ValueError("At least 2 data points are required for regression")

    sum_independent = sum(independent_variable)
    sum_dependent = sum(dependent_variable)
    sum_independent_squared = sum(x**2 for x in independent_variable)
    sum_dependent_squared = sum(y**2 for y in dependent_variable)
    sum_independent_dependent_product = sum(
        independent_variable[i] * dependent_variable[i]
        for i in range(data_points_count)
    )
    return (
        sum_independent,
        sum_dependent,
        sum_independent_squared,
        sum_independent_dependent_product,
        sum_dependent_squared,
    )


def calculate_slope(
    sum_independent,
    sum_dependent,
    sum_independent_squared,
    sum_independent_dependent_product,
    data_points_count,
):
    """
    Calculate slope (b1) for linear regression.

    Args:
        sum_independent: Sum of independent variable values
        sum_dependent: Sum of dependent variable values
        sum_independent_squared: Sum of squared independent variable values
        sum_independent_dependent_product: Sum of product of variables
        data_points_count: Number of data points

    Returns:
        float: Calculated slope

    Raises:
        ValueError: If denominator is too close to zero
    """
    denominator = sum_independent_squared - (sum_independent**2) / data_points_count
    if abs(denominator) < 1e-10:
        raise ValueError("Cannot calculate slope: denominator is too close to zero")

    slope = (
        sum_independent_dependent_product
        - ((sum_independent * sum_dependent) / data_points_count)
    ) / denominator
    return slope


def calculate_intercept(sum_independent, sum_dependent, slope, data_points_count):
    """
    Calculate intercept (b0) for linear regression.

    Args:
        sum_independent: Sum of independent variable values
        sum_dependent: Sum of dependent variable values
        slope: Calculated slope
        data_points_count: Number of data points

    Returns:
        float: Calculated intercept
    """
    intercept = (1 / data_points_count) * (sum_dependent - (slope * sum_independent))
    return intercept


def perform_calculations(quantity_values, price_values, data_points_count):
    """
    Perform complete linear regression calculation.

    Args:
        quantity_values: List of quantity values
        price_values: List of price values
        data_points_count: Number of data points

    Returns:
        tuple: (intercept, slope)

    Raises:
        ValueError: If input arrays are empty
    """
    if not quantity_values or not price_values:
        raise ValueError("Input arrays cannot be empty")

    (
        sum_independent,
        sum_dependent,
        sum_independent_squared,
        sum_independent_dependent_product,
        _,
    ) = calculate_sums(quantity_values, price_values, data_points_count)
    slope = calculate_slope(
        sum_independent,
        sum_dependent,
        sum_independent_squared,
        sum_independent_dependent_product,
        data_points_count,
    )
    intercept = calculate_intercept(
        sum_independent, sum_dependent, slope, data_points_count
    )
    return intercept, slope


def calculate_equilibrium(
    demand_intercept, demand_slope, supply_intercept, supply_slope
):
    """
    Calculate equilibrium price and quantity.

    Args:
        demand_intercept: Demand curve intercept
        demand_slope: Demand curve slope
        supply_intercept: Supply curve intercept
        supply_slope: Supply curve slope

    Returns:
        tuple: (equilibrium_price, equilibrium_quantity)

    Raises:
        ValueError: If curves are parallel or equilibrium has negative values
    """
    if abs(demand_slope - supply_slope) < 1e-10:
        raise ValueError(
            "Demand and supply curves are parallel - no equilibrium exists"
        )

    equilibrium_price = (supply_intercept - demand_intercept) / (
        demand_slope - supply_slope
    )
    equilibrium_quantity = demand_intercept + demand_slope * equilibrium_price

    if equilibrium_price < 0 or equilibrium_quantity < 0:
        raise ValueError("Equilibrium point has negative values")

    return equilibrium_price, equilibrium_quantity


def calculate_surpluses(
    equilibrium_quantity,
    equilibrium_price,
    demand_price_intercept,
    supply_quantity_intercept,
    supply_price_intercept,
):
    """
    Calculate consumer and producer surpluses.

    Args:
        equilibrium_quantity: Quantity at equilibrium
        equilibrium_price: Price at equilibrium
        demand_price_intercept: Price intercept of demand curve
        supply_quantity_intercept: Quantity intercept of supply curve
        supply_price_intercept: Price intercept of supply curve

    Returns:
        tuple: (consumer_surplus, producer_surplus)

    Raises:
        ValueError: If equilibrium values are not positive
    """
    if equilibrium_quantity <= 0 or equilibrium_price <= 0:
        raise ValueError("Equilibrium values must be positive")

    consumer_surplus = (
        equilibrium_quantity * (demand_price_intercept - equilibrium_price)
    ) / 2
    producer_surplus = 0

    if supply_quantity_intercept > 0:
        producer_surplus = (
            (equilibrium_quantity + supply_quantity_intercept) * equilibrium_price
        ) / 2
    else:
        producer_surplus = (
            equilibrium_quantity * (equilibrium_price - supply_price_intercept)
        ) / 2

    return consumer_surplus, producer_surplus


def plot_curves(demand_intercept, demand_slope, supply_intercept, supply_slope):
    """
    Plot supply and demand curves with equilibrium point and surpluses.

    Args:
        demand_intercept: Demand curve intercept
        demand_slope: Demand curve slope
        supply_intercept: Supply curve intercept
        supply_slope: Supply curve slope

    Raises:
        Exception: If plotting fails
    """
    try:
        # Calculate equilibrium and intercepts
        equilibrium_data = _calculate_plot_data(
            demand_intercept, demand_slope, supply_intercept, supply_slope
        )

        # Create and display the plot
        _create_plot(equilibrium_data)

    except Exception as error:
        print(f"Error plotting curves: {error}")
        raise


def _calculate_plot_data(
    demand_intercept, demand_slope, supply_intercept, supply_slope
):
    """Calculate all data needed for plotting."""
    equilibrium_price, equilibrium_quantity = calculate_equilibrium(
        demand_intercept, demand_slope, supply_intercept, supply_slope
    )

    # Calculate intercepts
    demand_price_intercept = (
        -demand_intercept / demand_slope if demand_slope != 0 else float("inf")
    )
    demand_quantity_intercept = demand_intercept

    supply_price_intercept = (
        -supply_intercept / supply_slope if supply_slope != 0 else float("inf")
    )
    supply_quantity_intercept = supply_intercept

    # Calculate surpluses
    consumer_surplus, producer_surplus = calculate_surpluses(
        equilibrium_quantity,
        equilibrium_price,
        demand_price_intercept,
        supply_quantity_intercept,
        supply_price_intercept,
    )

    return {
        "equilibrium_price": equilibrium_price,
        "equilibrium_quantity": equilibrium_quantity,
        "demand_price_intercept": demand_price_intercept,
        "demand_quantity_intercept": demand_quantity_intercept,
        "supply_price_intercept": supply_price_intercept,
        "supply_quantity_intercept": supply_quantity_intercept,
        "consumer_surplus": consumer_surplus,
        "producer_surplus": producer_surplus,
        "demand_intercept": demand_intercept,
        "demand_slope": demand_slope,
        "supply_intercept": supply_intercept,
        "supply_slope": supply_slope,
    }


def _plot_curves(demand_quantities, supply_quantities, price_range):
    """Common function to plot supply and demand curves."""
    plt.figure(figsize=(10, 10))
    plt.plot(
        demand_quantities,
        price_range,
        label="Demand Curve",
        color="blue",
        linewidth=2,
    )
    plt.plot(
        supply_quantities,
        price_range,
        label="Supply Curve",
        color="red",
        linewidth=2,
    )


def _plot_curves_on_axis(ax, demand_quantities, supply_quantities, price_range):
    """Plot supply and demand curves on existing axis."""
    ax.plot(
        demand_quantities,
        price_range,
        label="Demand Curve",
        color="blue",
        linewidth=2,
    )
    ax.plot(
        supply_quantities,
        price_range,
        label="Supply Curve",
        color="red",
        linewidth=2,
    )


def _create_plot(data):
    """Create and display the plot."""
    # Print results
    print(
        f"Equilibrium Price: {data['equilibrium_price']:.2f}, "
        f"Equilibrium Quantity: {data['equilibrium_quantity']:.2f}"
    )
    print(
        f"Consumer Surplus: {data['consumer_surplus']:.2f}, "
        f"Producer Surplus: {data['producer_surplus']:.2f}"
    )

    # Create price range
    max_price_intercept = max(
        (
            data["demand_price_intercept"]
            if data["demand_price_intercept"] != float("inf")
            else 0
        ),
        (
            data["supply_price_intercept"]
            if data["supply_price_intercept"] != float("inf")
            else 0
        ),
    )
    price_range = np.linspace(0, max_price_intercept * 1.1, 100)

    # Calculate quantities
    demand_quantities = data["demand_intercept"] + data["demand_slope"] * price_range
    supply_quantities = data["supply_intercept"] + data["supply_slope"] * price_range

    # Create plot using common function
    _plot_curves(demand_quantities, supply_quantities, price_range)

    # Add intercept points
    plt.scatter(
        [data["demand_quantity_intercept"]],
        [0],
        color="blue",
        marker="o",
        label=f"Demand Intercept (0, {data['demand_quantity_intercept']:.2f})",
    )
    if data["demand_price_intercept"] != float("inf"):
        plt.scatter(
            [0],
            [data["demand_price_intercept"]],
            color="blue",
            marker="x",
            label=f"Price Intercept Demand ({data['demand_price_intercept']:.2f}, 0)",
        )

    plt.scatter(
        [data["supply_quantity_intercept"]],
        [0],
        color="red",
        marker="o",
        label=f"Supply Intercept (0, {data['supply_quantity_intercept']:.2f})",
    )
    if data["supply_price_intercept"] != float("inf"):
        plt.scatter(
            [0],
            [data["supply_price_intercept"]],
            color="red",
            marker="x",
            label=f"Price Intercept Supply ({data['supply_price_intercept']:.2f}, 0)",
        )

    # Add equilibrium point
    plt.axhline(
        data["equilibrium_price"],
        color="green",
        linestyle="--",
        label=f"Equilibrium Price (P={data['equilibrium_price']:.2f})",
    )
    plt.axvline(
        data["equilibrium_quantity"],
        color="green",
        linestyle="--",
        label=f"Equilibrium Quantity (Q={data['equilibrium_quantity']:.2f})",
    )
    plt.scatter(
        [data["equilibrium_quantity"]],
        [data["equilibrium_price"]],
        color="green",
        marker="o",
        s=100,
        label=f"Equilibrium Point ({data['equilibrium_price']:.2f}, "
        f"{data['equilibrium_quantity']:.2f})",
    )

    # Configure plot
    plt.title("Supply and Demand Curves with Intercepts and Equilibrium Point")
    plt.xlabel("Quantity (Q)")
    plt.ylabel("Price (P)")
    plt.axhline(0, color="red", lw=0.5, ls="--")
    plt.axvline(0, color="red", lw=0.5, ls="--")
    plt.legend()
    plt.grid(True)

    # Set axis limits
    max_quantity = max(
        data["demand_quantity_intercept"],
        data["supply_quantity_intercept"],
        data["equilibrium_quantity"],
    )
    max_price = max(
        (
            data["demand_price_intercept"]
            if data["demand_price_intercept"] != float("inf")
            else 0
        ),
        (
            data["supply_price_intercept"]
            if data["supply_price_intercept"] != float("inf")
            else 0
        ),
        data["equilibrium_price"],
    )

    plt.xlim(0, max_quantity * 1.1)
    plt.ylim(0, max_price * 1.1)

    # Set tick intervals
    tick_interval_x = (plt.xlim()[1] - plt.xlim()[0]) / 15
    tick_interval_y = (plt.ylim()[1] - plt.ylim()[0]) / 15

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(tick_interval_x))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(tick_interval_y))

    plt.show()
