#!/bin/python3
V_FB = 0.8       # V, feedback reference
I_FB = 50e-9     # A, feedback bias current
R2_MAX = 160e3   # Ohms, standard upper limit for R2

voltages = [1.1, 2.6, 3.3]

for V_OUT in voltages:
    R_LIMIT = V_OUT / (I_FB * 100)
    R2 = min(R2_MAX, R_LIMIT)
    R1 = ((V_OUT / V_FB) - 1) * R2
    total_R = R1 + R2

    print(f"--- For V_OUT = {V_OUT:.1f} V ---")
    print(f"  R2 = {R2/1e3:.0f} kΩ")
    print(f"  R1 = {R1/1e3:.0f} kΩ")
    print(f"  R1 + R2 = {total_R/1e3:.0f} kΩ")
    print(f"  Maximum allowed (R1 + R2): {R_LIMIT/1e3:.0f} kΩ")
    if total_R > R_LIMIT:
        print("  Warning: Total resistance exceeds limit! Adjust R2.")