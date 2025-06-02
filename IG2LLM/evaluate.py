import json
import logging
from pathlib import Path
import sys
from typing import Dict, List, Tuple

import argparse
from dotenv import load_dotenv
from tqdm import tqdm
from tabulate import tabulate

from services.llm_interface import LLMConfig, LLMInterface
from util import csv_to_json
from util.aggregation import aggregate_results
from metrics import (
    compute_component_metrics,
    compute_aggregate_metrics_with_ci
)
from model.classes import Regulative, Constitutive
from prompt_templates.registry import get_template

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

for logger_name in ("openai", "openai.api_requestor", "httpx"):
    logging.getLogger(logger_name).setLevel(logging.WARNING)

def load_prompts(statement_type: str, include_examples: bool) -> Dict[str, str]:
    """
    Read all prompt fragments (definitions, guidelines, examples, statement_information, logical operators)
    and return a dict of their contents.
    """
    base = Path("prompts")
    fragments = {
        "definitions":            f"{statement_type}_definitions.txt",
        "guidelines":             f"{statement_type}_guidelines.txt",
        "statement_information":  f"{statement_type}_information.txt",
        "logical":                "logical_operator.txt",
    }
    if include_examples:
        fragments["examples"] = f"{statement_type}_examples.txt"

    contents: Dict[str, str] = {}
    for key, fname in fragments.items():
        path = base / fname
        try:
            contents[key] = path.read_text()
            logging.debug("Loaded prompt fragment %s", path)
        except FileNotFoundError:
            logging.error("Required prompt file not found: %s", path)
            raise
    return contents


def run_llm_on_data(
    data: List[Dict],
    llm: LLMInterface,
    system_text: str,
    runs: int,
    statement_type: str,
    include_logic: bool = False,
) -> List[Dict]:
    """
    Call the LLM on each statement, tracking progress with tqdm.
    """
    output: List[Dict] = []
    ResponseClass = Regulative if statement_type == "regulative" else Constitutive

    if include_logic:
        lo_prompt = load_prompts(statement_type, include_examples=False)["logical"]

    for item in tqdm(data, desc="Extraction", unit="stmt", file=sys.stdout):

        resp = llm.run(
            user_prompt=item["input"],
            system_prompt=system_text,
            runs=runs,
            response_model=ResponseClass,
            lo_prompt=(lo_prompt if include_logic else "")
        )

        output.append({
            "input":               item["input"],
            "expected_components": item.get("expected_components"),
            "results":             resp,
        })
    return output

def save_json(data: List[Dict], path: Path) -> None:
    """
    Serialize `data` to the given JSON file.
    """
    path.write_text(json.dumps(data, indent=4))
    logging.info("Saved results to %s", path)


def load_json(path: Path) -> List[Dict]:
    """
    Load JSON from file, or return None if not present.
    """
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return None


def display_metrics(
    component_metrics: Dict[str, Dict[str, float]],
    aggregate_cis: Dict[str, Dict[str, any]],
    total: int
) -> None:
    """
    Display the metrics in a formatted table.
    """
    logging.info("Total statements processed: %d", total)

    # Content-Level
    print("\nContent-Level Metrics:")
    headers1 = ["Component", "Precision", "Recall", "F1"]
    rows1 = [
        [
            comp,
            f"{m.get('precision', 0):.3f}",
            f"{m.get('recall',    0):.3f}",
            f"{m.get('f1',        0):.3f}"
        ]
        for comp, m in component_metrics.items()
    ]
    print(tabulate(rows1, headers=headers1, tablefmt="github"))

    # Aggregate-Level with CIs
    print("\nAggregate Content-Level Metrics:")
    headers2 = ["Type", "Precision", "Recall", "F1 (95% CI)"]

    rows2 = []
    for agg_type, m in aggregate_cis.items():
        rows2.append([
            agg_type,
            f"{m['precision']:.3f}",
            f"{m['recall']:.3f}",
            f"{m['f1']:.3f} ({m['ci'][0]:.3f} - {m['ci'][1]:.3f})"
        ])
    print(tabulate(rows2, headers=headers2, tablefmt="github"))

def main(
    runs: int,
    statement_type: str,
    difficulty: str,
    include_examples: bool,
    provider: str,
):
    # Load data and prepare output paths
    data_csv = Path(f"data/{difficulty}_{statement_type}_statements.csv")
    if not data_csv.exists():
        logging.error("Data file not found: %s", data_csv)
        return
    
    out_dir = Path("results")
    out_dir.mkdir(exist_ok=True)
    if not out_dir.is_dir():
        logging.error("Results directory not found: %s", out_dir)
        return

    out_json = Path("results") / data_csv.with_name(
        provider + "_" + data_csv.stem + ("_with_examples" if include_examples else "") + "_results.json"
    ).name

    # Check for cached results
    results = load_json(out_json)
    if results is None:
        logging.info("No cached results found, invoking LLM…")
        # Convert CSV to JSON format
        data = csv_to_json(str(data_csv), statement_type=statement_type)
        # Load prompt fragments
        prompts = load_prompts(statement_type, include_examples)
        # Prepare the system prompt
        template_name = f"{statement_type}_with_examples" if include_examples else statement_type
        template = get_template(template_name)
        system_text = template.format(
            statement_type=statement_type,
            definitions=prompts["definitions"],
            guidelines=prompts["guidelines"],
            statement_information=prompts["statement_information"],
            examples=prompts.get("examples", ""),
        )

        print(system_text)  # Debug: print the system prompt

        # Initialize the LLM interface
        config = LLMConfig(
            provider=provider,           
            temperature=0.0,             
            timeout=15,                  
        )

        llm = LLMInterface(
            config=config,
        )

        # Run the LLM on the data
        results = run_llm_on_data(
            data,
            llm,
            system_text,
            runs,
            statement_type,
            include_logic=(difficulty == "hard")
        )
        save_json(results, out_json)
    else:
        logging.info("Loaded cached results from %s", out_json)

    # Aggregate & compute metrics
    aggregated = aggregate_results(results, save=False)
    comp_metrics = compute_component_metrics(aggregated)
    agg_with_ci   = compute_aggregate_metrics_with_ci(
        aggregated,
        bootstrap_iterations=1000,
        seed=42
    )

    # Display all four metric tables
    display_metrics(comp_metrics, agg_with_ci, total=len(results))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run classification experiments over statements."
    )
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--type", choices=["r","c"], default="r")
    parser.add_argument("--level",choices=["1","2","3"], default="1")
    parser.add_argument("--examples", action="store_true")
    parser.add_argument("--provider", choices=["openai","deepseek","gemini","claude"], default="openai")
    args = parser.parse_args()

    statement_type = "regulative" if args.type == "r" else "constitutive"
    difficulty = { "1": "easy", "2": "medium", "3": "hard" }[args.level]

    main(
        runs=args.runs,
        statement_type=statement_type,
        difficulty=difficulty,
        include_examples=args.examples,
        provider=args.provider
    )
