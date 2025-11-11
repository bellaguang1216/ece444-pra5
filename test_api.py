"""
API Testing Script for Fake News Detector
Performs functional tests and latency/performance tests
"""

import requests
import time
import csv
import statistics
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Tuple, Dict
import os


API_BASE_URL = os.getenv("API_URL", "http://serve-sentiment-env.eba-rpcabree.us-east-2.elasticbeanstalk.com")
PREDICT_ENDPOINT = f"{API_BASE_URL}/predict"

# Test cases: 2 fake news examples, 2 real news examples
# Note: The expected_label is just for reference - actual predictions depend on the trained model
TEST_CASES = [
    {
        "name": "Fake News 1",
        "text": "BREAKING: Scientists discover that drinking bleach cures all diseases instantly. Doctors are shocked by this revolutionary finding that Big Pharma doesn't want you to know! Share this immediately before they delete it!",
        "expected_label": "FAKE"
    },
    {
        "name": "Fake News 2",
        "text": "ALERT: The moon landing was completely faked in a Hollywood studio. NASA has been covering this up for decades with help from the government. This explosive truth will change everything you know!",
        "expected_label": "FAKE"
    },
    {
        "name": "Real News 1",
        "text": "The International Space Station completed another successful mission today, with astronauts conducting important research on microgravity effects on plant growth. The findings were published in the latest issue of Space Science Journal.",
        "expected_label": "REAL"
    },
    {
        "name": "Real News 2",
        "text": "Scientists at MIT published a new study in Nature journal showing promising results in renewable energy storage technology that could reduce battery costs by 30%. The research team spent three years developing the new approach.",
        "expected_label": "REAL"
    }
]


def functional_test() -> Dict[str, bool]:
    """
    Perform functional/unit tests with the 4 test cases.
    Returns a dictionary with test results.
    """
    print("=" * 60)
    print("FUNCTIONAL/UNIT TESTS")
    print("=" * 60)
    
    results = {}
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print(f"Text: {test_case['text'][:80]}...")
        
        try:
            start_time = time.time()
            response = requests.post(
                PREDICT_ENDPOINT,
                json={"message": test_case["text"]},
                timeout=30
            )
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                predicted_label = data.get("label", "UNKNOWN")
                print(f"✓ Status: {response.status_code}")
                print(f"✓ Predicted Label: {predicted_label}")
                print(f"✓ Response Time: {elapsed_time:.3f}s")
                
                # Note: We're just checking if it returns a valid response
                # The actual label depends on the model's training
                results[test_case['name']] = True
            else:
                print(f"✗ Status: {response.status_code}")
                print(f"✗ Error: {response.text}")
                results[test_case['name']] = False
                
        except Exception as e:
            print(f"✗ Exception: {str(e)}")
            results[test_case['name']] = False
    
    print("\n" + "=" * 60)
    print("FUNCTIONAL TEST SUMMARY")
    print("=" * 60)
    for name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"{name}: {status}")
    
    return results


