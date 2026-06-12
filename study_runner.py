# HVDC Insulation Coordination Study — System Definition
#
# All values are generic, standard-aligned engineering parameters for a
# ±320 kV VSC-HVDC converter station. This file is the single source of
# truth for the study: changing values here re-runs the full calculation chain.
#
# NOTE: All data is synthetic demo data for portfolio purposes.

project:
  name: "Demo VSC-HVDC Link — Converter Station A"
  voltage_class: "±320 kV VSC-HVDC"
  report_number: "IC-STUDY-0001"
  revision: "P01"
  author: "Armin Shahbazi"
  note: "Synthetic demo data — not for use in any real project."

site:
  name: "Converter Station A"
  altitude_m: 50          # metres above sea level (affects clearance correction)
  pollution_level: "III"  # IEC 60815 light/medium/heavy/very heavy → I/II/III/IV
  # Altitude correction factor Ka = (1 + 0.0012 * H) where H = altitude in metres
  # For H = 50 m: Ka ≈ 1.06 — small but included for completeness

# DC side: pole-to-earth operating voltage
dc_system:
  cov_kv: 320.0           # Continuous Operating Voltage (kV), pole-to-earth
  topology: "bipolar"     # bipolar / monopolar
  # Overvoltage factors (multipliers on COV) from system studies / standard practice
  tov_factor: 1.10        # Temporary overvoltage (sustained, e.g. load rejection)
  sfo_factor: 1.70        # Slow-front overvoltage (switching surge)
  ffo_factor: 2.20        # Fast-front overvoltage (lightning / travelling wave)
  # Arrester parameters
  tov_arrester_factor: 1.10   # TOV capability / Uc ratio for DC MOSA
  protection_factor: 1.65     # Up/Ur ratio (residual voltage at rated discharge current)
  # Coordination factor (IEC 60071-1 — directly connected arrester)
  coordination_factor_kc: 1.15

# AC system: 400 kV network connecting to converter transformer HV side
ac_system:
  nominal_kv: 400.0
  # Overvoltage factors for 400 kV AC network (standard-aligned)
  tov_factor: 1.40        # Includes earth-fault factor for solidly earthed system
  sfo_factor: 2.50        # Switching surge factor at 400 kV
  ffo_factor: 4.00        # Lightning withstand factor (conservative for open air)
  # Arrester parameters
  tov_arrester_factor: 1.25
  protection_factor: 1.55
  coordination_factor_kc: 1.15

# Equipment locations to study — each gets its own arrester selection
# and withstand voltage requirement
equipment_locations:
  - id: "DC-POLE-A"
    description: "DC busbar pole A (positive)"
    side: "dc"
    connected_equipment:
      - "DC switchgear (SWG-DC-201)"
      - "Smoothing reactor (SR-DC-001)"
      - "Converter transformer valve-side bushing (TR-CONV-001)"

  - id: "DC-POLE-B"
    description: "DC busbar pole B (negative)"
    side: "dc"
    connected_equipment:
      - "DC switchgear (SWG-DC-202)"
      - "Smoothing reactor (SR-DC-002)"
      - "Converter transformer valve-side bushing (TR-CONV-002)"

  - id: "DC-CABLE-SEALING-END"
    description: "DC cable sealing end"
    side: "dc"
    connected_equipment:
      - "DC cable termination"
      - "DC surge arrester at cable end"

  - id: "AC-HV-BUS"
    description: "400 kV AC busbar (converter transformer HV side)"
    side: "ac"
    connected_equipment:
      - "Converter transformer HV bushing (TR-CONV-001/002)"
      - "AC switchgear (SWG-AC-101)"

  - id: "TRANSFORMER-NEUTRAL"
    description: "Converter transformer neutral / valve-side"
    side: "ac"
    connected_equipment:
      - "Converter transformer valve winding"
      - "Valve-side surge arrester"

# Standard withstand voltage table (IEC 60071-1 / -4 aligned, generic values)
# Used for step 4: selecting the nearest standard level above the required value.
# Format: { required_up_to_kv: standard_liwv_kv, standard_siwv_kv }
standard_withstand_levels:
  dc_liwv_table:
    - { up_to_kv: 400,  liwv_kv: 450,  siwv_kv: 375  }
    - { up_to_kv: 500,  liwv_kv: 550,  siwv_kv: 450  }
    - { up_to_kv: 650,  liwv_kv: 750,  siwv_kv: 620  }
    - { up_to_kv: 850,  liwv_kv: 950,  siwv_kv: 800  }
    - { up_to_kv: 1050, liwv_kv: 1175, siwv_kv: 950  }
  ac_liwv_table:
    - { up_to_kv: 900,  liwv_kv: 1050, siwv_kv: 850  }
    - { up_to_kv: 1175, liwv_kv: 1300, siwv_kv: 1050 }
    - { up_to_kv: 1425, liwv_kv: 1425, siwv_kv: 1050 }
    - { up_to_kv: 1700, liwv_kv: 1800, siwv_kv: 1425 }
