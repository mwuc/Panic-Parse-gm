"""Domain data tables for iPhone panic-log analysis.

Pure data, no logic. Adding a device generation = add a bitmask table and
routing entries here only.
"""

# Per bitmask entry: "suspected_hardware" is the text emitted in the output's
# suspected_hardware list, "components" is the free-form component key shown in
# the output's components list (for reporting/statistics — it drives nothing
# else), and "description" is a reserved, currently-unused field kept for
# reference. Conventional component keys (not enforced): charging, front_als,
# wireless, battery, interposer, board, gyro, display, sep, rf, storage, audio.

SMC_BITMASK_ARCHITECTURES = {
    # iPhone 16 / 17 series (targets d93, d94, d47, d57, d58, d97, d98 ...)
    "ARCH_IPHONE_16_17": {
        0x080000: {
            "description": "USB-C Charging Port Flex Assembly (Primary Mic mic1 / Barometer prs0)",
            "suspected_hardware": "USB-C Port Flex Assembly",
            "components": "charging",
        },
        0x100000: {
            "description": "Front Earpiece / Proximity & Ambient Light Sensor Flex (ALS/PRX)",
            "suspected_hardware": "Front Earpiece Sensor Flex",
            "components": "front_als",
        },
        0x200000: {
            "description": "Wireless Charging Coil / MagSafe Thermal Sensor Assembly (TW0P)",
            "suspected_hardware": "Wireless Charging / MagSafe Coil",
            "components": "wireless",
        },
        0x400000: {
            "description": "Battery Gas Gauge Bus / Power Button Flex Line",
            "suspected_hardware": "Battery Connector / Power Button Flex",
            "components": "battery",
        },
        0x800000: {
            "description": "Display Driver Interposer / Face ID Bus Line",
            "suspected_hardware": "Display / Face ID Interposer Bus",
            "components": "interposer",
        },
    },
    # iPhone 15 Pro series (targets d83, d84)
    "ARCH_IPHONE_15_PRO": {
        0x040000: {
            "description": "Charging Port Flex Assembly (Legacy Bitfield)",
            "suspected_hardware": "Lightning/USB-C Port Assembly",
            "components": "charging",
        },  
        0x080000: {
            "description": "Charging Port Flex Assembly / Air Pressure Sensor",
            "suspected_hardware": "Charging Port Flex Assembly / Air Pressure Sensor",
            "components": "charging",
        },
        0x100000: {
            "description": "Charging Port Flex Assembly",
            "suspected_hardware": "Charging Port Flex Assembly",
            "components": "charging",
        },
        0x200000: {
            "description": "Front Proximity / Ambient Light Sensor Flex Assembly",
            "suspected_hardware": "Front Proximity / Ambient Light Sensor Flex Assembly",
            "components": "front_als",
        },
        0x400000: {
            "description": "Wireless Charging Flex (Back Glass)",
            "suspected_hardware": "Wireless Charging Flex (Back Glass)",
            "components": "wireless",
        },
    },
    # iPhone 15 series (targets d37, d38)
    "ARCH_IPHONE_15": {
        0x040000: {
            "description": "Charging Port Flex Assembly (Legacy Bitfield)",
            "suspected_hardware": "Lightning/USB-C Port Assembly",
            "components": "charging",
        },  
        0x080000: {
            "description": "Charging Port Flex Assembly / Air Pressure Sensor",
            "suspected_hardware": "Charging Port Flex Assembly / Air Pressure Sensor",
            "components": "charging",
        },
        0x100000: {
            "description": "Front Proximity Flex Assembly",
            "suspected_hardware": "Front Proximity Flex Assembly",
            "components": "front_als",
        },
         0x200000: {
            "description": "Wireless Charging Flex (Back Glass)",
            "suspected_hardware": "Wireless Charging Flex (Back Glass)",
            "components": "wireless",
        },
    },
    # iPhone 14 Pro series (targets d73, d74)
    "ARCH_IPHONE_14_PRO": {
            0x020000: {
                "description": "Sandwich board",
                "suspected_hardware": "Sandwich board",
                "components": "board",
            },
            0x040000: {
                "description": "Charging Port Flex Assembly (Legacy Bitfield)",
                "suspected_hardware": "Lightning/USB-C Port Assembly",
                "components": "charging",
            },  
            0x080000: {
                "description": "Front Proximity / Ambient Light Sensor Flex (Legacy Bitfield)",
                "suspected_hardware": "Front Sensor Flex",
                "components": "front_als",
            },             
            0x100000: {
                "description": "Power Button Flex",
                "suspected_hardware": "Power Button Flex",
                "components": "battery",
            },
        },
    # iPhone 14 series (targets d27, d28)
    "ARCH_IPHONE_14": {
            0x020000: {
                "description": "Sandwich board",
                "suspected_hardware": "Sandwich board",
                "components": "board",
            },           
            0x100000: {
                "description": "Charging Port Flex Assembly (Legacy Bitfield)",
                "suspected_hardware": "Lightning/USB-C Port Assembly",
                "components": "charging",
            },
            0x200000: {
                "description": "Front Proximity Sensor / Ambient Light Sensor Flex (Legacy Bitfield)",
                "suspected_hardware": "Front Sensor Flex",
                "components": "front_als",
            },
            0x400000: {
                "description": "Wireless Charging Flex (Back Glass)",
                "suspected_hardware": "Wireless Charging Flex Back Glass",
                "components": "wireless",
            },
        },
    # iPhone 13 series (targets d17, d16, d63, d64)
    "ARCH_IPHONE_13": {
        0x000400: {
            "description": "Bottom board",
            "suspected_hardware": "Bottom board",
            "components": "board",
        },
        0x000800: {
            "description": "Charging Port Flex Assembly (Legacy Bitfield)",
            "suspected_hardware": "Lightning/USB-C Port Assembly",
            "components": "charging",
        },
        0x001000: {
            "description": "Front Proximity Sensor / Ambient Light Sensor Flex (Legacy Bitfield)",
            "suspected_hardware": "Front Sensor Flex",
            "components": "front_als",
        },
        0x004000: {
            "description": "Battery Data Line",
            "suspected_hardware": "Battery Connector / Power Button Flex",
            "components": "battery",
        },
    },
    # iPhone 11 / 12 series (targets N104, D53, D54, D42, D43, N841)
    "ARCH_IPHONE_11_12": {
        0x000100: {
            "description": "Charging Port Primary Mic Failure (mic1)",
            "suspected_hardware": "Charging Port Mic1",
            "components": "charging",
        },
        0x000200: {
            "description": "Power Button / Rear Noise-Canceling Mic Failure (mic2)",
            "suspected_hardware": "Power Flex Mic2",
            "components": "board",
        },
        0x000400: {
            "description": "Front Earpiece Mic Failure (mic3)",
            "suspected_hardware": "Front Earpiece Mic3",
            "components": "front_als",
        },
        0x000800: {
            "description": "Charging Port Barometer Sensor Failure (prs0)",
            "suspected_hardware": "Barometer prs0 Sensor",
            "components": "charging",
        },
    },
    "DEFAULT_GENERIC": {
        0x001000: {
            "description": "Charging Port Assembly",
            "suspected_hardware": "Charging Port Area",
            "components": "charging",
        },
        0x004000: {
            "description": "Battery sensor",
            "suspected_hardware": "Battery Sensor",
            "components": "battery",
        },
        0x020000: {
            "description": "Gyroscope / Accelerometer ICs on Logic Board",
            "suspected_hardware": "Gyroscope / Accelerometer ICs on Logic Board",
            "components": "gyro",
        },
        0x040000: {
            "description": "Charging Port Assembly / Bottom Sensor Array",
            "suspected_hardware": "Charging Port Area",
            "components": "charging",
        },
        0x080000: {
            "description": "Front Proximity / Ambient Light Sensor Flex Assembly",
            "suspected_hardware": "Front Sensor Flex",
            "components": "front_als",
        },
        0x100000: {
            "description": "Power Button / Rear Noise-Canceling Mic Flex Assembly",
            "suspected_hardware": "Power Button Flex",
            "components": "board",
        },
        0x200000: {
            "description": "Wireless Charging / MagSafe Module",
            "suspected_hardware": "Wireless Charging Module",
            "components": "wireless",
        },
    },
    # ==================== iPad architectures ====================
    # Full-screen iPad Pro / Air (M1 / M2 / M4 / A12X/Z)
    # (J317/J320, J517/J522, J617/J620, J717/J720, J407, J507/J537 ...)
    "ARCH_IPAD_MX": {
        0x00001: {
            "description": "Cold solder joint in the core area of the motherboard or an open circuit in the step-down power supply circuit.",
            "suspected_hardware": "SOC / CPU Core NTC",
            "components": "board",
        },
        0x00100: {
            "description": "Side-mounted magnetic wireless charging board flex cable",
            "suspected_hardware": "Pencil Magnetic Charging Module",
            "components": "charging",
        },
        0x00800: {
            "description": "Magnetic keyboard contact ribbon cable",
            "suspected_hardware": "Smart Connector",
            "components": "board",
        },
        0x02000: {
            "description": "The ambient light sensor ribbon cable at the top of the screen is damaged.",
            "suspected_hardware": "ALS (Ambient Light Sensor) / Face ID / Top Front-Facing Camera Flex Cable",
            "components": "front_als",
        },
        0x40000: {
            "description": "The temperature sensor on the bottom daughterboard is open-circuited, not securely connected, or the ribbon cable is damaged.",
            "suspected_hardware": "USB-C / Thunderbolt Dock Flex Cable",
            "components": "charge",
        },
        0x80000: {
            "description": "PD controller chip (Tristar/Hydra/CD3217) is damaged.",
            "suspected_hardware": "USB-C CC/PD Controller Chip",
            "components": "board",
        },
        0x100000: {
            "description": "Open circuit in the four-speaker sub-board ribbon cable or burnt-out power amplifier IC.",
            "suspected_hardware": "Speaker / Audio Amp Area Thermistor",
            "components": "audio",
        },
        0x400000: {
            "description": "Faulty display backlight cable on the Pro 12.9 M4 Pro",
            "suspected_hardware": "NTC for Mini-LED/OLED Backlight Driver Board",
            "components": "display",
        },
        0x800000: {
            "description": "Magnetic Connector / Wireless Charging & Accessory Path",
            "suspected_hardware": "Magnetic Connector / Wireless Charging & Accessory Path",
            "components": "charging",
        },
        0x1000000: {
            "description": "Wireless/Celluar module failure",
            "suspected_hardware": "Cellular Board Flex",
            "components": "wireless",
        },
        0x2000000: {
            "description": "Pencil 2 Charging Rail",
            "suspected_hardware": "Pencil 2 Charging Rail",
            "components": "charging",
        },                
    },
    # iPad Mini 6/A17 Pro, Air 4 (J310/J311, J410, J307/J308)
    "ARCH_IPAD_6": {
        0x00001: {
            "description": "Battery FPC Connector / Board PMU abnormality",
            "suspected_hardware": "Battery FPC Connector / Board PMU",
            "components": "board",
        },
        0x00004: {
            "description": "BMS communication fail",
            "suspected_hardware": "Battery FPC Connector / USB-C charging port flex)",
            "components": "charging",
        },
        0x00080: {
            "description": "Side Power Button (Touch ID / Power Flex Cable) were damaged",
            "suspected_hardware": "Side Power Button (Touch ID / Power Flex Cable)",
            "components": "board",
        },
        0x00100: {
            "description": "Side-mounted magnetic wireless charging board flex cable",
            "suspected_hardware": "Pencil Magnetic Charging Module",
            "components": "charging",
        },
        0x01000: {
            "description": "Top Volume Button Board NTC (Mini 6 Specific)",
            "suspected_hardware": "Top Volume Button Board NTC",
            "components": "board",
        },
        0x08000: {
            "description": "Battery protection board data cable abnormality",
            "suspected_hardware": "Battery Gas Gauge / B0T Node",
            "components": "battery",
        },
        0x40000: {
            "description": "Damaged charging port/daughterboard or open circuit in the NTC sensing line.",
            "suspected_hardware": "USB-C charging port flex",
            "components": "charge",
        },
    },
    # iPad 5th-9th, Air 3, Mini 5 (J71/J72, J171/J181, J217, J210 ...)
    "ARCH_IPAD_5_9": {
        0x00002: {
            "description": "Accidentally blew off the surrounding NTC chip resistor.",
            "suspected_hardware": "NAND Flash Area Thermistor",
            "components": "storage",
        },
        0x00010: {
            "description": "Home Button / Touch ID Flex Cable was damaged",
            "suspected_hardware": "Home Button / Touch ID Flex Cable",
            "components": "board",
        },
        0x02000: {
            "description": "Ambient Light Sensor & True Tone Flex Cable",
            "suspected_hardware": "Ambient Light Sensor & True Tone Flex Cable",
            "components": "front_als",
        },
        0x08000: {
            "description": "Battery Cell Temperature (B0T / B0V)",
            "suspected_hardware": "Battery Flex Cable",
            "components": "battery",
        },
        0x10000: {
            "description": "Lightning Connector Flex (Dock Cable)",
            "suspected_hardware": "Lightning Connector Flex (Dock Cable)",
            "components": "board",
        },
    },
    "DEFAULT_IPAD_GENERIC": {},
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
    "ARCH_IPHONE_14": {
        0x500000: ("Battery Connector / Power Button Flex (0x500000)", "battery"),
    },
    "ARCH_IPAD_MX": {
        0x7000000: ("Pencil Pro Charger / FPC Connector (0x7000000)", "charging"),
    },
}

