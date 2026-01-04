import pandas as pd

def detect_anomalies(df):
    """
    Detect anomalies in parsed log data
    Returns DataFrame with anomaly scores and flags
    """
    anomalies = []
    
    # 1. Multiple failed login attempts from same IP
    failed_auth = df[df['is_auth_failure'] == True].groupby('ip').size()
    suspicious_ips = failed_auth[failed_auth >= 3].index.tolist()
    
    for ip in suspicious_ips:
        ip_logs = df[df['ip'] == ip]
        anomalies.append({
            'type': 'Repeated Auth Failure',
            'ip': ip,
            'count': len(ip_logs[ip_logs['is_auth_failure']]),
            'severity': 'HIGH',
            'details': f"IP {ip} had {len(ip_logs[ip_logs['is_auth_failure']])} authentication failures"
        })
    
    # 2. High request frequency (potential DDoS)
    high_frequency = df[df['ip_request_count'] > 10].groupby('ip').first()
    
    for ip in high_frequency.index:
        if ip not in suspicious_ips:  # Avoid duplicate
            anomalies.append({
                'type': 'High Request Volume',
                'ip': ip,
                'count': df[df['ip'] == ip]['ip_request_count'].iloc[0],
                'severity': 'MEDIUM',
                'details': f"IP {ip} made {df[df['ip'] == ip]['ip_request_count'].iloc[0]} requests"
            })
    
    # 3. Unauthorized access attempts
    forbidden = df[(df['status'] == 403) & (df['endpoint'].str.contains('admin', case=False))]
    
    for _, row in forbidden.iterrows():
        anomalies.append({
            'type': 'Unauthorized Access Attempt',
            'ip': row['ip'],
            'count': 1,
            'severity': 'HIGH',
            'details': f"IP {row['ip']} tried accessing {row['endpoint']}"
        })
    
    return pd.DataFrame(anomalies)


if __name__ == "__main__":
    # Load parsed logs
    df = pd.read_csv("parsed_logs.csv")
    
    # Detect anomalies
    anomalies_df = detect_anomalies(df)
    
    if not anomalies_df.empty:
        anomalies_df.to_csv("anomalies.csv", index=False)
        print(f"✓ Detected {len(anomalies_df)} anomalies")
        print("\nAnomalies detected:")
        print(anomalies_df.to_string(index=False))
    else:
        print("No anomalies detected")