# Boxplot Analysis - 

## Understanding Boxplots

A boxplot (box-and-whisker plot) is a visual representation of statistical distribution that shows:
- **Median** (middle line in the box)
- **Quartiles** (Q1 and Q3 - edges of the box)
- **Interquartile Range (IQR)** (height of the box)
- **Whiskers** (extend to show data range, typically 1.5×IQR)
- **Outliers** (points beyond the whiskers)

## What the Boxplots Reveal About API Performance

Based on the statistics data, here's what each boxplot component tells us:

### 1. **Distribution Shape & Spread**

#### **Fake News 1 Boxplot** (Average: 160ms, Std Dev: 151ms)
- **Wide box**: Large IQR indicates high variability
- **Long whiskers**: Data spread from 56ms to 849ms
- **Outliers visible**: The 849ms point will appear as an outlier
- **Right-skewed**: Median (105ms) much lower than average (160ms)
  - **Insight**: Most requests are fast, but a few slow ones pull average up
  - **Visual**: Box will be positioned low with long upper whisker

#### **Fake News 2 Boxplot** (Average: 74ms, Std Dev: 17ms)
- **Narrow box**: Small IQR shows consistent performance
- **Short whiskers**: Tight range (56ms - 141ms)
- **Symmetric**: Median (68ms) close to average (74ms)
  - **Insight**: Most reliable and predictable performance
  - **Visual**: Compact box centered around 70ms

#### **Real News 1 Boxplot** (Average: 83ms, Std Dev: 28ms)
- **Moderate box width**: Some variability but acceptable
- **Medium whiskers**: Range from 58ms to 258ms
- **Slight right-skew**: Median (71ms) lower than average (83ms)
  - **Insight**: Generally consistent with occasional slower requests
  - **Visual**: Box around 70-80ms with some upper outliers

#### **Real News 2 Boxplot** (Average: 77ms, Std Dev: 32ms)
- **Similar to Real News 1**: Moderate variability
- **Range**: 54ms to 275ms
- **Slight right-skew**: Median (68ms) lower than average (77ms)
  - **Insight**: Comparable performance to Real News 1
  - **Visual**: Similar shape to Real News 1

### 2. **Key Visual Comparisons**

#### **Height Comparison**
- **Fake News 1**: Tallest boxplot (widest distribution)
- **Fake News 2**: Shortest boxplot (tightest distribution)
- **Real News cases**: Medium height (moderate spread)

**Interpretation**: Lower box height = more consistent performance

#### **Position on Y-Axis**
- **Fake News 1**: Highest position (slowest)
- **Fake News 2**: Lowest position (fastest)
- **Real News cases**: Middle position

**Interpretation**: Lower position = faster response times

#### **Whisker Length**
- **Fake News 1**: Very long upper whisker (outliers at 849ms)
- **Fake News 2**: Short whiskers (tight range)
- **Real News cases**: Medium whiskers

**Interpretation**: Shorter whiskers = more predictable performance

### 3. **Specific Insights from Boxplot Elements**

#### **The Box (IQR)**
Shows where 50% of requests fall:
- **Fake News 1**: Wide box = inconsistent (50% of requests vary widely)
- **Fake News 2**: Narrow box = consistent (50% of requests cluster tightly)
- **Real News cases**: Medium box = moderate consistency

#### **The Median Line**
Shows the "typical" response time:
- **Fake News 1**: 105ms median (but average is 160ms - skewed!)
- **Fake News 2**: 68ms median (close to 74ms average - normal)
- **Real News 1**: 71ms median
- **Real News 2**: 68ms median

**Key Insight**: When median ≠ average, distribution is skewed (outliers present)

#### **Outliers (Points Beyond Whiskers)**
- **Fake News 1**: Will show multiple outliers, especially the 849ms point
- **Fake News 2**: Likely no outliers (tight distribution)
- **Real News cases**: May show a few outliers (258ms, 275ms)

**Action**: Investigate outliers - they indicate performance issues

