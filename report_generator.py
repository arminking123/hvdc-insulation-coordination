# Engineering methodology

## Why insulation coordination matters for HVDC

In a ±320 kV VSC-HVDC link, a flashover or insulation failure can disconnect
two power grids simultaneously. Insulation coordination is the engineering
process that prevents this: it ensures every piece of equipment can withstand
every overvoltage it will ever see, with the surge arrester absorbing any
exceedance before the insulation breaks down.

## The five-step chain

### Step 1 — Overvoltage classification

The system sees three classes of overvoltage:

| Class | Origin | Timescale | Typical factor on COV |
|---|---|---|---|
| TOV | Load rejection, earth faults | seconds–minutes | 1.05–1.15 |
| SFO | Switching surges, converter firing | milliseconds | 1.5–2.0 |
| FFO | Lightning, travelling waves | microseconds | 1.8–2.5 |

Factors are derived from electromagnetic transient (PSCAD/EMTP) simulations
of the actual project. Conservative standard-aligned values are used in this
preliminary study.

### Step 2 — Surge arrester selection

A metal oxide surge arrester (MOSA) clamps overvoltages before they damage
equipment insulation. Three parameters define it:

- **Uc** (continuous operating voltage) — must handle COV without conducting
- **Ur** (rated voltage) — must survive TOV; selected from standard steps
- **Up** (protection level) — residual voltage at rated discharge current;
  this is what the connected equipment must withstand

### Step 3 — Required withstand voltages

The coordination factor Kc = 1.15 adds a safety margin above the arrester
protection level. This accounts for arrester tolerance, cable travelling
wave effects, and measurement uncertainty.

```
Required LIWV = Up × Kc
Required SIWV = Required LIWV × (SFO_factor / FFO_factor)
```

### Step 4 — Standard level selection

IEC 60071-1 and -4 define a series of standard withstand voltages. The
nearest standard value at or above the required value is selected, and the
margin (headroom) above the requirement is reported. Positive margin is
essential — it must never be negative.

### Step 5 — Minimum air clearances

The minimum distance between live parts and earthed objects (and between
live parts of different polarity) is derived from the selected LIWV.

At higher altitudes, reduced air pressure lowers the dielectric strength
of air gaps. The altitude correction factor Ka compensates:

```
Ka = 1 + 0.00125 × H (H = altitude in metres)
Corrected clearance = uncorrected clearance × Ka
```

## Limitations of this study

1. **Simplified clearance model.** The rod-plane gradient (500 kV/m) is a
   conservative approximation. Real gap factor calculations account for
   electrode geometry, gap configuration, and pressure.

2. **Conservative overvoltage factors.** Standard-aligned preliminary values
   are used. System studies would replace these with project-specific values.

3. **Single arrester location per bus.** Real layouts may require arresters
   at multiple points (cable ends, transformer terminals, busbar tees).

4. **No energy calculation.** Arrester energy class assignment is indicative.
   A proper energy absorption study is required using the fault current and
   charge injection results from the system simulation.
