import numpy as np
import pandas as pd

def pv_curve(
        E, #sending voltage
        X, #line reactance
        pf, #pf
        n_points = 500, #P samples
        lagging = True, # true= inductive, false= capacitive
        P_step = 0.001,
        tol=1e-10

):
    phi= np.arccos(pf)
    q_sign= 1 if lagging else -1
    P= 0.0
    results= []

    for n in range(n_points):
        Q= q_sign *P*np.tan(phi) #reactive power at given P
        inner = (E**4)/4 - E**2 *X *Q - (X**2) *(P**2) #inner discriminant
        if inner <=tol : #voltage capability limit
            print(f'Max P = {P:.6f}')
            break

        V2_high = E**2/2 - X*Q + np.sqrt(inner)
        V2_low = E**2/2 - X*Q - np.sqrt(inner)

        V_high= np.sqrt(V2_high) if V2_high>0 else np.nan #only real value
        V_low= np.sqrt(V2_low) if V2_low>0 else np.nan #only real value
        
        results.append([
            P,Q,V_high,V_low
        ])

        P+=P_step
    
    df= pd.DataFrame(results, columns=[
        "P",
        "Q",
        "V_high",
        'V_low'
    ])

    df.to_csv('pv_curve.csv', index=False)
    return df


pv_curve(
    E= 13.5,
    X=100,
    pf=0.95,
    lagging=True,
    P_step=0.002
)



