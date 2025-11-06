"""
Linear Programming Optimization for Furniture Production
Solves for optimal number of tables (T) and chairs (C) to produce.

Constraints:
1. Carpentry time: 3T + 4C ≤ 2,400
2. Painting time: 2T + 1C ≤ 1,000
3. Chairs sold: C ≤ 450
4. Tables sold: T ≥ 100

Objective: Maximize profit (you can modify profit_per_table and profit_per_chair)
"""

from pulp import LpMaximize, LpProblem, LpVariable, LpStatus, value


def solve_furniture_optimization(profit_per_table=50, profit_per_chair=30):
    """
    Solve the furniture production optimization problem.

    Args:
        profit_per_table: Profit earned per table (default: 50)
        profit_per_chair: Profit earned per chair (default: 30)

    Returns:
        dict: Solution containing optimal values and profit
    """

    # Create the LP problem
    problem = LpProblem("Furniture_Production_Optimization", LpMaximize)

    # Decision variables (T = tables, C = chairs)
    # Both must be non-negative
    T = LpVariable("Tables", lowBound=0, cat='Continuous')
    C = LpVariable("Chairs", lowBound=0, cat='Continuous')

    # Objective function: Maximize profit
    problem += profit_per_table * T + profit_per_chair * C, "Total_Profit"

    # Constraint 1: Carpentry time
    problem += 3 * T + 4 * C <= 2400, "Carpentry_Time"

    # Constraint 2: Painting time
    problem += 2 * T + 1 * C <= 1000, "Painting_Time"

    # Constraint 3: Maximum chairs sold
    problem += C <= 450, "Max_Chairs_Sold"

    # Constraint 4: Minimum tables sold
    problem += T >= 100, "Min_Tables_Sold"

    # Solve the problem
    problem.solve()

    # Extract results
    status = LpStatus[problem.status]
    optimal_tables = value(T)
    optimal_chairs = value(C)
    max_profit = value(problem.objective)

    # Calculate resource utilization
    carpentry_used = 3 * optimal_tables + 4 * optimal_chairs
    painting_used = 2 * optimal_tables + 1 * optimal_chairs

    return {
        "status": status,
        "optimal_tables": optimal_tables,
        "optimal_chairs": optimal_chairs,
        "max_profit": max_profit,
        "carpentry_used": carpentry_used,
        "carpentry_available": 2400,
        "painting_used": painting_used,
        "painting_available": 1000,
        "problem": problem
    }


def print_solution(solution):
    """Print the solution in a readable format."""

    print("=" * 60)
    print("FURNITURE PRODUCTION OPTIMIZATION RESULTS")
    print("=" * 60)

    print(f"\nSolver Status: {solution['status']}")

    if solution['status'] == 'Optimal':
        print("\n--- OPTIMAL SOLUTION ---")
        print(f"Tables to produce (T): {solution['optimal_tables']:.2f}")
        print(f"Chairs to produce (C): {solution['optimal_chairs']:.2f}")
        print(f"Maximum Profit: ${solution['max_profit']:.2f}")

        print("\n--- RESOURCE UTILIZATION ---")
        carpentry_pct = (solution['carpentry_used'] / solution['carpentry_available']) * 100
        painting_pct = (solution['painting_used'] / solution['painting_available']) * 100

        print(f"Carpentry time: {solution['carpentry_used']:.2f} / {solution['carpentry_available']} hours ({carpentry_pct:.1f}%)")
        print(f"Painting time: {solution['painting_used']:.2f} / {solution['painting_available']} hours ({painting_pct:.1f}%)")

        print("\n--- CONSTRAINT VERIFICATION ---")
        print(f"✓ Carpentry: 3T + 4C = {solution['carpentry_used']:.2f} ≤ 2,400")
        print(f"✓ Painting: 2T + 1C = {solution['painting_used']:.2f} ≤ 1,000")
        print(f"✓ Chairs: C = {solution['optimal_chairs']:.2f} ≤ 450")
        print(f"✓ Tables: T = {solution['optimal_tables']:.2f} ≥ 100")

    else:
        print(f"\nNo optimal solution found. Status: {solution['status']}")

    print("=" * 60)


def main():
    """Main function to run the optimization."""

    # Solve with default profit values
    print("Solving with default values (Profit: $50 per table, $30 per chair)...\n")
    solution = solve_furniture_optimization(profit_per_table=50, profit_per_chair=30)
    print_solution(solution)

    # You can also try different profit scenarios
    print("\n\n")
    print("Solving with alternative values (Profit: $60 per table, $40 per chair)...\n")
    solution2 = solve_furniture_optimization(profit_per_table=60, profit_per_chair=40)
    print_solution(solution2)


if __name__ == "__main__":
    main()
