import csv
import random
import datetime
import sys

# ==========================================
# CONFIGURATION
# ==========================================

SOURCE_IPS = [
    "192.168.1.10",
    "192.168.1.11",
    "192.168.1.12",
    "192.168.1.13",
    "192.168.1.14",
    "192.168.1.15",
    "192.168.1.16",
    "192.168.1.17",
]

DESTINATION_IPS = [
    "10.0.0.5",
    "10.0.0.10",
    "10.0.0.15",
    "10.0.0.20",
    "10.0.0.25",
]

USERS = [
    "admin",
    "john",
    "alice",
    "svc_backup",
    "svc_sql",
    "guest",
]

HOSTS = [
    "WS01",
    "WS02",
    "WS03",
    "WS04",
    "APP01",
    "FILE01",
    "DB01",
    "DC01",
]

PROTOCOLS = ["TCP", "UDP"]

APPLICATIONS = [
    "HTTPS",
    "HTTP",
    "DNS",
    "SMB",
    "RDP",
    "SSH",
]

# ==========================================
# FIELD DEFINITIONS
# ==========================================

qradar_fields = [
    "EventID","EventName","EventCategory","Severity","Credibility","Relevance","Magnitude",
    "SourceIP","SourcePort","SourceMAC","SourceHostname","SourceUser","SourceGeo",
    "DestinationIP","DestinationPort","DestinationMAC","DestinationHostname","DestinationUser","DestinationGeo",
    "Protocol","BytesSent","BytesReceived","PacketsSent","PacketsReceived","Direction",
    "LogSourceID","LogSourceType","DeviceVendorProduct",
    "StartTime","EndTime","LogSourceTime","StorageTime",
    "EventDescription","RuleName","OffenseID","EventCount","CustomProperties"
]

stealthwatch_fields = [
    "EventID","EventCategory","Message","FullMessage","AlarmID","AlarmStatus","AlarmSeverity",
    "SourceIP","SourcePort","SourceHG","SourceUser","SourceHostname",
    "DestinationIP","DestinationPort","TargetHG","TargetUser","TargetHostname",
    "Protocol","FlowCollectorName","FlowCollectorIP","ExporterName","ExporterIP","ExporterInfo",
    "StartTime","EndTime","Domain"
]

arista_fields = [
    "EventID","EventType","Severity","DetectionRule","ConfidenceScore",
    "SourceIP","SourcePort","SourceMAC","SourceHostname","SourceUser","SourceGeo",
    "DestinationIP","DestinationPort","DestinationMAC","DestinationHostname","DestinationUser","DestinationGeo",
    "Protocol","BytesSent","BytesReceived","PacketsSent","PacketsReceived","FlowDirection","FlowDuration","Application",
    "ThreatCategory","ThreatName","MITRETechnique","DetectionEngine",
    "StartTime","EndTime","DetectionTime","CollectorID"
]

# ==========================================
# EVENT PROFILES
# ==========================================

QRADAR_EVENTS = [
    ("Failed Login Attempt", "Authentication", 389),
    ("Successful Login", "Authentication", 389),
    ("VPN Login", "Authentication", 443),
    ("DNS Query", "DNS", 53),
    ("DNS Response", "DNS", 53),
    ("Port Scan Detected", "Reconnaissance", 22),
    ("Service Discovery", "Reconnaissance", 135),
    ("HTTP Request", "Network", 80),
    ("HTTPS Session", "Network", 443),
    ("SMB Connection", "Network", 445),
    ("RDP Connection", "Network", 3389),
    ("Malware Detected", "Malware", 445),
    ("Suspicious Process", "Malware", 8080),
    ("Data Exfiltration", "Exfiltration", 443),
    ("Beaconing Activity", "Command & Control", 443),
]

