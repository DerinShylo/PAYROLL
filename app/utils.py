# utils.py
import math
import calendar
from datetime import datetime
from typing import List, Dict, Any

def calculate_salary_components(
    gross_salary: float,
    lop_days: float,
    deductions: Dict[str, float],
    reimbursements: List[float],
    month: int,
    year: int
) -> Dict[str, Any]:

    # Defensive safety checks
    gross_salary = float(gross_salary or 0)
    lop_days = float(lop_days or 0)
    deductions = deductions or {}
    reimbursements = reimbursements or []

    # ----------------------------
    # Step 1: Days in the month
    # ----------------------------
    days_in_month = calendar.monthrange(year, month)[1]

    # ----------------------------
    # Step 2: LOP Amount (exact)
    # ----------------------------
    lop_amount = (lop_days / days_in_month) * gross_salary

    # ----------------------------
    # Step 3: Adjusted Gross (gross minus actual LOP)
    # ----------------------------
    adjusted_gross = gross_salary - lop_amount

    # ----------------------------
    # Step 4: EPF & ESI Calculations (use rounded-up LOP days for these)
    # ----------------------------
    rounded_lop = math.ceil(lop_days)
    lop_amount_for_epf_esi = (rounded_lop / days_in_month) * gross_salary
    adjusted_gross_for_epf_esi = gross_salary - lop_amount_for_epf_esi

    epf = math.ceil(adjusted_gross_for_epf_esi * 0.70 * 0.12)
    esi = math.ceil(adjusted_gross_for_epf_esi * 0.0075)

    # ----------------------------
    # Step 5: Manual Deductions (sum of provided deduction fields)
    # ----------------------------
    total_manual_deductions = sum(float(v or 0) for v in deductions.values())

    # ----------------------------
    # Step 6: Reimbursements
    # ----------------------------
    total_reimbursements = sum(float(r or 0) for r in reimbursements)

    # ----------------------------
    # Step 7: Total Deductions (do NOT include lop_amount here — it's already removed)
    # ----------------------------
    total_deductions = epf + esi + total_manual_deductions

    # ----------------------------
    # Step 8: Net Salary
    # net = adjusted_gross - total_deductions + reimbursements
    # ----------------------------
    net_salary = adjusted_gross - total_deductions + total_reimbursements

    # ----------------------------
    # Round & Format Results
    # ----------------------------
    result = {
        "gross_salary": round(gross_salary, 2),
        "days_in_month": days_in_month,
        "lop_days": lop_days,
        "lop_amount": round(lop_amount, 2),
        "rounded_lop": rounded_lop,
        "lop_amount_for_epf_esi": round(lop_amount_for_epf_esi, 2),
        "adjusted_gross": round(adjusted_gross, 2),
        "adjusted_gross_for_epf_esi": round(adjusted_gross_for_epf_esi, 2),
        "epf": round(epf, 2),
        "esi": round(esi, 2),
        "total_manual_deductions": round(total_manual_deductions, 2),
        "total_reimbursements": round(total_reimbursements, 2),
        "total_deductions": round(total_deductions, 2),
        "net_salary": round(net_salary, 2),
    }

    return result
