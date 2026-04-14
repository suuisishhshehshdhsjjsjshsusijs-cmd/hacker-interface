import streamlit as st
import requests
import time
import json
import random
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import os

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:5000").rstrip("/")

# إعدادات الصفحة
st.set_page_config(page_title="Hacker Terminal v4.0", layout="wide", initial_sidebar_state="collapsed")

# تصميم CSS لنمط الـ Terminal الواقعي المحسّن
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500&display=swap');
    
    .stApp {
        background-color: #0a0a0a;
        color: #00ff00;
        font-family: 'Fira Code', monospace;
    }
    .terminal-container {
        background-color: #000000;
        border: 1px solid #333;
        border-radius: 5px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.1);
        margin-bottom: 20px;
    }
    .terminal-header {
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
        margin-bottom: 15px;
        display: flex;
        justify-content: space-between;
        color: #555;
        font-size: 0.8em;
    }
    .terminal-output {
        height: 450px;
        overflow-y: auto;
        font-size: 0.9em;
        line-height: 1.4;
        border: 1px solid #111;
        padding: 10px;
        background: #050505;
    }
    .log-entry { margin-bottom: 5px; }
    .log-time { color: #555; }
    .log-info { color: #00ff00; }
    .log-warn { color: #ffff00; }
    .log-error { color: #ff0000; font-weight: bold; }
    .log-cmd { color: #00ffff; }
    .log-success { color: #00ff00; font-weight: bold; }
    .log-network { color: #00aaff; }
    
    .stButton>button {
        background-color: #111 !important;
        color: #00ff00 !important;
        border: 1px solid #00ff00 !important;
        border-radius: 0 !important;
        font-family: 'Fira Code', monospace !important;
        transition: all 0.3s !important;
        width: 100% !important;
        text-align: left !important;
        padding: 10px !important;
        margin-bottom: 5px !important;
    }
    .stButton>button:hover {
        background-color: #00ff00 !important;
        color: #000 !important;
        box-shadow: 0 0 10px #00ff00 !important;
    }
    
    .network-status {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .network-connected {
        background-color: rgba(0, 255, 0, 0.1);
        border: 1px solid #00ff00;
        color: #00ff00;
    }
    .network-disconnected {
        background-color: rgba(255, 0, 0, 0.1);
        border: 1px solid #ff0000;
        color: #ff0000;
    }
</style>
""", unsafe_allow_html=True)

# تهيئة حالة الجلسة
if 'terminal_logs' not in st.session_state:
    st.session_state.terminal_logs = [
        {"time": datetime.now().strftime("%H:%M:%S"), "type": "info", "msg": "Hacker Terminal v4.0 Initialized..."},
        {"time": datetime.now().strftime("%H:%M:%S"), "type": "info", "msg": "System: Kali Linux v2024.1 (Rolling)"},
        {"time": datetime.now().strftime("%H:%M:%S"), "type": "info", "msg": "Network Interface: eth0 (192.168.1.x)"},
        {"time": datetime.now().strftime("%H:%M:%S"), "type": "info", "msg": "Ready for network penetration. Target: Local Network."},
    ]

if 'device_ip' not in st.session_state:
    st.session_state.device_ip = f"192.168.1.{random.randint(100, 254)}"

if 'is_connected' not in st.session_state:
    st.session_state.is_connected = False

def add_log(msg, type="info"):
    """إضافة سجل جديد إلى الطرفية"""
    st.session_state.terminal_logs.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "type": type,
        "msg": msg
    })
    if len(st.session_state.terminal_logs) > 150:
        st.session_state.terminal_logs.pop(0)

def connect_to_network():
    """سيناريو الاتصال بالشبكة"""
    add_log("root@kali:~# ifconfig eth0 up", "cmd")
    add_log("Configuring network interface...", "info")
    time.sleep(0.5)
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/device/connect",
            json={
                "ip": st.session_state.device_ip,
                "name": "Kali Linux Attacker",
                "mac": f"00:11:22:33:44:{random.randint(10, 99)}"
            },
            timeout=5
        )
        
        if response.status_code == 200:
            res_data = response.json()
            add_log(f"[+] Network connection established!", "success")
            add_log(f"[+] IP Address: {st.session_state.device_ip}", "info")
            add_log(f"[+] Gateway: 192.168.1.1", "info")
            add_log(f"[+] DNS: 8.8.8.8", "info")
            add_log(f"[+] Status: Connected to local network", "network")
            st.session_state.is_connected = True
            st.rerun()
        else:
            add_log(f"[-] Connection failed: {response.status_code}", "error")
            
    except Exception as e:
        add_log(f"[-] FATAL: Network connection error - {str(e)}", "error")

def disconnect_from_network():
    """قطع الاتصال عن الشبكة"""
    add_log("root@kali:~# ifconfig eth0 down", "cmd")
    add_log("Disconnecting from network...", "info")
    time.sleep(0.5)
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/device/disconnect",
            json={"ip": st.session_state.device_ip},
            timeout=5
        )
        
        if response.status_code == 200:
            add_log(f"[+] Network disconnected successfully", "success")
            st.session_state.is_connected = False
            st.rerun()
        else:
            add_log(f"[-] Disconnection failed: {response.status_code}", "error")
            
    except Exception as e:
        add_log(f"[-] FATAL: Disconnection error - {str(e)}", "error")

def generate_packets(attack_type, count=50):
    """توليد حزم هجوم واقعية"""
    target_ip = "10.0.0.5"
    packets = []
    base_time = datetime.now()

    for i in range(count):
        ts = (base_time + timedelta(milliseconds=i * 10)).isoformat()
        if attack_type == "SYN Flood":
            pkt = {
                "timestamp": ts, "src_ip": st.session_state.device_ip, "dst_ip": target_ip,
                "src_port": random.randint(1024, 65535), "dst_port": 80,
                "protocol": "TCP", "packet_size": 64, "payload_size": 0,
                "ttl": 64, "flags": "S"
            }
        elif attack_type == "UDP Flood":
            pkt = {
                "timestamp": ts, "src_ip": st.session_state.device_ip, "dst_ip": target_ip,
                "src_port": random.randint(1024, 65535), "dst_port": random.randint(1, 65535),
                "protocol": "UDP", "packet_size": 1400, "payload_size": 1360,
                "ttl": 128, "flags": ""
            }
        elif attack_type == "SQL Injection":
            pkt = {
                "timestamp": ts, "src_ip": st.session_state.device_ip, "dst_ip": target_ip,
                "src_port": random.randint(1024, 65535), "dst_port": 80,
                "protocol": "TCP", "packet_size": 500, "payload_size": 460,
                "ttl": 64, "flags": "PA"
            }
        elif attack_type == "Port Scan":
            pkt = {
                "timestamp": ts, "src_ip": st.session_state.device_ip, "dst_ip": target_ip,
                "src_port": random.randint(1024, 65535), "dst_port": i + 1,
                "protocol": "TCP", "packet_size": 40, "payload_size": 0,
                "ttl": 64, "flags": "S"
            }
        else:
            pkt = {
                "timestamp": ts, "src_ip": st.session_state.device_ip, "dst_ip": target_ip,
                "src_port": random.randint(1024, 65535), "dst_port": 80,
                "protocol": "TCP", "packet_size": 100, "payload_size": 60,
                "ttl": 64, "flags": "PA"
            }
        packets.append(pkt)
    return packets

def send_attack(attack_type):
    """إرسال هجوم حقيقي"""
    if not st.session_state.is_connected:
        add_log("[-] ERROR: Not connected to network. Connect first!", "error")
        return
    
    add_log(f"root@kali:~# ./exploit --type {attack_type.lower().replace(' ', '_')}", "cmd")
    add_log(f"[*] Initiating {attack_type} attack...", "warn")
    time.sleep(0.3)
    
    packets = generate_packets(attack_type)
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/attack",
            json={
                "attacker_ip": st.session_state.device_ip,
                "attack_type": attack_type,
                "packets": packets
            },
            timeout=5
        )
        
        if response.status_code == 200:
            res_data = response.json()
            if res_data.get("status") == "blocked":
                add_log(f"[!] ALERT: Smart Defender detected the attack pattern!", "error")
                add_log(f"[!] THREAT SCORE: {res_data.get('threat_score', '0'):.2%}", "error")
                add_log(f"[!] IP {st.session_state.device_ip} has been ISOLATED via iptables.", "error")
                add_log(f"[!] Attack Type: {res_data.get('attack_type', 'Unknown')}", "error")
                st.session_state.is_connected = False
                st.rerun()
            else:
                add_log(f"[+] SUCCESS: Payload delivered to target.", "success")
                add_log(f"[+] Response: {res_data.get('message')}", "info")
        else:
            add_log(f"[-] ERROR: Server returned {response.status_code}", "error")
            
    except Exception as e:
        add_log(f"[-] FATAL: Could not establish connection to target API.", "error")

# واجهة المستخدم الرئيسية
st.markdown("<h1 style='text-align: center; color: #00ff00; text-shadow: 0 0 10px #00ff00;'>💀 HACKER TERMINAL v4.0</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<div class="terminal-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="terminal-header"><span>SESSION: {random.randint(1000,9999)}</span><span>TARGET: 10.0.0.5</span></div>', unsafe_allow_html=True)
    
    terminal_html = '<div class="terminal-output">'
    for log in st.session_state.terminal_logs:
        color_class = f"log-{log['type']}"
        terminal_html += f'<div class="log-entry"><span class="log-time">[{log["time"]}]</span> <span class="{color_class}">{log["msg"]}</span></div>'
    terminal_html += '</div>'
    
    st.markdown(terminal_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 🌐 NETWORK")
    
    # عرض حالة الاتصال
    if st.session_state.is_connected:
        st.markdown(f'<div class="network-status network-connected">● CONNECTED<br>{st.session_state.device_ip}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="network-status network-disconnected">○ DISCONNECTED</div>', unsafe_allow_html=True)
    
    # أزرار الاتصال
    col_net1, col_net2 = st.columns(2)
    with col_net1:
        if st.button("🔌 CONNECT"):
            connect_to_network()
    with col_net2:
        if st.button("🔌 DISCONNECT"):
            disconnect_from_network()
    
    st.markdown("---")
    st.markdown("### 🛠️ EXPLOITS")
    
    if st.button("🚀 SYN FLOOD"):
        send_attack("SYN Flood")
    
    if st.button("💥 UDP FLOOD"):
        send_attack("UDP Flood")
        
    if st.button("🔍 PORT SCAN"):
        send_attack("Port Scan")
        
    if st.button("💉 SQL INJECTION"):
        send_attack("SQL Injection")
        
    st.markdown("---")
    if st.button("🧹 CLEAR CONSOLE"):
        st.session_state.terminal_logs = []
        st.rerun()

    # فحص حالة النظام
    try:
        status_res = requests.get(f"{API_BASE_URL}/api/status", timeout=1)
        if status_res.status_code == 200:
            status_data = status_res.json()
            st.markdown("<p style='color: #00ff00; font-weight: bold;'>● DEFENDER ONLINE</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #555; font-size: 0.8em;'>Blocked: {status_data.get('blocked_count', 0)}</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: #ff0000; font-weight: bold;'>○ DEFENDER OFFLINE</p>", unsafe_allow_html=True)
    except:
        st.markdown("<p style='color: #ff0000; font-weight: bold;'>○ DEFENDER OFFLINE</p>", unsafe_allow_html=True)

# تأخير بسيط لمحاكاة الواقعية
time.sleep(0.1)
