# Loan-Portfolio-Pricing-Model-Set

ABOUT
The Loan Portfolio Pricing Model Set is (will be) as suite of pricing models for a variety of loan types. Each model will evaluate a raw loan tape and output the portfolio's weighted average price (over)under par and its associated dollar price. Each model will consider the intricacies of the loan types' legal, financial, and economic traits in order to produce the most accurate projections.

**DISCLAIMER: None of the outputs produced by these models should be used as financial advice. Please be advised that past results are not indicative of future performance***

CURRENT SUITE 

no-effect-amortizing PRICING MODEL

The No-Effect Pricing model determines the price of an amortizing installment loan based on:
    a. An estimated Conditional Prepayment Rate (CPR) Curve
    b. An estimated Annual Charge Off (ACO) Curve
    c. A target yield (IRR)

Current Static Characteristics/Assumptions
1) 30/360 Accrual Basis
2) Payment Scheduling: No Effect (Prepayments do not result in a change in the scheduled payment)
3) CPR/ACO Curves

UPDATES

0.0.1: ALPHA 1
    Added the no-effect-amortizing Pricing Model
    Notes:
    Currently working on how to optimize loading times
    0.0.1.1
        Decreased run time by 50% by optimizing the increment used in the IRR to target yield goal seek. Need to optimize IRR goal seek next