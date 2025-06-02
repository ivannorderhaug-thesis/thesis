import unittest
from util.aggregation import aggregate_results

class TestAggregation(unittest.TestCase):
    def test_basic_consistency(self):
        data = [
            {
                "input": "The commission shall optimize public investment.",
                "expected_components": {
                    "A": ["commission"],
                    "D": ["shall"],
                    "I": ["optimize"],
                    "Bdir": ["investment"],
                    "Bdir,p": ["public"]
                },
                "results": [
                    {
                        "A": ["commission"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["investment"],
                        "Bdir,p": ["public"]
                    },
                    {
                        "A": ["commission"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["investment"],
                        "Bdir,p": ["public"]
                    },
                    {
                        "A": ["commission"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["investment"],
                        "Bdir,p": ["public"]
                    },
                    {
                        "A": ["commission"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["investment"],
                        "Bdir,p": ["public"]
                    },
                    {
                        "A": ["commission"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["investment"],
                        "Bdir,p": ["public"]
                    }
                ]
            }
        ]
        expected_aggregated = {
            "A": ["commission"],
            "D": ["shall"],
            "I": ["optimize"],
            "Bdir": ["investment"],
            "Bdir,p": ["public"]
        }
        aggregated = aggregate_results(data)
        self.assertEqual(aggregated[0]["actual_components"], expected_aggregated)
    
    def test_single_run(self):
        data = [
            {
                "input": "The commission shall optimize public investment.",
                "expected_components": {
                    "A": ["commission"],
                    "D": ["shall"],
                    "I": ["optimize"],
                    "Bdir": ["investment"],
                    "Bdir,p": ["public"]
                },
                "results": [
                    {
                        "A": ["commission"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["investment"],
                        "Bdir,p": ["public"]
                    }
                ]
            }
        ]
        expected_aggregated = {
            "A": ["commission"],
            "D": ["shall"],
            "I": ["optimize"],
            "Bdir": ["investment"],
            "Bdir,p": ["public"]
        }
        aggregated = aggregate_results(data)
        self.assertEqual(aggregated[0]["actual_components"], expected_aggregated)
    
    def test_missing_component(self):
        data = [
            {
                "input": "The commission shall optimize public investment.",
                "expected_components": {
                    "A": ["commission"],
                    "D": ["shall"],
                    "I": ["optimize"],
                    "Bdir": ["investment"],
                    "Bdir,p": ["public"]
                },
                "results": [
                    {
                        "A": ["commission"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["public investment"]
                    },
                    {
                        "A": ["commission"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["public investment"]
                    },
                    {
                        "A": ["commission"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["public investment"]
                    },
                    {
                        "A": ["commission"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["public investment"]
                    },
                    {
                        "A": ["commission"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["investment"],
                        "Bdir,p": ["public"]
                    }
                ]
            }
        ]
        # Here, for "Bdir": "public investment" appears in 4 out of 5 runs (>=3),
        # so aggregated actual components should keep that value and drop "investment".
        expected_aggregated = {
            "A": ["commission"],
            "D": ["shall"],
            "I": ["optimize"],
            "Bdir": ["public investment"]
        }
        aggregated = aggregate_results(data)
        self.assertEqual(aggregated[0]["actual_components"], expected_aggregated)

    def test_tie_between_components(self):
        data = [
            {
                "input": "The commission shall optimize public investment.",
                "expected_components": {
                    "A": ["the commission", "commission"],
                    "D": ["shall"],
                    "I": ["optimize"],
                    "Bdir": ["investment"],
                    "Bdir,p": ["public"]
                },
                "results": [
                    {
                        "A": ["the commission"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["investment"],
                        "Bdir,p": ["public"]
                    },
                    {
                        "A": ["the commission"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["investment"],
                        "Bdir,p": ["public"]
                    },
                    {
                        "A": ["commission"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["investment"],
                        "Bdir,p": ["public"]
                    },
                    {
                        "A": ["commission"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["investment"],
                        "Bdir,p": ["public"]
                    }
                ]
            }
        ]
        # Both variants for A occur twice, so both should be kept.
        expected_aggregated = {
            "A": ["the commission", "commission"],
            "D": ["shall"],
            "I": ["optimize"],
            "Bdir": ["investment"],
            "Bdir,p": ["public"]
        }
        aggregated = aggregate_results(data)
        self.assertEqual(aggregated[0]["actual_components"], expected_aggregated)
    
    def test_multiple_variants_same_symbol(self):
        data = [
            {
                "input": "The Energy Commission and Board of Directors shall optimize public investment.",
                "expected_components": {
                    "A": ["The Energy Commission", "Board of Directors"],
                    "D": ["shall"],
                    "I": ["optimize"],
                    "Bdir": ["investment"],
                    "Bdir,p": ["public"]
                },
                "results": [
                    {
                        "A": ["The Energy Commission", "Board of Directors"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["investment"],
                        "Bdir,p": ["public"]
                    },
                    {
                        "A": ["The Energy Commission", "Board of Directors"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["investment"],
                        "Bdir,p": ["public"]
                    },
                    {
                        "A": ["The Energy Commission", "Board of Directors"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["investment"],
                        "Bdir,p": ["public"]
                    },
                    {
                        "A": ["The Energy Commission", "Board of Directors"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["investment"],
                        "Bdir,p": ["public"]
                    },
                    {
                        "A": ["The Energy Commission", "Board of Directors"],
                        "D": ["shall"],
                        "I": ["optimize"],
                        "Bdir": ["investment"],
                        "Bdir,p": ["public"]
                    }
                ]
            }
        ]
        expected_aggregated = {
            "A": ["The Energy Commission", "Board of Directors"],
            "D": ["shall"],
            "I": ["optimize"],
            "Bdir": ["investment"],
            "Bdir,p": ["public"]
        }
        aggregated = aggregate_results(data)
        self.assertEqual(aggregated[0]["actual_components"], expected_aggregated)
    
if __name__ == "__main__":
    unittest.main()
