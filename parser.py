import re
import pandas as pd
from datetime import datetime

log_pattern = re.compile(
    r'(?P<ip>\S+) - - \[(?P<date>.*?)\] "(?P<method>\S+) (?P<endpoint>\S+) \S+" (?P<status>\d+) -'
)

rows = []

print("Starting to parse access.log...")
with open("access.log") as f:
    for i, line in enumerate(f, 1):
        match = log_pattern.search(line)
        if match:
            rows.append(match.groupdict())
            print(f"✓ Line {i} matched: {match.groupdict()}")
        else:
            print(f"✗ Line {i} NO MATCH --> {line.strip()}")

print(f"\nTotal matches: {len(rows)}")
df = pd.DataFrame(rows)
print(f"DataFrame columns: {df.columns.tolist()}")
print(f"DataFrame shape: {df.shape}")

if not df.empty and 'status' in df.columns:
    df['status'] = df['status'].astype(int)
    
    # Parse timestamp for time-based analysis
    df['timestamp'] = pd.to_datetime(df['date'], format='%d/%b/%Y:%H:%M:%S %z')
    df['hour'] = df['timestamp'].dt.hour
    df['minute'] = df['timestamp'].dt.minute
    
    # Add anomaly flags for common patterns
    df['is_error'] = df['status'] >= 400
    df['is_auth_failure'] = (df['status'] == 401) | (df['status'] == 403)
    
    # Calculate request frequency per IP
    ip_counts = df.groupby('ip').size()
    df['ip_request_count'] = df['ip'].map(ip_counts)
    
    df.to_csv("parsed_logs.csv", index=False)
    print("\n✓ Parsed logs saved to parsed_logs.csv")
    print(f"✓ Total entries: {len(df)}")
    print(f"✓ Unique IPs: {df['ip'].nunique()}")
    print(f"✓ Error responses: {df['is_error'].sum()}")
    print("\nSample data:")
    print(df.head())
elif df.empty:
    print("\n⚠️ ERROR: No logs matched the pattern!")
    print("Please check that access.log exists and has the correct format.")
else:
    print(f"\n⚠️ ERROR: Missing expected columns. Found: {df.columns.tolist()}")
    print("The regex pattern may need adjustment.")