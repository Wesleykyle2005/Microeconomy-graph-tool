"""
Microeconomy Graph Tool - Main Application.

This module provides a graphical user interface for microeconomic analysis
using Tkinter. It allows users to input supply and demand data, calculate
equilibrium points and surpluses, and visualize the results.
"""

import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd

from funct import (
    perform_calculations,
    calculate_equilibrium,
    calculate_surpluses,
    _plot_curves_on_axis,
)


class DataManager:
    """Manages data loading, parsing, and validation."""

    def __init__(self):
        """Initialize DataManager."""
        self._initialized = True

    def get_example_data(self):
        """Get example data for testing."""
        return self.load_example_data_from_csv()

    @staticmethod
    def load_example_data_from_csv(filename="example_data.csv"):
        """
        Load example data from CSV file.

        Args:
            filename: Path to the CSV file

        Returns:
            dict: Dictionary containing demand and supply data or None if error
        """
        try:
            df = pd.read_csv(filename)
            demand_data = df[df["curve_type"] == "demand"]
            supply_data = df[df["curve_type"] == "supply"]

            return {
                "demand_prices": demand_data["price"].tolist(),
                "demand_quantities": demand_data["quantity"].tolist(),
                "supply_prices": supply_data["price"].tolist(),
                "supply_quantities": supply_data["quantity"].tolist(),
            }
        except (FileNotFoundError, pd.errors.EmptyDataError, KeyError) as error:
            print(f"Error loading CSV: {error}")
            return None

    @staticmethod
    def parse_data_string(data_string):
        """
        Parse comma-separated string into list of floats.

        Args:
            data_string: Comma-separated string of numbers

        Returns:
            list: List of float values
        """
        try:
            return [float(x.strip()) for x in data_string.split(",") if x.strip()]
        except ValueError:
            return []

    @staticmethod
    def validate_data(
        demand_prices, demand_quantities, supply_prices, supply_quantities
    ):
        """
        Validate input data.

        Args:
            demand_prices: List of demand prices
            demand_quantities: List of demand quantities
            supply_prices: List of supply prices
            supply_quantities: List of supply quantities

        Returns:
            tuple: (is_valid, error_message)
        """
        if len(demand_prices) != len(demand_quantities):
            return False, "Demand price and quantity arrays must have the same length"

        if len(supply_prices) != len(supply_quantities):
            return False, "Supply price and quantity arrays must have the same length"

        if len(demand_prices) < 2:
            return False, "At least 2 demand data points are required"

        if len(supply_prices) < 2:
            return False, "At least 2 supply data points are required"

        return True, "Data is valid"


class Calculator:
    """Handles all mathematical calculations."""

    def __init__(self):
        """Initialize Calculator."""
        self._initialized = True

    def get_calculation_methods(self):
        """Get available calculation methods."""
        return ["linear_regression", "equilibrium", "surpluses"]

    @staticmethod
    def calculate_curves(
        demand_prices, demand_quantities, supply_prices, supply_quantities
    ):
        """
        Calculate demand and supply curve parameters.

        Args:
            demand_prices: List of demand prices
            demand_quantities: List of demand quantities
            supply_prices: List of supply prices
            supply_quantities: List of supply quantities

        Returns:
            tuple: (demand_intercept, demand_slope, supply_intercept, supply_slope)

        Raises:
            ValueError: If calculation fails
        """
        try:
            # Calculate demand curve
            demand_intercept, demand_slope = perform_calculations(
                demand_quantities, demand_prices, len(demand_prices)
            )

            # Calculate supply curve
            supply_intercept, supply_slope = perform_calculations(
                supply_quantities, supply_prices, len(supply_prices)
            )

            return demand_intercept, demand_slope, supply_intercept, supply_slope

        except Exception as error:
            raise ValueError(f"Error calculating curves: {str(error)}") from error

    @staticmethod
    def calculate_equilibrium_and_surpluses(
        demand_intercept, demand_slope, supply_intercept, supply_slope
    ):
        """
        Calculate equilibrium point and surpluses.

        Args:
            demand_intercept: Demand curve intercept
            demand_slope: Demand curve slope
            supply_intercept: Supply curve intercept
            supply_slope: Supply curve slope

        Returns:
            dict: Dictionary containing equilibrium and surplus data

        Raises:
            ValueError: If calculation fails
        """
        try:
            # Calculate equilibrium
            equilibrium_price, equilibrium_quantity = calculate_equilibrium(
                demand_intercept, demand_slope, supply_intercept, supply_slope
            )

            # Calculate intercepts for surplus calculation
            demand_price_intercept = (
                -demand_intercept / demand_slope if demand_slope != 0 else float("inf")
            )
            supply_price_intercept = (
                -supply_intercept / supply_slope if supply_slope != 0 else float("inf")
            )

            # Calculate surpluses
            consumer_surplus, producer_surplus = calculate_surpluses(
                equilibrium_quantity,
                equilibrium_price,
                demand_price_intercept,
                supply_intercept,
                supply_price_intercept,
            )

            return {
                "equilibrium_price": equilibrium_price,
                "equilibrium_quantity": equilibrium_quantity,
                "consumer_surplus": consumer_surplus,
                "producer_surplus": producer_surplus,
                "total_surplus": consumer_surplus + producer_surplus,
            }

        except Exception as error:
            raise ValueError(f"Error calculating equilibrium: {str(error)}") from error