# Missing-sensor text -> (suspected_hardware text, component key)
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

# iPad missing-sensor text -> (suspected_hardware text, component key).
# Platform-specific: the same sensor name can map to different hardware on
# iPad vs iPhone (e.g. tg0b -> board on iPad, battery on iPhone).
IPAD_SENSOR_HARDWARE_MAP = {
    'tg0b': ('Mainboard Core / GPU Power Area NTC', 'board'),
    'tg0v': ('Mainboard Core / GPU Power Area NTC', 'board'),
    'tg0p': ('SoC / CPU Processor Thermal Node', 'board'),
    'tb0t': ('Battery Protection Board / Battery NTC', 'battery'),
    'tb1t': ('Battery Protection Board / Battery NTC', 'battery'),
    'ta0p': ('Ambient Light Sensor (ALS) / Top Front Camera Flex', 'front_als'),
    'ta0s': ('Ambient Light Sensor (ALS) / Top Front Camera Flex', 'front_als'),
    'tp0d': ('USB-C / Lightning Dock Flex NTC', 'charge'),
    'tp0p': ('USB-C / Lightning Dock Flex NTC', 'charge'),
    't2m0': ('Mainboard Frame / Edge Area Thermal Node', 'board'),
    't2m1': ('Mainboard Frame / Edge Area Thermal Node', 'board'),
    'ts0p': ('Speaker / Audio Amp Thermal Sensor', 'audio'),
    'tc0d': ('Charging IC / Smart Connector ', 'charge'),
    'tc0p': ('Charging IC / Smart Connector ', 'charge'),
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
    # --- iPad target codes ---
    'j71b': 'ARCH_IPAD_5_9',
    'j72b': 'ARCH_IPAD_5_9',
    'j71s': 'ARCH_IPAD_5_9',
    'j72s': 'ARCH_IPAD_5_9',
    'j171': 'ARCH_IPAD_5_9',
    'j172': 'ARCH_IPAD_5_9',
    'j171a': 'ARCH_IPAD_5_9',
    'j172a': 'ARCH_IPAD_5_9',
    'j181': 'ARCH_IPAD_5_9',
    'j182': 'ARCH_IPAD_5_9',
    'b201': 'ARCH_IPAD_6',
    'b202': 'ARCH_IPAD_6',
    'j481': 'ARCH_IPAD_6',
    'j482': 'ARCH_IPAD_6',
    'j71': 'ARCH_IPAD_5_9',
    'j72': 'ARCH_IPAD_5_9',
    'j81': 'ARCH_IPAD_5_9',
    'j82': 'ARCH_IPAD_5_9',
    'j217': 'ARCH_IPAD_5_9',
    'j218': 'ARCH_IPAD_5_9',
    'j307': 'ARCH_IPAD_6',
    'j308': 'ARCH_IPAD_6',
    'j407': 'ARCH_IPAD_MX',
    'j408': 'ARCH_IPAD_MX',
    'j507': 'ARCH_IPAD_MX',
    'j508': 'ARCH_IPAD_MX',
    'j537': 'ARCH_IPAD_MX',
    'j538': 'ARCH_IPAD_MX',
    'P101': 'ARCH_IPAD_5_9',
    'P102': 'ARCH_IPAD_5_9',
    'P103': 'ARCH_IPAD_5_9',
    'j85': 'ARCH_IPAD_5_9',
    'j86': 'ARCH_IPAD_5_9',
    'j87': 'ARCH_IPAD_5_9',
    'j85m': 'ARCH_IPAD_5_9',
    'j86m': 'ARCH_IPAD_5_9',
    'j87m': 'ARCH_IPAD_5_9',
    'j96': 'ARCH_IPAD_5_9',
    'j97': 'ARCH_IPAD_5_9',
    'j210': 'ARCH_IPAD_5_9',
    'j211': 'ARCH_IPAD_5_9',
    'j310': 'ARCH_IPAD_6',
    'j311': 'ARCH_IPAD_6',
    'j410': 'ARCH_IPAD_6',
    'j411': 'ARCH_IPAD_6',
    'ipad14p': 'ARCH_IPAD_6',
    'j127': 'ARCH_IPAD_5_9',
    'j128': 'ARCH_IPAD_5_9',
    'j207': 'ARCH_IPAD_5_9',
    'j208': 'ARCH_IPAD_5_9',
    'j317': 'ARCH_IPAD_MX',
    'j317x': 'ARCH_IPAD_MX',
    'j318': 'ARCH_IPAD_MX',
    'j318x': 'ARCH_IPAD_MX',
    'j417': 'ARCH_IPAD_MX',
    'j418': 'ARCH_IPAD_MX',
    'j517': 'ARCH_IPAD_MX',
    'j517x': 'ARCH_IPAD_MX',
    'j518': 'ARCH_IPAD_MX',
    'j518x': 'ARCH_IPAD_MX',
    'j522': 'ARCH_IPAD_MX',
    'j523': 'ARCH_IPAD_MX',
    'j717': 'ARCH_IPAD_MX',
    'j718': 'ARCH_IPAD_MX',
    'j98a': 'ARCH_IPAD_5_9',
    'j99a': 'ARCH_IPAD_5_9',
    'j120': 'ARCH_IPAD_5_9',
    'j121': 'ARCH_IPAD_5_9',
    'j320': 'ARCH_IPAD_MX',
    'j320x': 'ARCH_IPAD_MX',
    'j321': 'ARCH_IPAD_MX',
    'j321x': 'ARCH_IPAD_MX',
    'j420': 'ARCH_IPAD_MX',
    'j421': 'ARCH_IPAD_MX',
    'j522x': 'ARCH_IPAD_MX',
    'j523x': 'ARCH_IPAD_MX',
    'j620': 'ARCH_IPAD_MX',
    'j621': 'ARCH_IPAD_MX',
    'j720': 'ARCH_IPAD_MX',
    'j721': 'ARCH_IPAD_MX',
}

