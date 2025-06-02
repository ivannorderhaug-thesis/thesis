from collections import defaultdict
import numpy as np

def compute_component_metrics(aggregated_test_results):
    """
    Compute component-level metrics from aggregated test results.
    Args:
        aggregated_test_results (list): List of dictionaries containing expected and actual components.
            Each dictionary should have keys "expected_components" and "actual_components".
    Returns:
        dict: A dictionary where keys are component symbols and values are dictionaries with metrics.
            Each value dictionary contains:
                - "tp": True Positives
                - "fp": False Positives
                - "fn": False Negatives
                - "expected_count": Total expected variants for the component
                - "aggregated_count": Total actual variants found in the aggregated results
                - "precision": Precision of the component
                - "recall": Recall of the component
                - "f1": F1 score of the component
    """
    component_metrics = defaultdict(lambda: {
        "tp": 0, "fp": 0, "fn": 0,
        "expected_count": 0, "aggregated_count": 0
    })

    for item in aggregated_test_results:
        expected_dict = item.get("expected_components", {})
        actual_dict = item.get("actual_components", {})

        expected_components = set(expected_dict.keys())
        actual_components = set(actual_dict.keys())

        for symbol in expected_components.union(actual_components):

            expected_variants = set(expected_dict.get(symbol, []))
            actual_variants = set(actual_dict.get(symbol, []))

            tp = len(expected_variants & actual_variants)
            fp = len(actual_variants - expected_variants)
            fn = len(expected_variants - actual_variants) 

            component_metrics[symbol]["tp"] += tp
            component_metrics[symbol]["fp"] += fp
            component_metrics[symbol]["fn"] += fn
            component_metrics[symbol]["expected_count"] += len(expected_variants)
            component_metrics[symbol]["aggregated_count"] += len(actual_variants)

    for symbol, metrics in component_metrics.items():
        tp = metrics["tp"]
        fp = metrics["fp"]
        fn = metrics["fn"]

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        metrics["precision"] = precision
        metrics["recall"] = recall
        metrics["f1"] = f1

    return component_metrics

def compute_aggregate_metrics(component_metrics):
    """
    Compute aggregate metrics from component-level metrics.
    Args:
        component_metrics (dict): A dictionary where keys are component symbols and values are dictionaries with metrics.
            Each value dictionary contains:
                - "tp": True Positives
                - "fp": False Positives
                - "fn": False Negatives
                - "precision": Precision of the component
                - "recall": Recall of the component
                - "f1": F1 score of the component
    Returns:
        dict: A dictionary with aggregate metrics:
            - "micro": Dictionary with micro-averaged precision, recall, and F1 score
            - "macro": Dictionary with macro-averaged precision, recall, and F1 score
    """
    total_tp = sum(m["tp"] for m in component_metrics.values())
    total_fp = sum(m["fp"] for m in component_metrics.values())
    total_fn = sum(m["fn"] for m in component_metrics.values())
    
    micro_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
    micro_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
    micro_f1 = (2 * micro_precision * micro_recall / (micro_precision + micro_recall)
                if (micro_precision + micro_recall) > 0 else 0)
    
    num_prefixes = len(component_metrics)
    macro_precision = sum(m["precision"] for m in component_metrics.values()) / num_prefixes if num_prefixes > 0 else 0
    macro_recall = sum(m["recall"] for m in component_metrics.values()) / num_prefixes if num_prefixes > 0 else 0
    macro_f1 = sum(m["f1"] for m in component_metrics.values()) / num_prefixes if num_prefixes > 0 else 0

    return {
        "micro": {"precision": micro_precision, "recall": micro_recall, "f1": micro_f1},
        "macro": {"precision": macro_precision, "recall": macro_recall, "f1": macro_f1}
    }

def compute_aggregate_metrics_with_ci(aggregated_test_results, bootstrap_iterations=1000, seed=None):
    """
    Compute aggregate metrics with confidence intervals using bootstrap sampling.
    Args:
        aggregated_test_results (list): List of dictionaries containing expected and actual components.
            Each dictionary should have keys "expected_components" and "actual_components".
        bootstrap_iterations (int): Number of bootstrap iterations to perform.
        seed (int, optional): Random seed for reproducibility.
    Returns:
        dict: A dictionary with aggregate metrics and confidence intervals:
            - "micro": Dictionary with micro-averaged precision, recall, F1 score, and confidence interval
            - "macro": Dictionary with macro-averaged precision, recall, F1 score, and confidence interval
    """
    if seed is not None:
        np.random.seed(seed)

    component_metrics = compute_component_metrics(aggregated_test_results)
    aggregate_metrics = compute_aggregate_metrics(component_metrics)

    micro_scores = []
    macro_scores = []

    for _ in range(bootstrap_iterations):
        sample = [np.random.choice(aggregated_test_results) for _ in range(len(aggregated_test_results))]
        sample_component_metrics = compute_component_metrics(sample)
        sample_aggregate_metrics = compute_aggregate_metrics(sample_component_metrics)

        micro_scores.append(sample_aggregate_metrics["micro"]["f1"])
        macro_scores.append(sample_aggregate_metrics["macro"]["f1"])

    lo_micro, hi_micro = np.percentile(micro_scores, [2.5, 97.5])
    lo_macro, hi_macro = np.percentile(macro_scores, [2.5, 97.5])

    return {
        "micro": {"precision": aggregate_metrics["micro"]["precision"],
                  "recall": aggregate_metrics["micro"]["recall"],
                  "f1": aggregate_metrics["micro"]["f1"],
                  "ci": (lo_micro, hi_micro)},
        "macro": {"precision": aggregate_metrics["macro"]["precision"],
                  "recall": aggregate_metrics["macro"]["recall"],
                  "f1": aggregate_metrics["macro"]["f1"],
                  "ci": (lo_macro, hi_macro)}
        }   
