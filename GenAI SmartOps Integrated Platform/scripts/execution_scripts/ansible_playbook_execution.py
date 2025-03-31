import sys
import time
import random
import re

# Remove sys.stdout modification (causes errors in Jupyter)
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') 

server_issue_mapping = {
    "down": [
        ("Server disk is full", "Calling Ansible Playbook for Freeing up disk space..."),
        ("Critical system service crashed", "Calling Ansible Playbook for Restarting services..."),
        ("Hardware failure detected", "Calling Ansible Playbook for Performing hardware diagnostics..."),
        ("Power failure or PSU issue", "Calling Ansible Playbook for Switching to backup power..."),
        ("Corrupted OS files detected", "Calling Ansible Playbook for Restoring system files..."),
        ("Network interface failure", "Calling Ansible Playbook for Resetting network configuration..."),
        ("Unexpected kernel panic", "Calling Ansible Playbook for Rebooting into recovery mode..."),
        ("Filesystem corruption detected", "Calling Ansible Playbook for Running file system repair..."),
        ("Overheating detected", "Calling Ansible Playbook for Reducing CPU load and checking cooling..."),
        ("Excessive failed SSH login attempts", "Calling Ansible Playbook for Blocking suspicious IPs..."),
    ],
    "unresponsive": [
        ("Memory leak detected", "Calling Ansible Playbook for Restarting affected services..."),
        ("Application process stuck", "Calling Ansible Playbook for Killing stuck processes..."),
        ("Deadlock detected in database", "Calling Ansible Playbook for Restarting database instance..."),
        ("High CPU utilization causing process hang", "Calling Ansible Playbook for Redistributing load..."),
        ("I/O bottleneck detected", "Calling Ansible Playbook for Optimizing disk performance..."),
        ("Excessive swap usage", "Calling Ansible Playbook for Clearing swap memory..."),
        ("Kernel thread stuck", "Calling Ansible Playbook for Restarting kernel modules..."),
        ("Unresponsive remote service dependency", "Calling Ansible Playbook for Checking dependent services..."),
        ("Overloaded message queue", "Calling Ansible Playbook for Flushing message queue..."),
        ("CPU throttling due to thermal limits", "Calling Ansible Playbook for Adjusting cooling strategies..."),
    ],
    "slow": [
        ("High RAM usage", "Calling Ansible Playbook for Clearing cache..."),
        ("CPU overload detected", "Calling Ansible Playbook for Redistributing CPU load..."),
        ("Disk I/O latency high", "Calling Ansible Playbook for Optimizing storage operations..."),
        ("Network congestion detected", "Calling Ansible Playbook for Resetting network adapter..."),
        ("Excessive database queries", "Calling Ansible Playbook for Optimizing database indexes..."),
        ("Large number of background processes", "Calling Ansible Playbook for Killing unnecessary processes..."),
        ("Inefficient caching strategy", "Calling Ansible Playbook for Adjusting cache settings..."),
        ("Virtual memory thrashing", "Calling Ansible Playbook for Increasing memory allocation..."),
        ("High log file writes affecting performance", "Calling Ansible Playbook for Rotating and archiving logs..."),
        ("Excessive thread contention", "Calling Ansible Playbook for Adjusting thread scheduling..."),
    ],
    "general": [
        ("Configuration mismatch detected", "Calling Ansible Playbook for Syncing configurations..."),
        ("Network latency issue", "Calling Ansible Playbook for Resetting network adapter..."),
        ("Unexpected application error", "Calling Ansible Playbook for Restarting application services..."),
        ("High file system inode usage detected", "Calling Ansible Playbook for Cleaning up unused files..."),
        ("Security patch missing", "Calling Ansible Playbook for Applying latest security patches..."),
        ("Log files consuming excessive disk space", "Calling Ansible Playbook for Rotating and archiving logs..."),
        ("Database connection timeout", "Calling Ansible Playbook for Restarting database services..."),
        ("CPU throttling detected due to power limits", "Calling Ansible Playbook for Adjusting power management settings..."),
        ("Multiple failed SSH login attempts detected", "Calling Ansible Playbook for Blocking suspicious IPs..."),
        ("Application dependency version mismatch", "Calling Ansible Playbook for Updating dependencies..."),
    ],
}


# Regex patterns to extract server names correctly
server_name_patterns = [
    r'server\s+name\s+([\w\d]+)',  
    r'server\s+name\s*["\']([^"\']+)["\']',  
    r'grafana\s*[:\-]\s*["\']?([\w\d]+)["\']?',  
    r'server\s*[:\-]?\s*["\']?([\w\d]+)["\']?',  
    r'hostname\s*[:\-]?\s*["\']?([\w\d]+)["\']?',  
    r'ci\s*[:\-]?\s*["\']?([\w\d]+)["\']?'  
    ]

# Keywords for Ansible execution
issue_keywords = {
    "down": ["down", "not responding", "crashed", "unavailable"],
    "unresponsive": ["unresponsive", "frozen", "hanging"],
    "slow": ["slow", "lagging", "delayed", "taking too long"]
}

def extract_issue_type(query):
    """Extracts the issue type (down, unresponsive, slow) from the query."""
    for issue, keywords in issue_keywords.items():
        for keyword in keywords:
            if keyword in query.lower():
                #print(f" Issue Type Detected: {issue}", flush=True)
                return issue
    #print(" No issue type detected in query.", flush=True)
    return None

def extract_server_name(query):
    """Extracts the server name from the query using regex patterns."""
    for pattern in server_name_patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            extracted_name = match.group(1)
            #print(f" Server Name Matched: {extracted_name}", flush=True)
            return extracted_name
    #print(" No server name found in query.", flush=True)
    return None

# def execute_ansible_playbook(query):
#     server_name = extract_server_name(query)
#     if not server_name:
#         print("\n **Error:** Server name not found in query.")
#         return

#     issue_type = extract_issue_type(query)
#     if not issue_type:
#         print("\n **Error:** Could not determine issue type from query.")
#         return

#     issue, fix_action = random.choice(server_issue_mapping.get(issue_type, [("Unknown issue detected", "Calling Ansible Playbook...")]))

#     print(f"\n **Issue detected on {server_name}:** {issue}")
#     time.sleep(2)
#     print(f"\n **Action:** {fix_action}")
#     #time.sleep(3)
#     #print(f"\n **{server_name} issue resolved successfully!**")

def execute_ansible_playbook(query):
    server_name = extract_server_name(query)
    if not server_name:
        print("\n **Error:** Server name not found in query.")
        return

    issue_type = extract_issue_type(query)

    # If no specific issue is found, pick a random issue from the 'general' category
    if not issue_type:
        issue_type = "general"

    issue, fix_action = random.choice(server_issue_mapping[issue_type])

    print(f"\n Issue detected on {server_name}: {issue}")
    time.sleep(2)
    print(f"\n Action: {fix_action}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
        #print(f"\nProcessing Query: {query}")
        execute_ansible_playbook(query)
    else:
        print(" No query provided. Please pass a valid query.")