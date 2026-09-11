"""Domain data tables for iPhone panic-log analysis.

Pure data, no logic. Adding a device generation = add a bitmask table,
routing entries, and (if needed) a suggestion template here only.
"""

# Component keys drive repair suggestions. One of:
# charging, front_als, wireless, battery, interposer, board

SMC_BITMASK_ARCHITECTURES = {
    # iPhone 16 / 17 series (targets d93, d94, d47, d57, d58, d97, d98 ...)
    "ARCH_IPHONE_16_17": {
        0x080000: {
            "description": "USB-C Charging Port Flex Assembly (Primary Mic mic1 / Barometer prs0)",
            "component": "USB-C Port Flex Assembly",
            "key": "charging",
        },
        0x100000: {
            "description": "Front Earpiece / Proximity & Ambient Light Sensor Flex (ALS/PRX)",
            "component": "Front Earpiece Sensor Flex",
            "key": "front_als",
        },
        0x200000: {
            "description": "Wireless Charging Coil / MagSafe Thermal Sensor Assembly (TW0P)",
            "component": "Wireless Charging / MagSafe Coil",
            "key": "wireless",
        },
        0x400000: {
            "description": "Battery Gas Gauge Bus / Power Button Flex Line",
            "component": "Battery Connector / Power Button Flex",
            "key": "battery",
        },
        0x800000: {
            "description": "Display Driver Interposer / Face ID Bus Line",
            "component": "Display / Face ID Interposer Bus",
            "key": "interposer",
        },
    },
    # iPhone 15 Pro series (targets d83, d84)
    "ARCH_IPHONE_15_PRO": {
        0x100000: {
            "description": "Charging Port Flex Assembly",
            "component": "Charging Port Flex Assembly",
            "key": "charging",
        },
        0x200000: {
            "description": "Front Proximity / Ambient Light Sensor Flex Assembly",
            "component": "Front Proximity / Ambient Light Sensor Flex Assembly",
            "key": "front_als",
        },
        0x400000: {
            "description": "Wireless Charging Flex (Back Glass)",
            "component": "Wireless Charging Flex (Back Glass)",
            "key": "wireless",
        },
    },
    # iPhone 15 series (targets d37, d38)
    "ARCH_IPHONE_15": {
        0x080000: {
            "description": "Charging Port Flex Assembly / Air Pressure Sensor",
            "component": "Charging Port Flex Assembly / Air Pressure Sensor",
            "key": "charging",
        },
        0x100000: {
            "description": "Front Proximity Flex Assembly",
            "component": "Front Proximity Flex Assembly",
            "key": "front_als",
        },
         0x200000: {
            "description": "Wireless Charging Flex (Back Glass)",
            "component": "Wireless Charging Flex (Back Glass)",
            "key": "wireless",
        },
    },
    # iPhone 14 Pro series (targets d73, d74)
    "ARCH_IPHONE_14_PRO": {
            0x020000: {
                "description": "Sandwich board",
                "component": "Sandwich board",
                "key": "board",
            },
            0x040000: {
                "description": "Charging Port Flex Assembly (Legacy Bitfield)",
                "component": "Lightning/USB-C Port Assembly",
                "key": "charging",
            },  
            0x080000: {
                "description": "Front Proximity / Ambient Light Sensor Flex (Legacy Bitfield)",
                "component": "Front Sensor Flex",
                "key": "front_als",
            },             
            0x100000: {
                "description": "Power Button Flex",
                "component": "Power Button Flex",
                "key": "battery",
            },
        },
    # iPhone 14 series (targets d27, d28)
    "ARCH_IPHONE_14": {
            0x020000: {
                "description": "Sandwich board",
                "component": "Sandwich board",
                "key": "board",
            },           
            0x100000: {
                "description": "Charging Port Flex Assembly (Legacy Bitfield)",
                "component": "Lightning/USB-C Port Assembly",
                "key": "charging",
            },
            0x200000: {
                "description": "Front Proximity Sensor / Ambient Light Sensor Flex (Legacy Bitfield)",
                "component": "Front Sensor Flex",
                "key": "front_als",
            },
            0x400000: {
                "description": "Wireless Charging Flex (Back Glass)",
                "component": "Wireless Charging Flex Back Glass",
                "key": "wireless",
            },
            0x500000: {
                "description": "Battery Data Line / aptic engine",
                "component": "Battery Connector / Power Button Flex",
                "key": "battery",
            },
        },
    # iPhone 13 series (targets d17, d16, d63, d64)
    "ARCH_IPHONE_13": {
        0x000400: {
            "description": "Bottom board",
            "component": "Bottom board",
            "key": "board",
        },
        0x000800: {
            "description": "Charging Port Flex Assembly (Legacy Bitfield)",
            "component": "Lightning/USB-C Port Assembly",
            "key": "charging",
        },
        0x001000: {
            "description": "Front Proximity Sensor / Ambient Light Sensor Flex (Legacy Bitfield)",
            "component": "Front Sensor Flex",
            "key": "front_als",
        },
        0x004000: {
            "description": "Battery Data Line",
            "component": "Battery Connector / Power Button Flex",
            "key": "battery",
        },
    },
    # iPhone 11 / 12 series (targets N104, D53, D54, D42, D43, N841)
    "ARCH_IPHONE_11_12": {
        0x000100: {
            "description": "Charging Port Primary Mic Failure (mic1)",
            "component": "Charging Port Mic1",
            "key": "charging",
        },
        0x000200: {
            "description": "Power Button / Rear Noise-Canceling Mic Failure (mic2)",
            "component": "Power Flex Mic2",
            "key": "board",
        },
        0x000400: {
            "description": "Front Earpiece Mic Failure (mic3)",
            "component": "Front Earpiece Mic3",
            "key": "front_als",
        },
        0x000800: {
            "description": "Charging Port Barometer Sensor Failure (prs0)",
            "component": "Barometer prs0 Sensor",
            "key": "charging",
        },
    },
    "DEFAULT_GENERIC": {
        0x001000: {
            "description": "Charging Port Assembly",
            "component": "Charging Port Area",
            "key": "charging",
        },
        0x004000: {
            "description": "Battery sensor",
            "component": "Battery Sensor",
            "key": "battery",
        },
        0x020000: {
            "description": "Gyroscope / Accelerometer ICs on Logic Board",
            "component": "Gyroscope / Accelerometer ICs on Logic Board",
            "key": "gyro",
        },
        0x040000: {
            "description": "Charging Port Assembly / Bottom Sensor Array",
            "component": "Charging Port Area",
            "key": "charging",
        },
        0x080000: {
            "description": "Front Proximity / Ambient Light Sensor Flex Assembly",
            "component": "Front Sensor Flex",
            "key": "front_als",
        },
        0x100000: {
            "description": "Power Button / Rear Noise-Canceling Mic Flex Assembly",
            "component": "Power Button Flex",
            "key": "board",
        },
        0x200000: {
            "description": "Wireless Charging / MagSafe Module",
            "component": "Wireless Charging Module",
            "key": "wireless",
        },
    },
}