class GraphManager:
    """Handles graph creation and display."""

    def __init__(self):
        """Initialize GraphManager."""
        self._initialized = True

    def get_graph_types(self):
        """Get available graph types."""
        return ["supply_demand", "equilibrium", "surpluses"]

    @staticmethod
    def create_supply_demand_graph(results, graph_container):
        """
        Create and display supply and demand graph.

        Args:
            results: Dictionary containing calculation results
            graph_container: Tkinter container for the graph

        Returns:
            matplotlib.figure.Figure: The created figure
        """
        # Clear previous graph
        for widget in graph_container.winfo_children():
            widget.destroy()

        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 8))

        # Calculate curve points
        price_range = np.linspace(0, max(results["equilibrium_price"] * 1.5, 10), 100)
        demand_quantities = (
            results["demand_intercept"] + results["demand_slope"] * price_range
        )
        supply_quantities = (
            results["supply_intercept"] + results["supply_slope"] * price_range
        )

        # Plot curves using common function from funct.py
        _plot_curves_on_axis(ax, demand_quantities, supply_quantities, price_range)

        # Plot equilibrium point
        ax.scatter(
            [results["equilibrium_quantity"]],
            [results["equilibrium_price"]],
            color="green",
            s=100,
            zorder=5,
            label="Equilibrium Point",
        )

        # Add lines to equilibrium
        ax.axhline(
            results["equilibrium_price"], color="green", linestyle="--", alpha=0.7
        )
        ax.axvline(
            results["equilibrium_quantity"], color="green", linestyle="--", alpha=0.7
        )

        # Formatting
        ax.set_xlabel("Quantity (Q)", fontsize=12)
        ax.set_ylabel("Price (P)", fontsize=12)
        ax.set_title("Supply and Demand Curves", fontsize=14, fontweight="bold")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, graph_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        return fig


class ExportManager:
    """Handles data export functionality."""

    def __init__(self):
        """Initialize ExportManager."""
        self._initialized = True

    def get_supported_formats(self):
        """Get list of supported export formats."""
        return ["CSV", "JSON"]

    @staticmethod
    def export_results_to_csv(results, filename):
        """
        Export calculation results to CSV.

        Args:
            results: Dictionary containing calculation results
            filename: Output file path

        Returns:
            bool: True if successful

        Raises:
            ValueError: If export fails
        """
        try:
            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Parameter", "Value"])
                writer.writerow(["Demand Intercept", results["demand_intercept"]])
                writer.writerow(["Demand Slope", results["demand_slope"]])
                writer.writerow(["Supply Intercept", results["supply_intercept"]])
                writer.writerow(["Supply Slope", results["supply_slope"]])
                writer.writerow(["Equilibrium Price", results["equilibrium_price"]])
                writer.writerow(
                    ["Equilibrium Quantity", results["equilibrium_quantity"]]
                )
                writer.writerow(["Consumer Surplus", results["consumer_surplus"]])
                writer.writerow(["Producer Surplus", results["producer_surplus"]])
                writer.writerow(["Total Surplus", results["total_surplus"]])
            return True
        except Exception as error:
            raise ValueError(f"Export failed: {str(error)}") from error