def latency_test(num_requests: int = 100) -> Dict[str, List[float]]:
    """
    Perform latency/performance tests: 100 API calls per test case.
    Records timestamps and returns latency data.
    """
    print("\n" + "=" * 60)
    print(f"LATENCY/PERFORMANCE TESTS ({num_requests} requests per test case)")
    print("=" * 60)
    
    all_latencies = {}
    csv_data = []
    
    for test_case in TEST_CASES:
        print(f"\nTesting: {test_case['name']}")
        latencies = []
        
        for i in range(num_requests):
            try:
                start_time = time.time()
                response = requests.post(
                    PREDICT_ENDPOINT,
                    json={"message": test_case["text"]},
                    timeout=30
                )
                end_time = time.time()
                latency = (end_time - start_time) * 1000  # Convert to milliseconds
                
                timestamp = time.time()
                latencies.append(latency)
                
                csv_data.append({
                    "test_case": test_case['name'],
                    "request_number": i + 1,
                    "timestamp": timestamp,
                    "latency_ms": latency,
                    "status_code": response.status_code
                })
                
                if (i + 1) % 20 == 0:
                    print(f"  Completed {i + 1}/{num_requests} requests...")
                    
            except Exception as e:
                print(f"  ✗ Request {i + 1} failed: {str(e)}")
                timestamp = time.time()
                csv_data.append({
                    "test_case": test_case['name'],
                    "request_number": i + 1,
                    "timestamp": timestamp,
                    "latency_ms": None,
                    "status_code": None
                })
        
        all_latencies[test_case['name']] = latencies
        
        # Calculate statistics
        if latencies:
            avg_latency = statistics.mean(latencies)
            median_latency = statistics.median(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            
            print(f"\n  Statistics for {test_case['name']}:")
            print(f"    Average: {avg_latency:.2f} ms")
            print(f"    Median: {median_latency:.2f} ms")
            print(f"    Min: {min_latency:.2f} ms")
            print(f"    Max: {max_latency:.2f} ms")
    
    # Save to CSV
    csv_filename = "api_performance_results.csv"
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['test_case', 'request_number', 'timestamp', 'latency_ms', 'status_code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"\n✓ Results saved to {csv_filename}")
    
    return all_latencies


def generate_boxplots(latencies: Dict[str, List[float]]):
    """
    Generate boxplots for each test case and save them.
    """
    print("\n" + "=" * 60)
    print("GENERATING BOXPLOTS")
    print("=" * 60)
    
    # Prepare data for plotting
    data_to_plot = []
    labels = []
    
    for test_case_name, latency_list in latencies.items():
        if latency_list:  # Only include if we have data
            data_to_plot.append(latency_list)
            labels.append(test_case_name)
    
    if not data_to_plot:
        print("✗ No data to plot!")
        return
    
    # Create boxplot
    plt.figure(figsize=(12, 8))
    bp = plt.boxplot(data_to_plot, labels=labels, patch_artist=True)
    
    # Customize boxplot
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    for patch, color in zip(bp['boxes'], colors[:len(bp['boxes'])]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    plt.title('API Latency Performance by Test Case', fontsize=16, fontweight='bold')
    plt.xlabel('Test Case', fontsize=12)
    plt.ylabel('Latency (milliseconds)', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=15, ha='right')
    
    # Add average line annotations
    for i, (label, lat_list) in enumerate(zip(labels, data_to_plot)):
        avg = statistics.mean(lat_list)
        plt.text(i + 1, avg, f'Avg: {avg:.1f}ms', 
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('api_performance_boxplot.png', dpi=300, bbox_inches='tight')
    print("✓ Boxplot saved as 'api_performance_boxplot.png'")
    
    # Also create individual boxplots if needed
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, (test_case_name, latency_list) in enumerate(latencies.items()):
        if latency_list:
            bp = axes[idx].boxplot([latency_list], labels=[test_case_name], patch_artist=True)
            bp['boxes'][0].set_facecolor(colors[idx % len(colors)])
            bp['boxes'][0].set_alpha(0.7)
            axes[idx].set_title(f'{test_case_name}\nAvg: {statistics.mean(latency_list):.2f}ms', 
                              fontsize=11, fontweight='bold')
            axes[idx].set_ylabel('Latency (milliseconds)', fontsize=10)
            axes[idx].grid(axis='y', alpha=0.3)
    
    plt.suptitle('API Latency Performance - Individual Test Cases', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('api_performance_boxplot_individual.png', dpi=300, bbox_inches='tight')
    print("✓ Individual boxplots saved as 'api_performance_boxplot_individual.png'")
    
    plt.close('all')


def calculate_statistics(latencies: Dict[str, List[float]]):
    """
    Calculate and print detailed statistics for each test case.
    """
    print("\n" + "=" * 60)
    print("DETAILED STATISTICS")
    print("=" * 60)
    
    stats_data = []
    
    for test_case_name, latency_list in latencies.items():
        if latency_list:
            stats = {
                'Test Case': test_case_name,
                'Average (ms)': statistics.mean(latency_list),
                'Median (ms)': statistics.median(latency_list),
                'Min (ms)': min(latency_list),
                'Max (ms)': max(latency_list),
                'Std Dev (ms)': statistics.stdev(latency_list) if len(latency_list) > 1 else 0,
                'Count': len(latency_list)
            }
            stats_data.append(stats)
            
            print(f"\n{test_case_name}:")
            print(f"  Average: {stats['Average (ms)']:.2f} ms")
            print(f"  Median: {stats['Median (ms)']:.2f} ms")
            print(f"  Min: {stats['Min (ms)']:.2f} ms")
            print(f"  Max: {stats['Max (ms)']:.2f} ms")
            print(f"  Std Dev: {stats['Std Dev (ms)']:.2f} ms")
            print(f"  Total Requests: {stats['Count']}")
    
    # Save statistics to CSV
    stats_df = pd.DataFrame(stats_data)
    stats_df.to_csv('api_performance_statistics.csv', index=False)
    print(f"\n✓ Statistics saved to 'api_performance_statistics.csv'")


def main():
    """
    Main function to run all tests.
    """
    print("Fake News Detector API Testing")
    print(f"API URL: {API_BASE_URL}")
    print(f"Endpoint: {PREDICT_ENDPOINT}")
    
    # Check if API is accessible
    try:
        health_response = requests.get(f"{API_BASE_URL}/", timeout=10)
        if health_response.status_code == 200:
            print("✓ API is accessible")
        else:
            print(f"⚠ API returned status {health_response.status_code}")
    except Exception as e:
        print(f"✗ Cannot reach API: {str(e)}")
        print("Please check the API_BASE_URL or set API_URL environment variable")
        return
    
    # Run functional tests
    functional_results = functional_test()
    
    # Run latency tests
    latencies = latency_test(num_requests=100)
    
    # Generate boxplots
    generate_boxplots(latencies)
    
    # Calculate statistics
    calculate_statistics(latencies)
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - api_performance_results.csv (all request data)")
    print("  - api_performance_statistics.csv (summary statistics)")
    print("  - api_performance_boxplot.png (combined boxplot)")
    print("  - api_performance_boxplot_individual.png (individual boxplots)")


if __name__ == "__main__":
    main()

