# Strategy Specification Document

This document outlines the evolving strategy for Diversified Program. It includes detailed specifications, adjustments, and rationale for each iteration. Updates are made on a monthly basis to reflect new insights and changes in market conditions.

## Table of Contents
- [Current Strategy](#current-strategy)
- [Past Iterations](#past-iterations)
- [Future Plans](#future-plans)
- [Changelog](#changelog)

---

## 1. First version (July 2024 - Jan2025):

Strategy: **system_f1**

**Objective:**  

Period: July 2024 to Jan 2025
First trading date: 1 July 2024 

**Key Components:**
1. **Asset Allocation:**  
   - FX 33%
   - Equity 33%
   - Metals 33%

2. **Instrument Allocation:**  
   - S50: 33%  
   - USD: 33%  
   - GF10: 33%  

2. **Risk Management:**  
   - Risk target: 14%  
   - Initial capital: 631,123.25

3. **Execution Rules:**  
   - Trading period: RTH only.
---
```markdown
forecast_weights:
     S50:
        ewmac16_64: 0.33
        ewmac32_128: 0.33
        ewmac64_256: 0.33
     USD:
        ewmac32_128: 0.50
        ewmac64_256: 0.50
     GF10:
        ewmac8_32: 0.25
        ewmac16_64: 0.25
        ewmac32_128: 0.25
        ewmac64_256: 0.25
```

## 2. Second version (Feb 2025):

**Key Changes:**

1. Change forecast weights

```markdown
forecast_weights:
     S50:
        ewmac2_8: 0
        ewmac8_32: 0.25 # Form this
        ewmac16_64: 0.25
        ewmac32_128: 0.25
        ewmac64_256: 0.25
     USD:
        ewmac2_8: 0
        ewmac8_32: 0
        ewmac16_64: 0.33 # From this
        ewmac32_128: 0.33
        ewmac64_256: 0.33
     GF10:
        ewmac2_8: 0
        ewmac8_32: 0.25 # From this
        ewmac16_64: 0.25
        ewmac32_128: 0.25
        ewmac64_256: 0.25
```