class MicroeconomyApp:
    """Main application class for the Microeconomy Graph Tool."""

    def __init__(self, root):
        """
        Initialize the application.

        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Microeconomy Graph Tool")
        self.root.geometry("900x700")

        # Initialize managers and data storage
        self.managers = {
            "data": DataManager(),
            "calculator": Calculator(),
            "graph": GraphManager(),
            "export": ExportManager(),
        }
        self.app_data = {
            "results": {},
            "current_figure": None,
            "ui_components": {
                "data_frame": None,
                "demand_prices_entry": None,
                "demand_quantities_entry": None,
                "supply_prices_entry": None,
                "supply_quantities_entry": None,
                "results_frame": None,
                "results_container": None,
                "export_button": None,
                "graph_frame": None,
                "graph_container": None,
                "save_graph_button": None,
                "notebook": None,
            },
        }

        self.create_widgets()

    def create_widgets(self):
        """Create main application widgets."""
        # Create notebook for tabs
        self.app_data["ui_components"]["notebook"] = ttk.Notebook(self.root)
        self.app_data["ui_components"]["notebook"].pack(
            fill="both", expand=True, padx=10, pady=10
        )

        # Create tabs
        self.create_data_input_tab()
        self.create_results_tab()
        self.create_graph_tab()

    def create_data_input_tab(self):
        """Create the data input tab."""
        self.app_data["ui_components"]["data_frame"] = ttk.Frame(
            self.app_data["ui_components"]["notebook"]
        )
        self.app_data["ui_components"]["notebook"].add(
            self.app_data["ui_components"]["data_frame"], text="Data Input"
        )

        # Title
        title_label = ttk.Label(
            self.app_data["ui_components"]["data_frame"],
            text="Enter Supply and Demand Data",
            font=("Arial", 14, "bold"),
        )
        title_label.pack(pady=10)

        # Main container
        main_container = ttk.Frame(self.app_data["ui_components"]["data_frame"])
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Create input sections
        self.create_demand_section(main_container)
        self.create_supply_section(main_container)
        self.create_buttons_section(main_container)

    def create_demand_section(self, parent):
        """Create demand curve input section."""
        demand_frame = ttk.LabelFrame(parent, text="Demand Curve Data", padding=10)
        demand_frame.pack(fill="x", pady=10)

        ttk.Label(demand_frame, text="Price Values (comma separated):").pack(anchor="w")
        self.app_data["ui_components"]["demand_prices_entry"] = ttk.Entry(
            demand_frame, width=50
        )
        self.app_data["ui_components"]["demand_prices_entry"].pack(fill="x", pady=5)

        ttk.Label(demand_frame, text="Quantity Values (comma separated):").pack(
            anchor="w"
        )
        self.app_data["ui_components"]["demand_quantities_entry"] = ttk.Entry(
            demand_frame, width=50
        )
        self.app_data["ui_components"]["demand_quantities_entry"].pack(fill="x", pady=5)

    def create_supply_section(self, parent):
        """Create supply curve input section."""
        supply_frame = ttk.LabelFrame(parent, text="Supply Curve Data", padding=10)
        supply_frame.pack(fill="x", pady=10)

        ttk.Label(supply_frame, text="Price Values (comma separated):").pack(anchor="w")
        self.app_data["ui_components"]["supply_prices_entry"] = ttk.Entry(
            supply_frame, width=50
        )
        self.app_data["ui_components"]["supply_prices_entry"].pack(fill="x", pady=5)

        ttk.Label(supply_frame, text="Quantity Values (comma separated):").pack(
            anchor="w"
        )
        self.app_data["ui_components"]["supply_quantities_entry"] = ttk.Entry(
            supply_frame, width=50
        )
        self.app_data["ui_components"]["supply_quantities_entry"].pack(fill="x", pady=5)

    def create_buttons_section(self, parent):
        """Create buttons section."""
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=20)

        ttk.Button(
            button_frame, text="Load Example Data", command=self.load_example_data
        ).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Calculate", command=self.calculate_results).pack(
            side="left", padx=5
        )
        ttk.Button(button_frame, text="Clear All", command=self.clear_data).pack(
            side="left", padx=5
        )

    def create_results_tab(self):
        """Create the results tab."""
        self.app_data["ui_components"]["results_frame"] = ttk.Frame(
            self.app_data["ui_components"]["notebook"]
        )
        self.app_data["ui_components"]["notebook"].add(
            self.app_data["ui_components"]["results_frame"], text="Results"
        )

        # Title
        title_label = ttk.Label(
            self.app_data["ui_components"]["results_frame"],
            text="Calculation Results",
            font=("Arial", 14, "bold"),
        )
        title_label.pack(pady=10)

        # Results container
        self.app_data["ui_components"]["results_container"] = ttk.Frame(
            self.app_data["ui_components"]["results_frame"]
        )
        self.app_data["ui_components"]["results_container"].pack(
            fill="both", expand=True, padx=20, pady=10
        )

        # Export button
        self.app_data["ui_components"]["export_button"] = ttk.Button(
            self.app_data["ui_components"]["results_frame"],
            text="Export to CSV",
            command=self.export_to_csv,
        )
        self.app_data["ui_components"]["export_button"].pack(pady=10)
        self.app_data["ui_components"]["export_button"].config(state="disabled")

    def create_graph_tab(self):
        """Create the graph tab."""
        self.app_data["ui_components"]["graph_frame"] = ttk.Frame(
            self.app_data["ui_components"]["notebook"]
        )
        self.app_data["ui_components"]["notebook"].add(
            self.app_data["ui_components"]["graph_frame"], text="Graph"
        )

        # Title
        title_label = ttk.Label(
            self.app_data["ui_components"]["graph_frame"],
            text="Supply and Demand Graph",
            font=("Arial", 14, "bold"),
        )
        title_label.pack(pady=10)

        # Graph container
        self.app_data["ui_components"]["graph_container"] = ttk.Frame(
            self.app_data["ui_components"]["graph_frame"]
        )
        self.app_data["ui_components"]["graph_container"].pack(
            fill="both", expand=True, padx=20, pady=10
        )

        # Save button
        self.app_data["ui_components"]["save_graph_button"] = ttk.Button(
            self.app_data["ui_components"]["graph_frame"],
            text="Save Graph",
            command=self.save_graph,
        )
        self.app_data["ui_components"]["save_graph_button"].pack(pady=10)
        self.app_data["ui_components"]["save_graph_button"].config(state="disabled")

    def load_example_data(self):
        """Load example data from CSV file."""
        example_data = self.managers["data"].load_example_data_from_csv()
        if example_data:
            # Load demand data
            demand_prices_str = ",".join(map(str, example_data["demand_prices"]))
            demand_quantities_str = ",".join(
                map(str, example_data["demand_quantities"])
            )

            self.app_data["ui_components"]["demand_prices_entry"].delete(0, tk.END)
            self.app_data["ui_components"]["demand_prices_entry"].insert(
                0, demand_prices_str
            )
            self.app_data["ui_components"]["demand_quantities_entry"].delete(0, tk.END)
            self.app_data["ui_components"]["demand_quantities_entry"].insert(
                0, demand_quantities_str
            )

            # Load supply data
            supply_prices_str = ",".join(map(str, example_data["supply_prices"]))
            supply_quantities_str = ",".join(
                map(str, example_data["supply_quantities"])
            )

            self.app_data["ui_components"]["supply_prices_entry"].delete(0, tk.END)
            self.app_data["ui_components"]["supply_prices_entry"].insert(
                0, supply_prices_str
            )
            self.app_data["ui_components"]["supply_quantities_entry"].delete(0, tk.END)
            self.app_data["ui_components"]["supply_quantities_entry"].insert(
                0, supply_quantities_str
            )
        else:
            messagebox.showerror("Error", "Could not load example data from CSV file")

    def clear_data(self):
        """Clear all input fields."""
        self.app_data["ui_components"]["demand_prices_entry"].delete(0, tk.END)
        self.app_data["ui_components"]["demand_quantities_entry"].delete(0, tk.END)
        self.app_data["ui_components"]["supply_prices_entry"].delete(0, tk.END)
        self.app_data["ui_components"]["supply_quantities_entry"].delete(0, tk.END)

    def calculate_results(self):
        """Calculate all results and update interface."""
        try:
            # Parse input data
            demand_prices = self.managers["data"].parse_data_string(
                self.app_data["ui_components"]["demand_prices_entry"].get()
            )
            demand_quantities = self.managers["data"].parse_data_string(
                self.app_data["ui_components"]["demand_quantities_entry"].get()
            )
            supply_prices = self.managers["data"].parse_data_string(
                self.app_data["ui_components"]["supply_prices_entry"].get()
            )
            supply_quantities = self.managers["data"].parse_data_string(
                self.app_data["ui_components"]["supply_quantities_entry"].get()
            )

            # Validate data
            is_valid, error_message = self.managers["data"].validate_data(
                demand_prices, demand_quantities, supply_prices, supply_quantities
            )
            if not is_valid:
                messagebox.showerror("Error", error_message)
                return

            # Calculate curves
            (
                demand_intercept,
                demand_slope,
                supply_intercept,
                supply_slope,
            ) = self.managers["calculator"].calculate_curves(
                demand_prices, demand_quantities, supply_prices, supply_quantities
            )

            # Calculate equilibrium and surpluses
            equilibrium_data = self.managers[
                "calculator"
            ].calculate_equilibrium_and_surpluses(
                demand_intercept, demand_slope, supply_intercept, supply_slope
            )

            # Store all results
            self.app_data["results"] = {
                "demand_intercept": demand_intercept,
                "demand_slope": demand_slope,
                "supply_intercept": supply_intercept,
                "supply_slope": supply_slope,
                **equilibrium_data,
            }

            # Update interface
            self.update_results_tab()
            self.update_graph_tab()

            # Enable export buttons
            self.app_data["ui_components"]["export_button"].config(state="normal")
            self.app_data["ui_components"]["save_graph_button"].config(state="normal")

            # Switch to results tab
            self.app_data["ui_components"]["notebook"].select(1)

            messagebox.showinfo("Success", "Calculations completed successfully!")

        except ValueError as error:
            messagebox.showerror("Error", f"Calculation error: {str(error)}")

    def update_results_tab(self):
        """Update the results tab with calculated data."""
        # Clear previous results
        for widget in self.app_data["ui_components"][
            "results_container"
        ].winfo_children():
            widget.destroy()

        # Create results display
        results_text = f"""
