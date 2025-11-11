# API Testing Guide

This guide explains how to test the deployed Fake News Detector API on AWS Elastic Beanstalk.

## Prerequisites

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Get the AWS Elastic Beanstalk URL (e.g., `http://app-name.elasticbeanstalk.com`)

## Running the Tests

### Step 1: Set the API URL

You have two options:

**Option A: Environment Variable (Recommended)**
```bash
export API_URL="http://eb-url.elasticbeanstalk.com"
python test_api.py
```

**Option B: Edit the script directly**
Edit `test_api.py` and change line 19:
```python
API_BASE_URL = os.getenv("API_URL", "http://actual-url.elasticbeanstalk.com")
```

### Step 2: Run the Tests

```bash
python test_api.py
```

The script will:
1. Run functional/unit tests (4 test cases)
2. Perform 100 API calls per test case (400 total requests)
3. Record all timestamps and latencies in CSV files
4. Generate boxplots
5. Calculate statistics

### Step 3: Review Results

The script generates:
- `api_performance_results.csv` - All 400 requests with timestamps
- `api_performance_statistics.csv` - Summary statistics per test case
- `api_performance_boxplot.png` - Combined boxplot
- `api_performance_boxplot_individual.png` - Individual boxplots

## Test Cases

The script includes 4 test cases:
1. **Fake News 1**: Example of clearly fake news
2. **Fake News 2**: Another fake news example
3. **Real News 1**: Example of legitimate news
4. **Real News 2**: Another real news example

You can modify these in `test_api.py` if needed.

## Adding Boxplots to README

After running the tests, add the boxplot images to the README.md:

```markdown
## Performance Results

![API Performance Boxplot](api_performance_boxplot.png)
```

