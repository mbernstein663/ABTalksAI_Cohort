# Query Structure:

## What are my plan pricing options? 

```
SELECT plan_id, monthly_premium FROM plans ORDER BY monthly_premium DESC
```

Plan: P101, Monthly Payment: 500
Plan: P102, Monthly Payment: 300
Plan: P103, Monthly Payment: 150

## How many claims are pending for member M1001?

```
SELECT COUNT(*) AS pending_claims
FROM claims
WHERE member_id = 'M1001' AND status = 'Pending'
```

Pending claims for member M1001: 1

## Which plans have a monthly premium under $400?

```
SELECT plan_id, plan_name, monthly_premium
FROM plans
WHERE monthly_premium < 400
ORDER BY monthly_premium ASC
```

Plans with monthly premium under $400:
Plan: P103 | Name: Bronze HMO | Premium: $150
Plan: P102 | Name: Silver HMO | Premium: $300

## JOIN between claims and plans

```
SELECT
    c.claim_id,
    c.member_id,
    p.plan_name,
    c.procedure,
    c.status,
    c.claim_amount
FROM claims AS c
JOIN plans AS p
    ON c.plan_id = p.plan_id
ORDER BY c.claim_id
```

Claims joined to plan details:
('C1001', 'M1001', 'Gold PPO', 'X-ray', 'Pending', 250)
('C1002', 'M1001', 'Gold PPO', 'Surgery', 'Approved', 1200)
('C1003', 'M1002', 'Silver HMO', 'X-ray', 'Denied', 150)
('C1004', 'M1002', 'Silver HMO', 'Surgery', 'Approved', 900)
('C1005', 'M1003', 'Bronze HMO', 'X-ray', 'Pending', 50)

## Top-N query: most claimed procedures

```
SELECT procedure, COUNT(*) AS claim_count
FROM claims
GROUP BY procedure
ORDER BY claim_count DESC
LIMIT 3
```

Top claimed procedures:
Procedure: X-ray | Claims: 3
Procedure: Surgery | Claims: 2
Created coverage.db with tables: plans, claims