### 4. **What Boxplots Show That Numbers Don't**

#### **Visual Pattern Recognition**
- **At a glance**: See which test case performs best/worst
- **Distribution shape**: Identify normal vs. skewed distributions
- **Outlier visibility**: Spot problematic requests immediately
- **Comparison ease**: Compare all 4 test cases side-by-side

#### **Percentile Information**
Boxplots show:
- **25th percentile** (bottom of box)
- **50th percentile** (median line)
- **75th percentile** (top of box)
- **Range** (whiskers)

**Example**: For Fake News 2, you can see:
- 25% of requests < ~60ms
- 50% of requests < ~68ms (median)
- 75% of requests < ~80ms
- 95% of requests < ~140ms

### 5. **Practical Insights from the Boxplots**

#### **Performance Reliability**
- **Fake News 2**: Tight boxplot = most reliable
- **Fake News 1**: Wide boxplot = least reliable
- **Recommendation**: Use Fake News 2 as performance benchmark

#### **SLA Definition**
Based on boxplots, you can define:
- **P50 (Median)**: 68-105ms depending on test case
- **P75**: Top of box (varies by test case)
- **P95**: End of upper whisker (varies by test case)
- **P99**: May include outliers

#### **Anomaly Detection**
- **Fake News 1**: Multiple outliers = investigate cold start
- **Other cases**: Few/no outliers = normal operation

### 6. **What the Combined Boxplot Shows**

The combined boxplot (`api_performance_boxplot.png`) reveals:

1. **Relative Performance**: Easy comparison across all test cases
2. **Consistency Ranking**: Visual ranking from most to least consistent
3. **Outlier Patterns**: See which test cases have problematic outliers
4. **Performance Spread**: Understand the range of performance across different inputs

### 7. **What Individual Boxplots Show**

The individual boxplots (`api_performance_boxplot_individual.png`) reveal:

1. **Detailed Distribution**: See exact shape for each test case
2. **Outlier Details**: Identify specific outlier values
3. **Percentile Breakdown**: Understand distribution within each test case
4. **Isolated Analysis**: Focus on one test case without comparison bias

### 8. **Key Takeaways from Boxplot Analysis**

#### **Performance Ranking (Best to Worst)**
1. **Fake News 2**: Fastest, most consistent (ideal performance)
2. **Real News 2**: Fast, moderately consistent
3. **Real News 1**: Fast, moderately consistent
4. **Fake News 1**: Slowest, least consistent (needs investigation)

#### **Reliability Ranking (Most to Least Reliable)**
1. **Fake News 2**: Tightest distribution
2. **Real News 1**: Moderate distribution
3. **Real News 2**: Moderate distribution
4. **Fake News 1**: Widest distribution

#### **Action Items Based on Boxplots**
1. **Investigate Fake News 1**: Why is it so different?
2. **Optimize for consistency**: Aim for all test cases to match Fake News 2
3. **Set monitoring thresholds**: Use boxplot quartiles for alerts
4. **Document performance**: Boxplots provide visual proof of API performance

### 9. **Boxplot vs. Statistics Table**

**Boxplot Advantages**:
- ✅ Visual, easy to understand at a glance
- ✅ Shows distribution shape (skew, outliers)
- ✅ Enables quick comparison
- ✅ Reveals patterns numbers might hide

**Statistics Table Advantages**:
- ✅ Exact numerical values
- ✅ Precise calculations (mean, std dev)
- ✅ Detailed metrics

**Best Practice**: Use both! Boxplots for visualization, tables for precise numbers.

## Conclusion

Boxplots provide a powerful visual summary that reveals:
- **Distribution patterns** (normal vs. skewed)
- **Performance consistency** (tight vs. wide spread)
- **Outlier presence** (problematic requests)
- **Relative performance** (comparison across test cases)
- **Percentile information** (P25, P50, P75, P95)

The boxplots clearly show that **Fake News 2** has ideal performance (fast and consistent), while **Fake News 1** has performance issues (slow and inconsistent) that need investigation.

