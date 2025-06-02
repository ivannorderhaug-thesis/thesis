from collections import defaultdict, Counter
from math import ceil
import json

def order_dict(d):
    """
    Returns a new dictionary with keys sorted alphabetically.
    """
    return {k: d[k] for k in sorted(d)}

def aggregate_results(data, save=False):
    """
    Aggregates the results of multiple runs of the same test case.
    
    For each test case:
      - Each result is a dictionary mapping symbols to lists of variants.
      - For each symbol, the variants are counted across runs.
      - A variant is kept if its count is at least the computed minimum presence
        (based on the number of runs).
      - Variants are sorted based on their appearance order in the first run.
      - The aggregated actual components remain as a dictionary (symbol -> [variants])
        and are sorted alphabetically by key.
      - The expected components (provided as a dictionary) are similarly sorted.
    
    Returns a list of dictionaries with:
      - input: the test case input.
      - expected_components: the expected components as a sorted dictionary.
      - actual_components: the aggregated components as a sorted dictionary.
    """
    aggregated_items = []
    
    for item in data:
        results_list = item.get("results", [])
        total_runs = len(results_list)
        computed_min_presence = 1 if total_runs == 1 else max(2, ceil(total_runs / 2))
        symbol_variant_counts = defaultdict(Counter)
        first_run_order = defaultdict(list)
        
        # Iterate over all runs and count the occurrences of each variant for each symbol.
        for i, res in enumerate(results_list):
            for symbol, variants in res.items():
                for variant in variants:
                    if i == 0 and variant not in first_run_order[symbol]:
                        first_run_order[symbol].append(variant)
                    symbol_variant_counts[symbol][variant] += 1
        
        aggregated_variants = {}
        # For each symbol, filter variants by the computed minimum presence.
        # The variants are sorted according to their order in the first run.
        for symbol, counter in symbol_variant_counts.items():
            qualifying = [variant for variant, count in counter.items() if count >= computed_min_presence]
            qualifying.sort(key=lambda x: first_run_order[symbol].index(x) if x in first_run_order[symbol] else 999)
            if qualifying:
                aggregated_variants[symbol] = qualifying
        
        # Sort the dictionaries alphabetically by their keys.
        ordered_aggregated = order_dict(aggregated_variants)
        ordered_expected = order_dict(item.get("expected_components", {}))
        
        aggregated_items.append({
            "input": item.get("input", ""),
            "expected_components": ordered_expected,
            "actual_components": ordered_aggregated
        })

    if save:
        with open("data/aggregated_results.json", "w") as f:
            json.dump(aggregated_items, f, indent=2)
        
    return aggregated_items