STEALTHWATCH_EVENTS = [
    ("Anomaly", "Suspicious Traffic"),
    ("Beaconing", "Periodic Communication"),
    ("Reconnaissance", "Port Scan Activity"),
    ("Data Transfer", "Large Data Transfer"),
    ("Malware", "Known Malicious Connection"),
    ("DNS", "Suspicious DNS Query"),
    ("Authentication", "Multiple Login Failures"),
    ("Authentication", "Successful Login"),
    ("Network", "SMB Traffic"),
    ("Network", "RDP Session"),
]

ARISTA_EVENTS = [
    ("Suspicious Beaconing", "Command & Control", "Cobalt Strike", "T1071.001"),
    ("Data Exfiltration", "Exfiltration", "Large Transfer", "T1048"),
    ("Port Scan", "Reconnaissance", "Network Scan", "T1046"),
    ("Malware Activity", "Malware", "Emotet", "T1105"),
    ("Lateral Movement", "Lateral Movement", "Remote Service", "T1021"),
    ("DNS Tunneling", "Command & Control", "DNS Tunnel", "T1071.004"),
    ("Credential Access", "Credential Access", "Password Spray", "T1110"),
    ("SMB Discovery", "Reconnaissance", "SMB Enumeration", "T1135"),
]

# ==========================================
# HELPERS
# ==========================================

base_time = datetime.datetime.now()

