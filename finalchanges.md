# MARS System Setup & Configuration Reference

This guide provides a comprehensive, unified checklist of every parameter, file path, setting, and code location that needs to be configured or modified when deploying the Malware Analysis & Reverse-engineering System (MARS).

It details the setup process for three environments:
1. **The Physical Hypervisor / Parent Host** (managing the virtualization layer and nested virtualization support).
2. **VM A — Controller** (where the web server, sniffer, and orchestration scripts run).
3. **VM B — Sandbox** (where the malware is executed and kernel events are tracked).

---

## 1. Physical Host / Hypervisor Configuration

The physical machine hosts both virtual machines and controls the virtual networking and nested CPU virtualization properties.

### 1.1 CPU Settings (Nested Virtualization)
To run virtualization-based security (VBS) or nested hypervisors (e.g., if VM A/B are inside another VM), you must enable nested CPU options.
* **Path/UI Location:** Open VMware Workstation → Right-click **VM A (Controller) / VM B (Sandbox)** → **Settings** → **Hardware Tab** → **Processors**.
* **Configurations to Change:**
  - Check **"Virtualize Intel VT-x/EPT or AMD-V/RVI"**.
  - Check **"Virtualize CPU performance counters"**.
  - Check **"Virtualize IOMMU (IO memory management unit)"** (if using Hyper-V features).

### 1.2 Virtual Network Editor Configuration
Configures the host-only network `VMnet1` to allow Scapy sniffing without leakage.
* **Path/UI Location:** Windows Start Menu → search **Virtual Network Editor** (Run as Administrator) or via VMware Workstation → **Edit → Virtual Network Editor**.
* **Configurations to Change:**
  1. Click **Change Settings** (requires Admin rights).
  2. Select **VMnet1** (Host-only).
  3. Ensure **"Connect a host virtual adapter to this network"** is **Checked**.
  4. Ensure **"Use local DHCP service to distribute IP addresses to VMs"** is **Unchecked** (for static IP reliability).
  5. Set **Subnet IP** to: `192.168.10.0`
  6. Set **Subnet Mask** to: `255.255.255.0`
  7. Click **Apply** and **OK**.

---

## 2. VM A — Controller Configuration (Host VM)

This is the machine running the main MARS FastAPI server, network sniffer, and orchestration engine.

### 2.1 Virtual Machine Hardware Properties
* **Path/UI Location:** VMware Workstation → Right-click **VM A** → **Settings**.
* **Configurations to Change:**
  - **Network Adapter 1 (Bridged/NAT):** Connected for general management/updates (optional).
  - **Network Adapter 2 (Custom):** Map to **VMnet1 (Host-only)**.
  - **IP Address (inside Guest OS):** Set a static IP on the VMnet1 interface:
    - IP: `192.168.10.1`
    - Subnet Mask: `255.255.255.0`

### 2.2 System Level Software (VM A)
* **Python 3.10 – 3.12:**
  - Download official installer and check **"Add Python to PATH"**.
