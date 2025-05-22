#!/bin/python3

# E12 resistor series base values
BASE_E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

def generate_series(base, min_exp=-1, max_exp=6):
    """Generate resistor values from E12 series over given decades."""
    vals = []
    for exp in range(min_exp, max_exp + 1):
        for b in base:
            vals.append(b * (10 ** exp))
    return sorted(vals)

# full E12 series from 0.1Ω to 8.2MΩ
E12_SERIES = generate_series(BASE_E12, min_exp=-1, max_exp=6)

def nearest_series(value, series=E12_SERIES):
    """Return nearest standard resistor value from series."""
    return min(series, key=lambda x: abs(x - value))

V_FB = 0.8       # V, feedback reference
I_FB = 50e-9     # A, feedback bias current
R2_MAX = 160e3   # Ohms, standard upper limit for R2

voltages = [1.1, 2.6, 3.3]

for V_OUT in voltages:
    R_LIMIT = V_OUT / (I_FB * 100)
    # ideal resistor values
    R2_ideal = min(R2_MAX, R_LIMIT)
    R1_ideal = ((V_OUT / V_FB) - 1) * R2_ideal

    # nearest E12 values
    R2_std = nearest_series(R2_ideal)
    R1_std = nearest_series(R1_ideal)
    total_R = R1_ideal + R2_ideal
    total_std = R1_std + R2_std

    # calculate output voltage using standard E12 resistors
    V_out_std = V_FB * (1 + (R1_std / R2_std))

    print(f"--- For V_OUT = {V_OUT:.1f} V ---")
    print(f"  Ideal: R2 = {R2_ideal/1e3:.2f} kΩ, R1 = {R1_ideal/1e3:.2f} kΩ, Total = {total_R/1e3:.2f} kΩ")
    print(f"  E12 Std: R2 = {R2_std/1e3:.2f} kΩ, R1 = {R1_std/1e3:.2f} kΩ, Total = {total_std/1e3:.2f} kΩ")
    print(f"  V_out with E12 std = {V_out_std:.2f} V")
    print(f"  Maximum allowed (sum of ideal): {R_LIMIT/1e3:.2f} kΩ")
    if total_R > R_LIMIT:
        print("  Warning: Total resistance exceeds limit! Adjust R2.")