# Exact-match codes take priority over bitwise decomposition.
# All values are sub-byte (< 0x100) so they can never collide with
# combinations of the architecture bitmasks above.
EXACT_CODES = {
    0x41: ("Battery Gas Gauge Data Line Fault (0x41)", "battery"),
    0xA1: ("Battery Gas Gauge Communication Timeout (0xA1 / 161)", "battery"),
    0xA9: ("Battery BMS Data Line Disconnection (0xA9 / 169)", "battery"),
}

# Generation-specific fault signatures. Unlike global EXACT_CODES, these MAY
# overlap bitmask bits: the whole value means one component on this generation,
# not the OR of its bits. Scoped to the architecture key; other generations
# (and DEFAULT_GENERIC) keep decomposing the value into their own bit meanings.
ARCHITECTURE_EXACT_CODES = {
    "ARCH_IPHONE_16_17": {
        0x300000: ("Charging Port Flex Assembly fault (0x300000)", "charging"),
    },
    "ARCH_IPHONE_15_PRO": {
        0x300000: ("Charging Port Flex Assembly fault (0x300000)", "charging"),
    },
}

# Missing-sensor text -> (hardware description, component key)
SENSOR_HARDWARE_MAP = {
    "mic1": ("Charging Port Flex Assembly (Primary Bottom Microphone)", "charging"),
    "mic2": ("Power Button / Rear Flash Flex (Rear Noise-Canceling Mic)", "board"),
    "mic3": ("Front Earpiece Sensor Flex (Top Microphone)", "front_als"),
    "prs0": ("Charging Port Flex Assembly (Barometric Pressure Sensor)", "charging"),
    "tg0b": ("Battery Flex / BMS IC (Battery Thermal Sensor tg0b)", "battery"),
    "tg0v": ("Battery Connector / Charging Circuit (Battery Voltage Sensor tg0v)", "battery"),
    "als": ("Front Earpiece Sensor Flex (Ambient Light Sensor)", "front_als"),
    "prx": ("Front Sensor / Face ID Module (Proximity Sensor)", "front_als"),
    "gyro": ("Logic Board Gyroscope IC & Power Circuit", "board"),
    "accel": ("Logic Board Accelerometer IC & Bus Circuit", "board"),
    "tw0p": ("Wireless Charging Coil / MagSafe Thermal Sensor Flex", "wireless"),
}

