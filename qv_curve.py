import numpy as np
import pandas as pd

def qv_curve(
        E,   #sending voltage
        X,   #line reactance
        Q,  # load Q
        P,  #load P
        V_min= 0.5,
        V_max= 500,
        n_points= 500,
        tol=1e-12

):
    V_values = np.linspace(V_min, V_max, n_points)
    results = []

    for V in V_values:
        if V <=tol:
            continue
        sin_phi = -P*X / (E*V) 
        if abs(sin_phi) > 1: #feasible region
            continue
        cosphi= np.sqrt(1-sin_phi**2)

        Qc= Q + (V**2)/X - (E*V/X) *cosphi
        results.append([V/E, Qc])
    
    df= pd.DataFrame(results, columns=[
        "V",
        "Qc"
        
    ])

    df.to_csv('qv_cuve.csv', index=False)
    return df

qv_curve(
    E=13.5,
    X=100,
    P=0.1,
    Q=0,
    V_min=0.4 *13.5,
    V_max=1.1 *13.5,
    n_points=800
)