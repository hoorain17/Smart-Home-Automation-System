import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# Load images
device_management_img = Image.open("device_managment.jpg")
energy_tracker_img = Image.open("energy_tracker.jpg")
automation_img = Image.open("automation.jpg")

# ----------------------------- Device Management ----------------------------- #
def device_management():
    st.header("🔧 Device Management")
    st.image(device_management_img, use_container_width=True)

    st.markdown("### Manage Your Smart Devices")

    if 'devices' not in st.session_state:
        st.session_state.devices = ['Lights', 'Fan', 'AC', 'Door Lock', 'Thermostat']
    if 'device_settings' not in st.session_state:
        st.session_state.device_settings = []

    col1, col2, col3 = st.columns(3)

    with col1:
        st.text_input("Add Device", key="new_device_name")
        st.button("➕ Add", on_click=lambda: add_device(st.session_state.new_device_name.strip()))

    with col2:
        st.text_input("Remove Device", key="remove_device_name")
        st.button("🗑️ Remove", on_click=lambda: remove_device(st.session_state.remove_device_name.strip()))

    with col3:
        st.button("🔃 Sort Devices", on_click=sort_devices)

    st.markdown("**Current Devices:**")
    st.success(", ".join(st.session_state.devices))

    st.divider()
    st.markdown("### Device Power Settings")

    if not st.session_state.device_settings:
        for device in st.session_state.devices:
            # Default status is OFF
            st.session_state[f"status_{device}"] = "ON"
            st.session_state[f"power_{device}"] = 0
            st.session_state.device_settings.append({"device": device, "status": "ON", "power": 20})

    # Display device power settings in a more visually appealing way
    power_data = {setting['device']: setting['power'] for setting in st.session_state.device_settings}
    st.markdown("#### Power Consumption Overview")
    st.write(power_data)

    # Plot power usage graph
    plot_power_usage(power_data)

    for setting in st.session_state.device_settings:
        st.info(f"**{setting['device']}** → Status: {setting['status']}, Power: {setting['power']}W")

def plot_power_usage(power_data):
    devices = list(power_data.keys())
    power_values = list(power_data.values())
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(devices, power_values, color='skyblue')
    ax.set_xlabel('Devices')
    ax.set_ylabel('Power (W)')
    ax.set_title('Device Power Consumption')
    ax.set_xticklabels(devices, rotation=45, ha="right")
    st.pyplot(fig)

def add_device(name):
    if not name:
        st.error("⚠️ Please enter a device name.")
    elif name in st.session_state.devices:
        st.warning(f"⚠️ '{name}' already exists.")
    else:
        st.session_state.devices.append(name)
        st.success(f"✅ '{name}' added successfully!")

def remove_device(name):
    if name in st.session_state.devices:
        st.session_state.devices.remove(name)
        st.success(f"🗑️ '{name}' removed.")
    else:
        st.error(f"❌ Device '{name}' not found.")

def sort_devices():
    st.session_state.devices.sort()
    st.success("🔃 Devices sorted alphabetically.")


# ----------------------------- Energy Tracker ----------------------------- #
def energy_tracker():
    st.header("⚡ Energy Consumption Tracker")
    st.image(energy_tracker_img, use_container_width=True)

    if 'energy_usage' not in st.session_state:
        st.session_state.energy_usage = {'Lights': 5, 'AC': 120, 'Fan': 30}

    st.markdown("### Monitor & Update Energy Usage")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.text_input("Add Device", key="add_device_name")
        st.number_input("Usage (kWh)", value=0, key="add_usage")
        st.button("➕ Add Usage", on_click=add_energy_usage)

    with col2:
        st.text_input("Update Device", key="update_device_name")
        st.number_input("New Usage (kWh)", value=0, key="update_usage")
        st.button("🔄 Update Usage", on_click=update_energy_usage)

    with col3:
        st.text_input("Remove Device", key="remove_device_name")
        st.button("🗑️ Remove Usage", on_click=remove_energy_usage)

    st.markdown("### 🔍 Current Energy Usage")
    st.write(st.session_state.energy_usage)

    if st.button("📊 Calculate Total Energy"):
        total = sum(st.session_state.energy_usage.values())
        st.success(f"🔋 Total Energy Consumption: **{total} kWh**")

    # Plot energy consumption graph
    plot_energy_usage(st.session_state.energy_usage)

    # Power Saving Modes
    st.divider()
    st.markdown("### 🌱 Power-Saving Modes")

    if 'power_modes' not in st.session_state:
        st.session_state.power_modes = {'Eco Mode', 'Night Mode'}

    col1, col2 = st.columns(2)

    with col1:
        st.text_input("Add New Mode", key="new_mode_name")
        st.button("➕ Add Mode", on_click=add_power_mode)

    with col2:
        st.text_input("Check Mode Availability", key="check_mode_name")
        st.button("🔍 Check Mode", on_click=check_power_mode)

    if st.button("📜 View All Modes"):
        st.info(", ".join(st.session_state.power_modes))