# target/<code> substring -> architecture. Checked in order; first match wins.
TARGET_CODE_ROUTING = {
    "d97": "ARCH_IPHONE_16_17",
    "d98": "ARCH_IPHONE_16_17",
    "d93": "ARCH_IPHONE_16_17",
    "d94": "ARCH_IPHONE_16_17",
    "d47": "ARCH_IPHONE_16_17",
    "d57": "ARCH_IPHONE_16_17",
    "v57": "ARCH_IPHONE_16_17",
    "d83": "ARCH_IPHONE_15_PRO",
    "d84": "ARCH_IPHONE_15_PRO",    
    "d37": "ARCH_IPHONE_15",
    "d38": "ARCH_IPHONE_15",
    "d73": "ARCH_IPHONE_14_PRO",
    "d74": "ARCH_IPHONE_14_PRO",
    "d27": "ARCH_IPHONE_14",
    "d28": "ARCH_IPHONE_14",
    "d63": "ARCH_IPHONE_13",
    "d64": "ARCH_IPHONE_13",    
    "d16": "ARCH_IPHONE_13",
    "d17": "ARCH_IPHONE_13",
    "n104": "ARCH_IPHONE_11_12",
    "d53": "ARCH_IPHONE_11_12",
    "d54": "ARCH_IPHONE_11_12",
    "d42": "ARCH_IPHONE_11_12",
    "d43": "ARCH_IPHONE_11_12",
    "n841": "ARCH_IPHONE_11_12",
}

# Exact product string ("product" field / "Hardware model:" text, e.g.
# "iPhone15,4") -> architecture. The product-map number does NOT track the
# marketing generation (e.g. iPhone13,x is the iPhone 12 family), so route by
# full product string, not by major number.
PRODUCT_MAP_ROUTING = {
    "iPhone10,3": "ARCH_IPHONE_11_12",
    "iPhone10,6": "ARCH_IPHONE_11_12",
    "iPhone11,2": "ARCH_IPHONE_11_12",
    "iPhone11,4": "ARCH_IPHONE_11_12",
    "iPhone11,6": "ARCH_IPHONE_11_12",
    "iPhone11,8": "ARCH_IPHONE_11_12",
    "iPhone12,1": "ARCH_IPHONE_11_12",
    "iPhone12,3": "ARCH_IPHONE_11_12",
    "iPhone12,5": "ARCH_IPHONE_11_12",
    "iPhone12,8": "ARCH_IPHONE_11_12",
    "iPhone13,1": "ARCH_IPHONE_11_12",
    "iPhone13,2": "ARCH_IPHONE_11_12",
    "iPhone13,3": "ARCH_IPHONE_11_12",
    "iPhone13,4": "ARCH_IPHONE_11_12",
    "iPhone14,4": "ARCH_IPHONE_13",
    "iPhone14,5": "ARCH_IPHONE_13",
    "iPhone14,2": "ARCH_IPHONE_13",
    "iPhone14,3": "ARCH_IPHONE_13",
    "iPhone14,6": "ARCH_IPHONE_13",
    "iPhone14,7": "ARCH_IPHONE_14",
    "iPhone14,8": "ARCH_IPHONE_14",
    "iPhone15,2": "ARCH_IPHONE_14_PRO",
    "iPhone15,3": "ARCH_IPHONE_14_PRO",
    "iPhone15,4": "ARCH_IPHONE_15",
    "iPhone15,5": "ARCH_IPHONE_15",
    "iPhone16,1": "ARCH_IPHONE_15_PRO",
    "iPhone16,2": "ARCH_IPHONE_15_PRO",
    "iPhone17,3": "ARCH_IPHONE_16_17",
    "iPhone17,4": "ARCH_IPHONE_16_17",
    "iPhone17,1": "ARCH_IPHONE_16_17",
    "iPhone17,2": "ARCH_IPHONE_16_17",
    "iPhone17,5": "ARCH_IPHONE_16_17",
    "iPhone18,1": "ARCH_IPHONE_16_17",
    "iPhone18,2": "ARCH_IPHONE_16_17",
    "iPhone18,3": "ARCH_IPHONE_16_17",
    "iPhone18,4": "ARCH_IPHONE_16_17",
}

# (component key, template) in fixed emission order. Numbers are part of the
# template text and may skip when a key is not matched (repo convention).
SUGGESTION_TEMPLATES = [
    ("charging", "1. Re-seat or replace the Charging Port Flex Assembly."),
    ("front_als", "2. Inspect or replace the Front Earpiece / Proximity & ALS Sensor Flex Assembly."),
    ("wireless", "3. Inspect the Wireless Charging Coil and MagSafe thermal sensor flex cable."),
    ("battery", "4. Inspect battery connector lines (Gas Gauge) or test with a genuine OEM battery replacement."),
    ("interposer", "5. Potential double-decker logic board interposer fracture or desoldering. Reballing or interposer re-flow required."),
    ("board", "6. It could require a sandwich reball or a bottom board swap."),
    ("gyro", "7. Inspect the Logic Board Gyroscope IC & Power Circuit."),
]

FALLBACK_SUGGESTION = (
    "Check diode mode reading against ground on affected lines "
    "and verify physical connector integrity."
)
