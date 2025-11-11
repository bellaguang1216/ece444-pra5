# CSV Data Analysis

## Overview
The CSV files contain performance data from 400 API calls (100 per test case) to the Fake News Detector API deployed on AWS Elastic Beanstalk.

## Key Insights from `api_performance_statistics.csv`

### 1. **Performance Comparison Across Test Cases**

| Test Case | Average (ms) | Median (ms) | Min (ms) | Max (ms) | Std Dev (ms) |
|-----------|--------------|-------------|----------|----------|--------------|
| **Fake News 1** | 160.04 | 104.72 | 56.06 | 849.20 | 151.64 |
| **Fake News 2** | 74.45 | 67.69 | 56.20 | 141.35 | 17.37 |
| **Real News 1** | 83.41 | 71.15 | 57.65 | 258.18 | 28.47 |
| **Real News 2** | 77.39 | 68.50 | 54.13 | 274.78 | 31.93 |

### 2. **Key Findings**

#### **Performance Anomaly: Fake News 1**
- **Slowest average**: 160.04ms (more than 2x slower than others)
- **Highest variability**: Std Dev of 151.64ms (very inconsistent)
- **Outlier**: Max latency of 849.20ms (likely a cold start or network issue)
- **Median vs Average gap**: 55.32ms difference suggests right-skewed distribution (outliers pulling average up)

**Possible causes:**
- First test case may have triggered model loading (cold start)
- Network latency spike
- AWS instance warming up

#### **Most Consistent Performance: Fake News 2**
- **Lowest average**: 74.45ms
- **Lowest variability**: Std Dev of 17.37ms (most consistent)
- **Tight range**: 56.20ms - 141.35ms (85ms span)
- **Median close to average**: Only 6.76ms difference (normal distribution)

#### **Real News Cases**
- **Similar performance**: Both around 77-83ms average
- **Moderate variability**: Std Dev 28-32ms (acceptable)
- **Slightly higher than Fake News 2**: Possibly due to text length or processing complexity

### 3. **Statistical Insights**

#### **Coefficient of Variation (CV = Std Dev / Mean)**
- **Fake News 1**: 94.7% (very high variability - unreliable)
- **Fake News 2**: 23.3% (low variability - reliable)
- **Real News 1**: 34.1% (moderate variability)
- **Real News 2**: 41.2% (moderate variability)

#### **Performance Stability Ranking**
1. Fake News 2 (most stable)
2. Real News 1
3. Real News 2
4. Fake News 1 (least stable)

### 4. **What `api_performance_results.csv` Tells Us**

#### **Temporal Patterns**
- **Timestamps**: Show exact timing of each request
- **Request sequence**: Can identify patterns (e.g., first request slower due to cold start)
- **Status codes**: All 200 (all requests successful - good!)

#### **Detailed Analysis Capabilities**
- **Outlier detection**: Can identify specific requests with unusually high latency
- **Trend analysis**: See if performance degrades over time
- **Request correlation**: Compare performance between sequential requests
- **Network patterns**: Identify if latency spikes correlate with specific times

### 5. **Practical Implications**

#### **For Production Deployment:**
1. **Cold Start Issue**: First request (Fake News 1) shows cold start penalty
   - **Solution**: Implement warm-up requests or keep-alive pings

2. **Performance Consistency**: Fake News 2 shows ideal performance
   - **Target**: Aim for <20ms std dev for production

3. **Average Response Time**: 74-83ms is acceptable for ML inference
   - **Benchmark**: Industry standard is <200ms for real-time APIs

4. **Outlier Management**: 849ms max latency is concerning
   - **Action**: Investigate network/instance issues
   - **Monitoring**: Set up alerts for latencies >500ms

#### **For Testing:**
1. **Test Order Matters**: First test case may be slower
   - **Recommendation**: Run warm-up requests before timing tests

2. **Sample Size**: 100 requests per case is sufficient for statistical significance
   - **Confidence**: Can make reliable conclusions about performance

3. **Variability Matters**: High std dev indicates unreliable service
   - **Metric**: Track coefficient of variation, not just average

### 6. **Questions the Data Answers**

✅ **Is the API fast enough?** Yes - average 74-83ms is good
✅ **Is the API consistent?** Mostly - except Fake News 1 (likely cold start)
✅ **Are there performance issues?** One outlier (849ms) needs investigation
✅ **Is the service reliable?** Yes - 100% success rate (all 200 status codes)
✅ **Does text length/complexity affect latency?** Possibly - needs more analysis

### 7. **What to Investigate Further**

1. **Why Fake News 1 is so slow**: 
   - Check if it's the first request (cold start)
   - Analyze text length/complexity
   - Check AWS CloudWatch logs for that time period

2. **The 849ms outlier**:
   - Network latency spike?
   - Instance resource contention?
   - Model loading delay?

3. **Performance optimization**:
   - Can we reduce Fake News 1 latency to match others?
   - Implement connection pooling?
   - Add caching for repeated requests?

## Conclusion

The CSV files provide comprehensive performance data that reveals:
- **Overall good performance** (74-83ms average for most cases)
- **Cold start penalty** (first request much slower)
- **High reliability** (100% success rate)
- **One performance anomaly** (Fake News 1) that needs investigation

This data is valuable for:
- **Performance monitoring** and alerting
- **Capacity planning** and scaling decisions
- **Optimization** efforts
- **SLA definition** (e.g., "95% of requests <150ms")