def plot_energy_usage(energy_usage):
    devices = list(energy_usage.keys())
    usage_values = list(energy_usage.values())
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(devices, usage_values, color='lightgreen')
    ax.set_xlabel('Devices')
    ax.set_ylabel('Energy Usage (kWh)')
    ax.set_title('Energy Consumption by Device')
    ax.set_xticklabels(devices, rotation=45, ha="right")
    st.pyplot(fig)

def add_energy_usage():
    device = st.session_state.add_device_name.strip()
    usage = st.session_state.add_usage
    if device and device not in st.session_state.energy_usage:
        st.session_state.energy_usage[device] = usage
        st.success(f"✅ '{device}' usage added.")
    elif device in st.session_state.energy_usage:
        st.warning("⚠️ Device already exists. Use update instead.")
    else:
        st.error("❌ Please enter a valid device name.")

def update_energy_usage():
    device = st.session_state.update_device_name.strip()
    usage = st.session_state.update_usage
    if device in st.session_state.energy_usage:
        st.session_state.energy_usage[device] = usage
        st.success(f"🔄 '{device}' usage updated.")
    else:
        st.error("❌ Device not found.")

def remove_energy_usage():
    device = st.session_state.remove_device_name.strip()
    if device in st.session_state.energy_usage:
        del st.session_state.energy_usage[device]
        st.success(f"🗑️ '{device}' removed.")
    else:
        st.error("❌ Device not found.")

def add_power_mode():
    new_mode = st.session_state.new_mode_name.strip()
    if new_mode and new_mode not in st.session_state.power_modes:
        st.session_state.power_modes.add(new_mode)
        st.success(f"🌿 New Mode Added: '{new_mode}'")
    elif not new_mode:
        st.error("⚠️ Please enter a mode name.")
    else:
        st.warning(f"⚠️ '{new_mode}' already exists.")

def check_power_mode():
    mode_to_check = st.session_state.check_mode_name.strip()
    if mode_to_check in st.session_state.power_modes:
        st.success(f"✅ '{mode_to_check}' is available.")
    else:
        st.error(f"❌ '{mode_to_check}' not found.")


# ----------------------------- Automation ----------------------------- #
def automation():
    st.header("🏡 Smart Home Automation")
    st.image(automation_img, use_container_width=True)

    st.markdown("### 📋 Set Automation Rule")
    device = st.text_input("Device Name")
    time = st.text_input("Time (e.g., 10:00 PM)")
    action = st.selectbox("Action", ["ON", "OFF"])

    if st.button("✅ Set Rule"):
        rule = f"{device} will be turned {action.upper()} at {time}."
        st.success(f"📌 Rule Set: {rule}")

    st.divider()
    st.markdown("### ⚙️ Optimize Power Consumption")
    num_devices = st.number_input("Number of Devices", min_value=1, value=1)
    devices = []

    for i in range(num_devices):
        name = st.text_input(f"Device Name {i+1}")
        power = st.number_input(f"{name} Power (W)", value=0)
        devices.append((name, power))

    if st.button("🧠 Optimize"):
        optimized = [name for name, power in devices if power <= 1000]
        st.success(f"⚡ Optimized Devices: {', '.join(optimized)}")

    st.divider()
    st.markdown("### 🤖 Smart Home Assistant")
    name = st.text_input("Homeowner Name")
    devices_input = st.text_input("Devices to check (comma-separated)")
    devices_to_check = [d.strip() for d in devices_input.split(",") if d.strip()]

    num_commands = st.number_input("Number of Commands", min_value=0, value=0)
    commands = {}

    for i in range(num_commands):
        dev = st.text_input(f"Command Device {i+1}").lower()
        status = st.selectbox(f"Status for {dev}", ["ON", "OFF"], key=f"status_{i}")
        commands[dev] = status

    if st.button("🚀 Run Assistant"):
        st.write(f"👋 Hello {name}, your Smart Home Assistant is active!")
        if devices_to_check:
            st.write(f"📡 Checking status for: {', '.join(devices_to_check)}")
        else:
            st.info("No devices selected for status check.")

        for dev, stat in commands.items():
            st.write(f"✅ {dev.title()} set to {stat.upper()}")


# ----------------------------- Main ----------------------------- #
def main():
    st.set_page_config(page_title="Smart Home Automation", layout="centered")
    st.title("🏠 Smart Home Automation System")
    menu = ["Device Management", "Energy Tracker", "Automation"]
    choice = st.sidebar.radio("📂 Navigation", menu)

    if choice == "Device Management":
        device_management()
    elif choice == "Energy Tracker":
        energy_tracker()
    elif choice == "Automation":
        automation()

if __name__ == "__main__":
    main()
