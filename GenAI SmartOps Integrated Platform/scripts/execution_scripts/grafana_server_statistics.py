import sys
import re
import random

# Regex patterns to extract server names correctly
server_name_patterns = [
    r'server\s+name\s+([\w\d]+)',  
    r'server\s+name\s*["\']([^"\']+)["\']',  
    r'grafana\s*[:\-]\s*["\']?([\w\d]+)["\']?',  
    r'server\s*[:\-]?\s*["\']?([\w\d]+)["\']?',  
    r'hostname\s*[:\-]?\s*["\']?([\w\d]+)["\']?',  
    r'ci\s*[:\-]?\s*["\']?([\w\d]+)["\']?'  
]

def extract_server_name(query):
    """Extracts the server name from the query using regex patterns."""
    for pattern in server_name_patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

def fetch_dummy_grafana_data(query):
    server_name = extract_server_name(query)
    if not server_name:
        return None

    # Dummy data for testing
    return {

        "server": server_name,
        "memory_usage": random.randint(30, 90),
        "disk_usage": random.randint(30, 90),
        "swap_usage":random.randint(30, 90),
        "Network_Traffic_Inbound": random.randint(110, 150),
        "Network_Traffic_Outbound": random.randint(75, 95),
        "Packet_Loss": random.randint(0, 2)
    }

def format_data(data):
    return (
        f"Please see below details of {data['server']}\n\n"
        f"1. General System Health & Resource Utilization\n"
        f"   Memory Usage: {data['memory_usage']}%\n"
        f"   Swap Usage: {data['swap_usage']}%\n"
        f"   Disk Usage: {data['disk_usage']}%\n\n"
        f"2. Network Performance\n"
        f"   Network Traffic Inbound: {data['Network_Traffic_Inbound']}MB/s\n"
        f"   Network Traffic Outbound: {data['Network_Traffic_Outbound']}MB/s\n"
        f"   Packet Loss: {data['Packet_Loss']}%\n"
    )

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
        data = fetch_dummy_grafana_data(query)
        if data:
            print(format_data(data))
    else:
        print("No query provided. Please pass a valid query.")
