import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

# --- Settings ---
machines = ['M1','M2','M3','M4','M5','M6','M7','M8','M9','M10']
temperature_threshold = 90
vibration_threshold = 0.05
update_interval = 3000  # milliseconds (3 seconds)

# --- Initialize DataFrame ---
def generate_sensor_data():
    return pd.DataFrame({
        'machine_id': machines,
        'timestamp': [pd.Timestamp.now()]*len(machines),
        'temperature': np.random.randint(65, 110, size=len(machines)),
        'vibration': np.round(np.random.uniform(0.01, 0.15, size=len(machines)), 2)
    })

df = generate_sensor_data()

# --- Setup plot ---
fig, ax = plt.subplots(figsize=(12, 6))

def update(frame):
    global df
    ax.clear()
    
    # --- Generate new sensor readings for all machines ---
    df['timestamp'] = [pd.Timestamp.now()]*len(machines)
    df['temperature'] = np.random.randint(65, 110, size=len(machines))
    df['vibration'] = np.round(np.random.uniform(0.01, 0.15, size=len(machines)), 2)
    
    # --- Determine alerts ---
    df['temperature_alert'] = df['temperature'] > temperature_threshold
    df['vibration_alert'] = df['vibration'] > vibration_threshold
    df['maintenance_needed'] = df['temperature_alert'] | df['vibration_alert']
    
    # --- Print summary ---
    num_alerts = df['maintenance_needed'].sum()
    num_ok = len(df) - num_alerts
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ✅ Machines OK: {num_ok}, ⚠️ Machines needing maintenance: {num_alerts}")
    
    alerts = df[df['maintenance_needed']]
    if not alerts.empty:
        print(alerts[['machine_id','timestamp','temperature','vibration']])
    
    # --- Plot chart ---
    colors = ['red' if alert else 'green' for alert in df['maintenance_needed']]
    ax.bar(df['machine_id'], df['temperature'], color=colors, alpha=0.6, label='Temperature')
    ax.plot(df['machine_id'], df['vibration']*1000, marker='o', linestyle='--', color='blue', label='Vibration x1000')
    
    ax.axhline(y=temperature_threshold, color='r', linestyle=':', label='Temp Threshold')
    ax.set_title('Live Machine Status: Temperature & Vibration Alerts (10 Machines)')
    ax.set_xlabel('Machine ID')
    ax.set_ylabel('Temperature / Vibration (x1000)')
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=30)

# --- Run animation ---
ani = FuncAnimation(fig, update, interval=update_interval)
plt.tight_layout()
plt.show()