Demand Curve:
  Intercept: {self.app_data['results']['demand_intercept']:.2f}
  Slope: {self.app_data['results']['demand_slope']:.2f}

Supply Curve:
  Intercept: {self.app_data['results']['supply_intercept']:.2f}
  Slope: {self.app_data['results']['supply_slope']:.2f}

Equilibrium Point:
  Price: ${self.app_data['results']['equilibrium_price']:.2f}
  Quantity: {self.app_data['results']['equilibrium_quantity']:.2f} units

Economic Surpluses:
  Consumer Surplus: ${self.app_data['results']['consumer_surplus']:.2f}
  Producer Surplus: ${self.app_data['results']['producer_surplus']:.2f}
  Total Surplus: ${self.app_data['results']['total_surplus']:.2f}
"""

        text_widget = tk.Text(
            self.app_data["ui_components"]["results_container"],
            height=15,
            width=50,
            font=("Courier", 10),
        )
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", results_text)
        text_widget.config(state="disabled")

    def update_graph_tab(self):
        """Update the graph tab with new graph."""
        self.app_data["current_figure"] = self.managers[
            "graph"
        ].create_supply_demand_graph(
            self.app_data["results"], self.app_data["ui_components"]["graph_container"]
        )

    def export_to_csv(self):
        """Export results to CSV file."""
        if not self.app_data["results"]:
            messagebox.showwarning("Warning", "No results to export")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )

        if filename:
            try:
                self.managers["export"].export_results_to_csv(
                    self.app_data["results"], filename
                )
                messagebox.showinfo("Success", f"Results exported to {filename}")
            except ValueError as error:
                messagebox.showerror("Error", str(error))

    def save_graph(self):
        """Save the current graph as image."""
        if not self.app_data["current_figure"]:
            messagebox.showwarning("Warning", "No graph to save")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("PDF files", "*.pdf"),
                ("All files", "*.*"),
            ],
        )

        if filename:
            try:
                self.app_data["current_figure"].savefig(
                    filename, dpi=300, bbox_inches="tight"
                )
                messagebox.showinfo("Success", f"Graph saved to {filename}")
            except (OSError, ValueError) as error:
                messagebox.showerror("Error", f"Save failed: {str(error)}")


def main():
    """Main application entry point."""
    root = tk.Tk()
    MicroeconomyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
