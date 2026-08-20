from usembridge.solvers.semantic_gap import run_semantic_gap_demo

if __name__ == "__main__":
    result = run_semantic_gap_demo()
    print("With faithful encoding:")
    print(f"  violation possible: {result.violation_possible}")
    print(f"  no violation possible: {result.no_violation_possible}")
    print("  => violation is not entailed because exception applicability is unresolved")
    print("With naive 'not recorded' -> 'does not apply' mapping:")
    print(f"  violation forced: {result.naive_mapping_forces_violation}")
