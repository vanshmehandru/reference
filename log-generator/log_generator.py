import csv
import random
import datetime
import sys

# Define log attributes for each platform
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

# Utility functions
def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def random_time():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

# Generators
def generate_qradar_log():
    return {
        "EventID": random.randint(1000,9999),
        "EventName": "Failed Login Attempt",
        "EventCategory": "Authentication",
        "Severity": random.choice([1,3,5]),
        "Credibility": random.randint(1,10),
        "Relevance": random.randint(1,10),
        "Magnitude": random.randint(50,500),
        "SourceIP": random_ip(),
        "SourcePort": random.randint(1024,65535),
        "SourceMAC": "00:1A:2B:3C:4D:5E",
        "SourceHostname": "HR-Laptop-01",
        "SourceUser": "jdoe",
        "SourceGeo": "India",
        "DestinationIP": random_ip(),
        "DestinationPort": 389,
        "DestinationMAC": "00:5E:6F:7A:8B:9C",
        "DestinationHostname": "AD-Server-01",
        "DestinationUser": "Administrator",
        "DestinationGeo": "Internal",
        "Protocol": "TCP",
        "BytesSent": random.randint(100,10000),
        "BytesReceived": random.randint(100,10000),
        "PacketsSent": random.randint(1,50),
        "PacketsReceived": random.randint(1,50),
        "Direction": "Inbound",
        "LogSourceID": 102,
        "LogSourceType": "Windows Security Event Log",
        "DeviceVendorProduct": "Microsoft Windows Server",
        "StartTime": random_time(),
        "EndTime": random_time(),
        "LogSourceTime": random_time(),
        "StorageTime": random_time(),
        "EventDescription": "User failed to authenticate",
        "RuleName": "Multiple Failed Logins",
        "OffenseID": random.randint(10000,99999),
        "EventCount": 1,
        "CustomProperties": "Process=lsass.exe"
    }

def generate_stealthwatch_log():
    return {
        "EventID": random.randint(1000,9999),
        "EventCategory": "Anomaly",
        "Message": "Suspicious traffic detected",
        "FullMessage": "Source host communicating with external target",
        "AlarmID": "AL-"+str(random.randint(1000,9999)),
        "AlarmStatus": "ACTIVE",
        "AlarmSeverity": random.choice(["Minor","Major","Critical"]),
        "SourceIP": random_ip(),
        "SourcePort": random.randint(1024,65535),
        "SourceHG": "Inside",
        "SourceUser": "admin",
        "SourceHostname": "Finance-PC",
        "DestinationIP": random_ip(),
        "DestinationPort": 80,
        "TargetHG": "Outside",
        "TargetUser": "websvc",
        "TargetHostname": "www.example.com",
        "Protocol": "TCP",
        "FlowCollectorName": "Collector1",
        "FlowCollectorIP": random_ip(),
        "ExporterName": "Router1",
        "ExporterIP": random_ip(),
        "ExporterInfo": "Cisco Router",
        "StartTime": random_time(),
        "EndTime": random_time(),
        "Domain": "Corporate"
    }

def generate_arista_log():
    return {
        "EventID": "NDR-"+str(random.randint(1000,9999)),
        "EventType": "Suspicious Beaconing",
        "Severity": "High",
        "DetectionRule": "Beaconing Behavior",
        "ConfidenceScore": random.randint(70,100),
        "SourceIP": random_ip(),
        "SourcePort": random.randint(1024,65535),
        "SourceMAC": "00:1B:44:11:3A:B7",
        "SourceHostname": "Finance-PC-07",
        "SourceUser": "vsharma",
        "SourceGeo": "India",
        "DestinationIP": random_ip(),
        "DestinationPort": 443,
        "DestinationMAC": "00:5E:6F:7A:8B:9C",
        "DestinationHostname": "malicious-c2.example.com",
        "DestinationUser": "N/A",
        "DestinationGeo": "Singapore",
        "Protocol": "TCP",
        "BytesSent": random.randint(1000,20000),
        "BytesReceived": random.randint(100,5000),
        "PacketsSent": random.randint(10,100),
        "PacketsReceived": random.randint(5,50),
        "FlowDirection": "Outbound",
        "FlowDuration": "00:01:12",
        "Application": "HTTPS",
        "ThreatCategory": "Command & Control",
        "ThreatName": "Cobalt Strike Beacon",
        "MITRETechnique": "T1071.001",
        "DetectionEngine": "Flow Analytics + ML",
        "StartTime": random_time(),
        "EndTime": random_time(),
        "DetectionTime": random_time(),
        "CollectorID": "NDR-Sensor-01"
    }

# Write logs to CSV
def write_csv(filename, fields, generator, count):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for _ in range(count):
            writer.writerow(generator())

if __name__ == "__main__":
    # Default to 1000 logs if no argument provided
    num_logs = 1000
    if len(sys.argv) > 1:
        try:
            num_logs = int(sys.argv[1])
        except ValueError:
            print("Invalid input, using default 1000 logs.")

    write_csv("qradar_logs.csv", qradar_fields, generate_qradar_log, num_logs)
    write_csv("stealthwatch_logs.csv", stealthwatch_fields, generate_stealthwatch_log, num_logs)
    write_csv("arista_logs.csv", arista_fields, generate_arista_log, num_logs)

    print(f"CSV logs generated ({num_logs} per platform) for QRadar, Stealthwatch, and Arista NDR!")
