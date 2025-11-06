"""
Visualization of Linear Programming Optimization for Furniture Production

This script creates a graphical representation of the feasible region,
constraints, and optimal solution for the furniture production problem.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for CLI environments

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from optimize_furniture import solve_furniture_optimization


def plot_optimization(profit_per_table=50, profit_per_chair=30, save_file='optimization_plot.png'):
    """
    Create a visualization of the linear programming problem.

    Args:
        profit_per_table: Profit per table (default: 50)
        profit_per_chair: Profit per chair (default: 30)
        save_file: Filename to save the plot (default: 'optimization_plot.png')
    """

    # Solve the optimization problem
    solution = solve_furniture_optimization(profit_per_table, profit_per_chair)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 10))

    # Define ranges for T and C
    T = np.linspace(0, 600, 1000)

    # Constraint 1: Carpentry time - 3T + 4C ≤ 2400
    # Rearranged: C ≤ (2400 - 3T) / 4
    C1 = (2400 - 3 * T) / 4

    # Constraint 2: Painting time - 2T + 1C ≤ 1000
    # Rearranged: C ≤ 1000 - 2T
    C2 = 1000 - 2 * T

    # Constraint 3: C ≤ 450
    C3 = np.full_like(T, 450)

    # Constraint 4: T ≥ 100
    T_min = 100

    # Plot constraint lines
    ax.plot(T, C1, 'r-', linewidth=2, label='Carpentry: 3T + 4C ≤ 2400', alpha=0.7)
    ax.plot(T, C2, 'b-', linewidth=2, label='Painting: 2T + C ≤ 1000', alpha=0.7)
    ax.plot(T, C3, 'g-', linewidth=2, label='Max Chairs: C ≤ 450', alpha=0.7)
    ax.axvline(x=T_min, color='purple', linewidth=2, label='Min Tables: T ≥ 100', alpha=0.7)

    # Find the feasible region vertices
    # We need to find intersection points of the constraints
    vertices = []

    # Intersection of T = 100 and C = 450
    vertices.append((100, 450))

    # Intersection of T = 100 and carpentry constraint
    C_at_T100_carp = (2400 - 3 * 100) / 4
    vertices.append((100, C_at_T100_carp))

    # Intersection of T = 100 and painting constraint
    C_at_T100_paint = 1000 - 2 * 100
    vertices.append((100, C_at_T100_paint))

    # Intersection of carpentry and painting constraints
    # 3T + 4C = 2400 and 2T + C = 1000
    # From second: C = 1000 - 2T
    # Substitute: 3T + 4(1000 - 2T) = 2400
    # 3T + 4000 - 8T = 2400
    # -5T = -1600
    # T = 320, C = 360
    vertices.append((320, 360))

    # Intersection of painting constraint and C = 450
    # 2T + 450 = 1000 => T = 275
    vertices.append((275, 450))

    # Intersection of carpentry constraint and C = 450
    # 3T + 4(450) = 2400 => 3T = 600 => T = 200
    vertices.append((200, 450))

    # Filter vertices that satisfy all constraints
    feasible_vertices = []
    for t, c in vertices:
        if (t >= 100 and  # T ≥ 100
            c <= 450 and  # C ≤ 450
            3*t + 4*c <= 2400 and  # Carpentry
            2*t + c <= 1000 and  # Painting
            t >= 0 and c >= 0):
            feasible_vertices.append((t, c))

    # Remove duplicates and sort
    feasible_vertices = list(set(feasible_vertices))

    # Sort vertices by angle from centroid for proper polygon plotting
    if feasible_vertices:
        centroid_t = sum(t for t, c in feasible_vertices) / len(feasible_vertices)
        centroid_c = sum(c for t, c in feasible_vertices) / len(feasible_vertices)

        def angle_from_centroid(vertex):
            return np.arctan2(vertex[1] - centroid_c, vertex[0] - centroid_t)

        feasible_vertices.sort(key=angle_from_centroid)

        # Plot feasible region
        polygon = Polygon(feasible_vertices, alpha=0.3, color='yellow',
                         edgecolor='black', linewidth=2, label='Feasible Region')
        ax.add_patch(polygon)

    # Plot optimal solution
    optimal_T = solution['optimal_tables']
    optimal_C = solution['optimal_chairs']
    ax.plot(optimal_T, optimal_C, 'r*', markersize=30,
           label=f'Optimal Solution: T={optimal_T:.0f}, C={optimal_C:.0f}', zorder=5)

    # Add annotation for optimal point
    ax.annotate(f'Optimal: ({optimal_T:.0f}, {optimal_C:.0f})\nProfit: ${solution["max_profit"]:.0f}',
                xy=(optimal_T, optimal_C), xytext=(optimal_T + 50, optimal_C + 50),
                fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=2))

    # Plot iso-profit lines (objective function)
    # Profit = profit_per_table * T + profit_per_chair * C
    # C = (Profit - profit_per_table * T) / profit_per_chair
    profit_levels = np.linspace(5000, solution['max_profit'], 5)
    for profit_level in profit_levels:
        C_profit = (profit_level - profit_per_table * T) / profit_per_chair
        if profit_level == solution['max_profit']:
            ax.plot(T, C_profit, 'k--', linewidth=2, alpha=0.8,
                   label=f'Max Profit Line: ${profit_level:.0f}')
        else:
            ax.plot(T, C_profit, 'k:', linewidth=1, alpha=0.3)

    # Set axis limits and labels
    ax.set_xlim(0, 600)
    ax.set_ylim(0, 700)
    ax.set_xlabel('Tables (T)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Chairs (C)', fontsize=14, fontweight='bold')
    ax.set_title('Linear Programming: Furniture Production Optimization\n' +
                f'Objective: Maximize Profit = ${profit_per_table}T + ${profit_per_chair}C',
                fontsize=16, fontweight='bold', pad=20)

    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--')

    # Add legend
    ax.legend(loc='upper right', fontsize=10, framealpha=0.9)

    # Add constraint text box
    constraint_text = (
        'Constraints:\n'
        f'• Carpentry: 3T + 4C ≤ 2,400\n'
        f'• Painting: 2T + C ≤ 1,000\n'
        f'• Chairs: C ≤ 450\n'
        f'• Tables: T ≥ 100'
    )
    ax.text(0.02, 0.98, constraint_text, transform=ax.transAxes,
           fontsize=11, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Tight layout
    plt.tight_layout()

    # Save the figure
    plt.savefig(save_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Visualization saved to: {save_file}")

    return fig, ax


def main():
    """Main function to create the visualization."""
    print("Creating visualization of furniture production optimization...")
    plot_optimization(profit_per_table=50, profit_per_chair=30)
    print("\nVisualization complete!")


if __name__ == "__main__":
    main()