* **Npcap (Raw Packet Sniffing Driver):**
  - Download installer from [npcap.com](https://npcap.com/).
  - **CRITICAL:** Check **"Install Npcap in WinPcap API-compatible mode"** during installation. Without this, Scapy will fail to bind to the interface.

---

## 3. VM B — Sandbox Configuration (Guest VM)

This is the isolated guest VM where malware is detonated. It must remain in a clean snapshot state.

### 3.1 Virtual Machine Hardware Properties
* **Path/UI Location:** VMware Workstation → Right-click **VM B (Sandbox)** → **Settings**.
* **Configurations to Change:**
  - **Processors:** Allocate `2` cores.
  - **Memory:** Allocate `4096 MB` (4 GB).
  - **Network Adapter 1 (NAT):** Uncheck **"Connect at power on"** (ensures air-gapped run during analysis).
  - **Network Adapter 2 (Custom):** Map to **VMnet1 (Host-only)**.
  - **Serial Port (Pipe Connection):**
    - Click **Add** → **Serial Port**.
    - Select **"Use named pipe"**.
    - Pipe Name: `\\.\pipe\sandbox_serial`
    - Option 1 (This end is): **Server**
    - Option 2 (The other end is): **A virtual machine**
    - Check **"Yield CPU on poll"**.

### 3.2 Network Adapter Settings (Inside VM B)
* **Path/UI Location:** Windows Settings → Network & Internet → Status → Change Adapter Options → Right-click the VMnet1 Ethernet adapter → **Properties** → Double-click **Internet Protocol Version 4 (TCP/IPv4)**.
* **Configurations to Change:**
  - Select **"Use the following IP address"**:
    - IP Address: `192.168.10.20`
    - Subnet Mask: `255.255.255.0`
    - Default Gateway: `192.168.10.1` (VM A's interface IP)
    - Preferred DNS Server: `8.8.8.8` (or empty if offline)

### 3.3 User Credentials Creation
* **Path/UI Location:** Run Administrator PowerShell or Command Prompt.
* **Configurations to Change:**
  ```powershell
  # Creates a local Administrator account matching config.yaml defaults
  net user Administrator Password123 /add
  net localgroup administrators Administrator /add
  ```

### 3.4 Python Installation & Directory Paths
* **Path/UI Location:** Download Python 3.9 (64-bit) installer.
* **Configurations to Change:**
  - Choose **"Customize installation"** → Set install path to exactly:
    ```
    C:\Python39\
    ```
  - Check **"Add Python to PATH"** and **"Install for all users"**.

### 3.5 System Tools Setup & EULA Regedit
* **Path/UI Location:** Inside VM B, create `C:\Tools\` directory.
* **Configurations to Change:**
  1. Move `procmon.exe` to `C:\Tools\procmon.exe`.
  2. Run `C:\Tools\procmon.exe` manually once as administrator.
  3. Click **Agree / Accept** on the EULA license pop-up. (This generates the registry key: `HKCU\Software\Sysinternals\Process Monitor\EulaAccepted = 1` which prevents the UI from blocking the background automated script).
  4. Close ProcMon.
  5. Create `C:\Analysis` folder:
     ```cmd
     mkdir C:\Analysis
     ```

### 3.6 Disabling Security Systems
* **Path/UI Location:** Administrator PowerShell window.
* **Configurations to Change:**
  ```powershell
  # Permanently disables Windows Defender engine and real-time protections
  Set-MpPreference -DisableRealtimeMonitoring $true
  Set-MpPreference -DisableBehaviorMonitoring $true
  Set-MpPreference -DisableBlockAtFirstSeen $true
  Set-MpPreference -DisableIOAVProtection $true
  ```

---

## 4. Configuration Mapping (File Modifications)

This section maps the exact files, paths, and line coordinates that must be modified to adapt to your specific paths or setup.

| File Path | Description of Change / Target Field | Key / Content to Modify |
| :--- | :--- | :--- |
| [config.yaml](file:///C:/Users/HP/OneDrive/Desktop/CyberSec/malware-final/config/config.yaml) (Line 89) | VMware VIX orchestration command-line path. | `vmrun_path: "C:\\Program Files\\VMware\\VMware Workstation\\vmrun.exe"` *(Verify path matches your installation)* |
| [config.yaml](file:///C:/Users/HP/OneDrive/Desktop/CyberSec/malware-final/config/config.yaml) (Line 90) | Physical path to VM B's VMX configuration file. | `vmx_path: "C:\\Users\\Acer\\Documents\\Virtual Machines\\Windows10_Sandbox\\Windows10_Sandbox.vmx"` *(Update to match your .vmx location)* |
| [config.yaml](file:///C:/Users/HP/OneDrive/Desktop/CyberSec/malware-final/config/config.yaml) (Line 93) | Clean baseline snapshot name in VMware. | `snapshot_name: "Clean_State"` *(Must match snapshot name created in VM B)* |
| [config.yaml](file:///C:/Users/HP/OneDrive/Desktop/CyberSec/malware-final/config/config.yaml) (Lines 94-95) | User credentials for VM B guest OS. | `guest_user: "Administrator"`<br>`guest_pass: "Password123"` |
| [config.yaml](file:///C:/Users/HP/OneDrive/Desktop/CyberSec/malware-final/config/config.yaml) (Line 99) | Shared telemetry Serial Named Pipe. | `serial_pipe: "\\\\.\\pipe\\sandbox_serial"` |
| [config.yaml](file:///C:/Users/HP/OneDrive/Desktop/CyberSec/malware-final/config/config.yaml) (Line 102) | Host network adapter display name for VMnet1. | `network_interface: "VMware Virtual Ethernet Adapter for VMnet1"` *(Run `python -c "import scapy.all; print(scapy.all.get_if_list())"` to verify matches exactly)* |
| [index.html](file:///C:/Users/HP/OneDrive/Desktop/CyberSec/malware-final/web/templates/index.html) (Line 8) | Air-Gap CDN Mitigation: ChartJS reference. | Change from external CDN to local file:<br>`<script src="/static/js/chart.js"></script>` |
| [index.html](file:///C:/Users/HP/OneDrive/Desktop/CyberSec/malware-final/web/templates/index.html) (Line 9) | Air-Gap CDN Mitigation: Google Fonts stylesheet import. | Comment out or delete the `@import` containing `fonts.googleapis.com`. |
| [report.html](file:///C:/Users/HP/OneDrive/Desktop/CyberSec/malware-final/web/templates/report.html) (Line 8) | Air-Gap CDN Mitigation: ChartJS reference. | Change from external CDN to local file:<br>`<script src="/static/js/chart.js"></script>` |
| [report.html](file:///C:/Users/HP/OneDrive/Desktop/CyberSec/malware-final/web/templates/report.html) (Line 10) | Air-Gap CDN Mitigation: Google Fonts stylesheet import. | Comment out or delete the `@import` containing `fonts.googleapis.com`. |
| [tailwind.css](file:///C:/Users/HP/OneDrive/Desktop/CyberSec/malware-final/web/static/css/tailwind.css) (Line 6) | Air-Gap CDN Mitigation: CSS import for Google Fonts. | Comment out or delete external `@import url("https://fonts.googleapis.com...")`. |
| [tailwind.css](file:///C:/Users/HP/OneDrive/Desktop/CyberSec/malware-final/web/static/css/tailwind.css) (Lines 1-5) | Local `@font-face` definitions (Air-Gap). | Define local font routes `/static/fonts/Inter.ttf`, `/static/fonts/Outfit.ttf`, and `/static/fonts/JetBrainsMono.ttf` (Refer to Section 5). |

---

## 5. Air-Gapped / Offline Asset Mappings

For air-gapped hosts, frontend library paths are routed locally as follows:

### 5.1 Local Files Path Mapping
To host the Web UI dependencies locally on VM A (Controller), place files in these precise directories:
* **Chart.js v4.x Library File:**
  - Save to: `C:\Users\HP\OneDrive\Desktop\CyberSec\malware-final\web\static\js\chart.js`
* **Google Fonts (Inter, Outfit, JetBrains Mono .ttf files):**
  - Save to: `C:\Users\HP\OneDrive\Desktop\CyberSec\malware-final\web\static\fonts\Inter.ttf`
  - Save to: `C:\Users\HP\OneDrive\Desktop\CyberSec\malware-final\web\static\fonts\Outfit.ttf`
  - Save to: `C:\Users\HP\OneDrive\Desktop\CyberSec\malware-final\web\static\fonts\JetBrainsMono.ttf`

### 5.2 Offline Pip Installation Wheels Directories
When installing dependencies in an offline machine, copy these wheels folders to the machine and reference them with pip:
* **VM A (Controller Host Wheels):**
  - Directory: `C:\MARS_Offline_Setup\host_wheels\`
  - Command: `pip install --no-index --find-links=C:\MARS_Offline_Setup\host_wheels -r requirements.txt`
* **VM B (Sandbox Guest Wheels):**
  - Directory: `C:\Users\Administrator\Desktop\guest_wheels\`
  - Command: `C:\Python39\python.exe -m pip install --no-index --find-links=C:\Users\Administrator\Desktop\guest_wheels pyserial psutil pywin32 wmi watchdog`
