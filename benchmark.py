import os
import json
import time
import traceback
from importlib import util

PROBLEMS = [
    {"id": "HumanEval/3", "name": "below_zero"},
    {"id": "HumanEval/5", "name": "intersperse"},
    {"id": "HumanEval/6", "name": "parse_nested_parens"},
    {"id": "HumanEval/13", "name": "greatest_common_divisor"},
    {"id": "HumanEval/17", "name": "parse_music"},
    {"id": "HumanEval/19", "name": "sort_numbers"},
    {"id": "HumanEval/26", "name": "factorize"},
    {"id": "HumanEval/32", "name": "find_zero"},
    {"id": "HumanEval/47", "name": "median"},
    {"id": "HumanEval/71", "name": "triangle_area"},
    {"id": "HumanEval/73", "name": "smallest_change"},
    {"id": "HumanEval/83", "name": "starts_one_ends"},
    {"id": "HumanEval/93", "name": "encode"},
    {"id": "HumanEval/95", "name": "check_dict_case"},
    {"id": "HumanEval/99", "name": "closest_integer"}
]

def load_test_cases():
    test_cases = {}
    for problem in PROBLEMS:
        filename = f"test_cases/{problem['id'].replace('/', '_')}.json"
        try:
            with open(filename, 'r') as f:
                test_cases[problem['id']] = json.load(f)
        except FileNotFoundError:
            print(f"Warning: No test cases found for {problem['id']}")
            test_cases[problem['id']] = {"test_cases": []}
    return test_cases

def load_solution(problem_id, func_name):
    filename = f"solutions/{problem_id.replace('/', '_')}_solution.py"
    try:
        spec = util.spec_from_file_location(func_name, filename)
        if spec is None:
            print(f"Error: Could not load {filename}")
            return None
        
        module = util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, func_name):
            return getattr(module, func_name)
        else:
            print(f"Error: Function {func_name} not found in {filename}")
            return None
    except Exception as e:
        print(f"Error loading solution for {problem_id}: {e}")
        return None

def run_test_case(func, test_case):
    try:
        inputs = test_case["inputs"]
        expected = test_case["output"]
        
        # Time execution
        start_time = time.time()
        result = func(*inputs)
        execution_time = time.time() - start_time
        
        passed = result == expected
        
        return {
            "passed": passed,
            "execution_time": execution_time,
            "result": result,
            "expected": expected
        }
    except Exception as e:
        return {
            "passed": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

def evaluate_solution(problem_id, func_name, test_cases):
    solution_func = load_solution(problem_id, func_name)
    if solution_func is None:
        return {
            "status": "failed",
            "error": "Could not load solution",
            "test_results": []
        }
    
    problem_test_cases = test_cases[problem_id]["test_cases"]
    if not problem_test_cases:
        return {
            "status": "skipped",
            "error": "No test cases available",
            "test_results": []
        }
    
    test_results = []
    passed_count = 0
    total_execution_time = 0
    
    for i, test_case in enumerate(problem_test_cases):
        result = run_test_case(solution_func, test_case)
        test_results.append(result)
        
        if result.get("passed", False):
            passed_count += 1
            total_execution_time += result.get("execution_time", 0)
    
    success_rate = passed_count / len(problem_test_cases) if problem_test_cases else 0
    avg_execution_time = total_execution_time / passed_count if passed_count > 0 else 0
    
    return {
        "status": "success" if success_rate == 1.0 else "partial",
        "success_rate": success_rate,
        "passed_count": passed_count,
        "total_tests": len(problem_test_cases),
        "avg_execution_time": avg_execution_time,
        "test_results": test_results
    }

def run_benchmark():
    test_cases = load_test_cases()
    results = {}
    
    for problem in PROBLEMS:
        problem_id = problem["id"]
        func_name = problem["name"]
        
        print(f"Evaluating {problem_id} ({func_name})...")
        result = evaluate_solution(problem_id, func_name, test_cases)
        results[problem_id] = result
        
        # Print results
        if result["status"] == "success":
            print(f"Passed {result['passed_count']}/{result['total_tests']} tests")
        elif result["status"] == "partial":
            print(f"Passed {result['passed_count']}/{result['total_tests']} tests")
        else:
            print(f"Failed: {result.get('error', 'Unknown error')}")
        
        print(f"Average execution time: {result.get('avg_execution_time', 0):.6f} seconds\n")
    
    os.makedirs("results", exist_ok=True)
    with open("results/benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    total_problems = len(PROBLEMS)
    success_problems = sum(1 for r in results.values() if r["status"] == "success")
    partial_problems = sum(1 for r in results.values() if r["status"] == "partial")
    failed_problems = total_problems - success_problems - partial_problems
    
    print("\n===== BENCHMARK SUMMARY =====")
    print(f"Total problems: {total_problems}")
    print(f"Fully successful: {success_problems} ({success_problems/total_problems*100:.1f}%)")
    print(f"Partially successful: {partial_problems} ({partial_problems/total_problems*100:.1f}%)")
    print(f"Failed: {failed_problems} ({failed_problems/total_problems*100:.1f}%)")
    
    total_tests = sum(r.get("total_tests", 0) for r in results.values())
    passed_tests = sum(r.get("passed_count", 0) for r in results.values())
    overall_success_rate = passed_tests / total_tests if total_tests > 0 else 0
    
    print(f"Overall test pass rate: {overall_success_rate*100:.1f}%")
    print(f"Detailed results saved to results/benchmark_results.json")

if __name__ == "__main__":
    run_benchmark()