def random_timestamp():
    offset = random.randint(0, 86400)
    return (base_time + datetime.timedelta(seconds=offset)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

def random_ip_pair():
    return (
        random.choice(SOURCE_IPS),
        random.choice(DESTINATION_IPS)
    )

# ==========================================
# QRADAR
# ==========================================

def generate_qradar_log():

    src_ip, dst_ip = random_ip_pair()
    event_name, category, dst_port = random.choice(QRADAR_EVENTS)

    return {
        "EventID": random.randint(1000,9999),
        "EventName": event_name,
        "EventCategory": category,
        "Severity": random.randint(1,10),
        "Credibility": random.randint(1,10),
        "Relevance": random.randint(1,10),
        "Magnitude": random.randint(50,500),

        "SourceIP": src_ip,
        "SourcePort": random.randint(1024,65535),

        "SourceMAC": "00:1A:2B:3C:4D:5E",
        "SourceHostname": random.choice(HOSTS),
        "SourceUser": random.choice(USERS),
        "SourceGeo": random.choice(["India","USA","UK"]),

        "DestinationIP": dst_ip,
        "DestinationPort": dst_port,

        "DestinationMAC": "00:5E:6F:7A:8B:9C",
        "DestinationHostname": random.choice(HOSTS),
        "DestinationUser": random.choice(USERS),
        "DestinationGeo": random.choice(["Internal","Germany","Singapore"]),

        "Protocol": random.choice(PROTOCOLS),

        "BytesSent": random.randint(100,10000),
        "BytesReceived": random.randint(100,10000),

        "PacketsSent": random.randint(1,100),
        "PacketsReceived": random.randint(1,100),

        "Direction": random.choice(["Inbound","Outbound","Lateral"]),

        "LogSourceID": 102,
        "LogSourceType": "Security Event Log",
        "DeviceVendorProduct": "Security Platform",

        "StartTime": random_timestamp(),
        "EndTime": random_timestamp(),
        "LogSourceTime": random_timestamp(),
        "StorageTime": random_timestamp(),

        "EventDescription": event_name,
        "RuleName": category + " Rule",

        "OffenseID": random.randint(10000,99999),
        "EventCount": random.randint(1,5),

        "CustomProperties": "Process=svchost.exe"
    }

# ==========================================
# STEALTHWATCH
# ==========================================

def generate_stealthwatch_log():

    src_ip, dst_ip = random_ip_pair()
    category, message = random.choice(STEALTHWATCH_EVENTS)

    return {
        "EventID": random.randint(1000,9999),
        "EventCategory": category,
        "Message": message,
        "FullMessage": message + " detected",

        "AlarmID": f"AL-{random.randint(1000,9999)}",
        "AlarmStatus": random.choice(["ACTIVE","CLOSED"]),
        "AlarmSeverity": random.choice(["Minor","Major","Critical"]),

        "SourceIP": src_ip,
        "SourcePort": random.randint(1024,65535),

        "SourceHG": "Inside",
        "SourceUser": random.choice(USERS),
        "SourceHostname": random.choice(HOSTS),

        "DestinationIP": dst_ip,
        "DestinationPort": random.choice([53,80,443,445,3389]),

        "TargetHG": "Outside",
        "TargetUser": random.choice(USERS),
        "TargetHostname": random.choice(HOSTS),

        "Protocol": random.choice(PROTOCOLS),

        "FlowCollectorName": "Collector1",
        "FlowCollectorIP": random.choice(DESTINATION_IPS),

        "ExporterName": "Router1",
        "ExporterIP": random.choice(DESTINATION_IPS),

        "ExporterInfo": "Flow Exporter",

        "StartTime": random_timestamp(),
        "EndTime": random_timestamp(),

        "Domain": random.choice([
            "Corporate",
            "Finance",
            "HR",
            "Engineering"
        ])
    }

# ==========================================
# ARISTA
# ==========================================

def generate_arista_log():

    src_ip, dst_ip = random_ip_pair()

    event_type, threat_category, threat_name, mitre = random.choice(
        ARISTA_EVENTS
    )

    return {
        "EventID": f"NDR-{random.randint(1000,9999)}",
        "EventType": event_type,

        "Severity": random.choice([
            "Low",
            "Medium",
            "High",
            "Critical"
        ]),

        "DetectionRule": event_type + " Detection",

        "ConfidenceScore": random.randint(50,100),

        "SourceIP": src_ip,
        "SourcePort": random.randint(1024,65535),

        "SourceMAC": "00:1B:44:11:3A:B7",
        "SourceHostname": random.choice(HOSTS),
        "SourceUser": random.choice(USERS),
        "SourceGeo": random.choice(["India","USA","UK"]),

        "DestinationIP": dst_ip,
        "DestinationPort": random.choice([53,80,443,445,3389]),

        "DestinationMAC": "00:5E:6F:7A:8B:9C",
        "DestinationHostname": random.choice(HOSTS),
        "DestinationUser": random.choice(USERS),
        "DestinationGeo": random.choice(["Singapore","Germany","USA"]),

        "Protocol": random.choice(PROTOCOLS),

        "BytesSent": random.randint(1000,50000),
        "BytesReceived": random.randint(100,20000),

        "PacketsSent": random.randint(10,500),
        "PacketsReceived": random.randint(5,300),

        "FlowDirection": random.choice([
            "Inbound",
            "Outbound",
            "Lateral"
        ]),

        "FlowDuration": str(
            datetime.timedelta(
                seconds=random.randint(10,600)
            )
        ),

        "Application": random.choice(APPLICATIONS),

        "ThreatCategory": threat_category,
        "ThreatName": threat_name,
        "MITRETechnique": mitre,

        "DetectionEngine": "Analytics Engine",

        "StartTime": random_timestamp(),
        "EndTime": random_timestamp(),
        "DetectionTime": random_timestamp(),

        "CollectorID": "NDR-Sensor-01"
    }

# ==========================================
# CSV WRITER
# ==========================================

def write_csv(filename, fields, generator, count):

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)

        writer.writeheader()

        for _ in range(count):
            writer.writerow(generator())

# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    count = 1000

    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except:
            pass

    write_csv(
        "qradar_logs.csv",
        qradar_fields,
        generate_qradar_log,
        count
    )

    write_csv(
        "stealthwatch_logs.csv",
        stealthwatch_fields,
        generate_stealthwatch_log,
        count
    )

    write_csv(
        "arista_logs.csv",
        arista_fields,
        generate_arista_log,
        count
    )

    print(f"Generated {count} logs per platform.")
    print("Created:")
    print(" - qradar_logs.csv")
    print(" - stealthwatch_logs.csv")
    print(" - arista_logs.csv")