# Exact product string ("product" field / "Hardware model:" text, e.g.
# "iPhone15,4") -> architecture. The product-map number does NOT track the
# marketing generation (e.g. iPhone13,x is the iPhone 12 family), so route by
# full product string, not by major number.
#
# Routing fallback rules (routing.py):
#   - iPhone product with major number <= 10 and no exact entry above
#     -> DEFAULT_GENERIC (old iPhone; no bitmask table exists)
#   - iPhone product with major number >= 11 and no exact entry above
#     -> the newest PRODUCT_GENERATION_FALLBACK generation at or below its
#        major number (forward compatibility); if no fallback covers it,
#        NOT_SUPPORTED (routing-data gap; add the entry instead of guessing)
#   - iPad product with no exact entry above -> the newest
#     IPAD_PRODUCT_GENERATION_FALLBACK generation at or below its major,
#     else NOT_SUPPORTED
#   - iPod / Watch / AppleTV -> NOT_SUPPORTED
#
# Supported ranges: iPhone 11 and later; iPad 5th generation and later.
NOT_SUPPORTED = "NOT_SUPPORTED"
NOT_SUPPORTED_MESSAGE = "Not Supported"

# iPhone product code mapping; refer to https://khwang9883.github.io/MobileModels/brands/apple_all.html
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
    "iPhone18,5": "ARCH_IPHONE_16_17",
    "iPhone19,2": "ARCH_IPHONE_16_17",
    "iPhone19,3": "ARCH_IPHONE_16_17",
    "iPhone19,4": "ARCH_IPHONE_16_17",
    "iPhone19,7": "ARCH_IPHONE_16_17",
    # --- iPad product codes ---
    'iPad6,11': 'ARCH_IPAD_5_9',
    'iPad6,12': 'ARCH_IPAD_5_9',
    'iPad7,5': 'ARCH_IPAD_5_9',
    'iPad7,6': 'ARCH_IPAD_5_9',
    'iPad7,11': 'ARCH_IPAD_5_9',
    'iPad7,12': 'ARCH_IPAD_5_9',
    'iPad11,6': 'ARCH_IPAD_5_9',
    'iPad11,7': 'ARCH_IPAD_5_9',
    'iPad12,1': 'ARCH_IPAD_5_9',
    'iPad12,2': 'ARCH_IPAD_5_9',
    'iPad13,18': 'ARCH_IPAD_6',
    'iPad13,19': 'ARCH_IPAD_6',
    'iPad15,7': 'ARCH_IPAD_6',
    'iPad15,8': 'ARCH_IPAD_6',
    'iPad4,1': 'ARCH_IPAD_5_9',
    'iPad4,2': 'ARCH_IPAD_5_9',
    'iPad4,3': 'ARCH_IPAD_5_9',
    'iPad5,3': 'ARCH_IPAD_5_9',
    'iPad5,4': 'ARCH_IPAD_5_9',
    'iPad11,3': 'ARCH_IPAD_5_9',
    'iPad11,4': 'ARCH_IPAD_5_9',
    'iPad13,1': 'ARCH_IPAD_6',
    'iPad13,2': 'ARCH_IPAD_6',
    'iPad13,16': 'ARCH_IPAD_MX',
    'iPad13,17': 'ARCH_IPAD_MX',
    'iPad14,8': 'ARCH_IPAD_MX',
    'iPad14,9': 'ARCH_IPAD_MX',
    'iPad14,10': 'ARCH_IPAD_MX',
    'iPad14,11': 'ARCH_IPAD_MX',
    'iPad2,5': 'ARCH_IPAD_5_9',
    'iPad2,6': 'ARCH_IPAD_5_9',
    'iPad2,7': 'ARCH_IPAD_5_9',
    'iPad4,4': 'ARCH_IPAD_5_9',
    'iPad4,5': 'ARCH_IPAD_5_9',
    'iPad4,6': 'ARCH_IPAD_5_9',
    'iPad4,7': 'ARCH_IPAD_5_9',
    'iPad4,8': 'ARCH_IPAD_5_9',
    'iPad4,9': 'ARCH_IPAD_5_9',
    'iPad5,1': 'ARCH_IPAD_5_9',
    'iPad5,2': 'ARCH_IPAD_5_9',
    'iPad11,1': 'ARCH_IPAD_5_9',
    'iPad11,2': 'ARCH_IPAD_5_9',
    'iPad14,1': 'ARCH_IPAD_6',
    'iPad14,2': 'ARCH_IPAD_6',
    'iPad16,1': 'ARCH_IPAD_6',
    'iPad16,2': 'ARCH_IPAD_6',
    'iPad6,3': 'ARCH_IPAD_5_9',
    'iPad6,4': 'ARCH_IPAD_5_9',
    'iPad7,3': 'ARCH_IPAD_5_9',
    'iPad7,4': 'ARCH_IPAD_5_9',
    'iPad8,1': 'ARCH_IPAD_MX',
    'iPad8,2': 'ARCH_IPAD_MX',
    'iPad8,3': 'ARCH_IPAD_MX',
    'iPad8,4': 'ARCH_IPAD_MX',
    'iPad8,9': 'ARCH_IPAD_MX',
    'iPad8,10': 'ARCH_IPAD_MX',
    'iPad13,4': 'ARCH_IPAD_MX',
    'iPad13,5': 'ARCH_IPAD_MX',
    'iPad13,6': 'ARCH_IPAD_MX',
    'iPad13,7': 'ARCH_IPAD_MX',
    'iPad14,3': 'ARCH_IPAD_MX',
    'iPad14,4': 'ARCH_IPAD_MX',
    'iPad16,3': 'ARCH_IPAD_MX',
    'iPad16,4': 'ARCH_IPAD_MX',
    'iPad6,7': 'ARCH_IPAD_5_9',
    'iPad6,8': 'ARCH_IPAD_5_9',
    'iPad7,1': 'ARCH_IPAD_5_9',
    'iPad7,2': 'ARCH_IPAD_5_9',
    'iPad8,5': 'ARCH_IPAD_MX',
    'iPad8,6': 'ARCH_IPAD_MX',
    'iPad8,7': 'ARCH_IPAD_MX',
    'iPad8,8': 'ARCH_IPAD_MX',
    'iPad8,11': 'ARCH_IPAD_MX',
    'iPad8,12': 'ARCH_IPAD_MX',
    'iPad13,8': 'ARCH_IPAD_MX',
    'iPad13,9': 'ARCH_IPAD_MX',
    'iPad13,10': 'ARCH_IPAD_MX',
    'iPad13,11': 'ARCH_IPAD_MX',
    'iPad14,5': 'ARCH_IPAD_MX',
    'iPad14,6': 'ARCH_IPAD_MX',
    'iPad16,5': 'ARCH_IPAD_MX',
    'iPad16,6': 'ARCH_IPAD_MX',
}

# Forward-compatibility floor table: an iPhone product NOT listed in
# PRODUCT_MAP_ROUTING inherits the newest architecture whose key is <= its
# major number. The key is the *threshold*, not a literal product major, so a
# single {17: ...} entry also covers 18, 19 and every future generation —
# newly released iPhones diagnose without a data edit, and the same bitmask
# layout stays valid while the platform is unchanged. Add a new entry (e.g.
# {20: "ARCH_IPHONE_20"}) only when a generation introduces a new SMC layout;
# majors 11-16 have no entry and therefore keep the NOT_SUPPORTED signal.
PRODUCT_GENERATION_FALLBACK = {
    17: "ARCH_IPHONE_16_17",
}

# Forward-compatibility floor table for iPads (same semantics as the iPhone
# one above). Kept separate because the keys collide with the iPhone table.
IPAD_PRODUCT_GENERATION_FALLBACK = {
    17: 'ARCH_IPAD_MX',
}
