# Generating training data, to train a gpt-workflow LLM README

## Approach

Create a small test dataset in CSV format, via Chat-GPT3.5 Turbo (why: power + speed + low effort)

- Summary,Description, DOT

Ideally, about 20 million rows?
Initially less - say 10,000 rows.

## Example Output

```
./test.sh
```

```
[[[TEST Generate training data for 10 workflows]]]
---
>> Create training data with 10 workflows
workflow-name,summary,description,request,DOT
EmployeeOnboarding,Manage the onboarding process for new employees,This workflow manages the onboarding process for new employees, including tasks such as paperwork completion, equipment setup, and orientation.,Create a workflow to manage the onboarding process for new employees,"digraph EmployeeOnboarding {
  node [shape=box];
  Start -> PaperworkCompletion;
  PaperworkCompletion -> EquipmentSetup;
  EquipmentSetup -> Orientation;
  Orientation -> End;
}"
ExpenseApproval,Streamline the expense approval process,This workflow streamlines the process of approving employee expenses, ensuring timely and accurate reimbursement.,Design a workflow to streamline the expense approval process,"digraph ExpenseApproval {
  node [shape=box];
  Start -> SubmitExpenseReport;
  SubmitExpenseReport -> ReviewExpense;
  ReviewExpense -> ApproveExpense;
  ApproveExpense -> ReimburseExpense;
  ReimburseExpense -> End;
}"
```

## Reference

[gpt-workflow via Chat-GPT](../../README.md)
