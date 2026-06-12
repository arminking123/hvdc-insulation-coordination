"""Data models for the HVDC Insulation Coordination study.

Each model maps to one layer of the calculation chain:
  SystemParameters  — loaded from YAML, drives everything else
  OvervoltageProfile — Step 1 output
  ArresterSelection  — Step 2 output (one per equipment location)
  WithstandRequirement — Step 3 output
  StandardLevel      — Step 4 output
  ClearanceResult    — Step 5 output
  ICResult           — full result for one equipment location (steps 1-5 bundled)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class SideParameters:
    """Electrical parameters for one side (AC or DC) of the converter station."""

    cov_kv: float
    tov_factor: float
    sfo_factor: float
    ffo_factor: float
    tov_arrester_factor: float
    protection_factor: float
    coordination_factor_kc: float
    side: Literal["ac", "dc"]

    @property
    def tov_kv(self) -> float:
        return round(self.cov_kv * self.tov_factor, 1)

    @property
    def sfo_kv(self) -> float:
        return round(self.cov_kv * self.sfo_factor, 1)

    @property
    def ffo_kv(self) -> float:
        return round(self.cov_kv * self.ffo_factor, 1)


@dataclass
class OvervoltageProfile:
    """Step 1 — overvoltage levels at a given equipment location."""

    location_id: str
    side: Literal["ac", "dc"]
    cov_kv: float
    tov_kv: float      # temporary overvoltage
    sfo_kv: float      # slow-front overvoltage (switching surge)
    ffo_kv: float      # fast-front overvoltage (lightning)


@dataclass
class ArresterSelection:
    """Step 2 — surge arrester parameters for a given location.

    Uc  continuous operating voltage of the arrester
    Ur  rated voltage (must withstand TOV)
    Up  protection level (residual voltage at rated discharge current)
    """

    location_id: str
    side: Literal["ac", "dc"]
    uc_kv: float       # continuous operating voltage ≥ COV
    ur_kv: float       # rated voltage (rounded up from TOV / tov_arrester_factor)
    up_kv: float       # protection level = Ur × protection_factor
    ur_standard_kv: float  # nearest standard Ur above calculated Ur

    @property
    def energy_class(self) -> str:
        """Indicative energy class based on voltage level (generic)."""
        if self.ur_standard_kv >= 300:
            return "EC 4"
        if self.ur_standard_kv >= 150:
            return "EC 3"
        return "EC 2"


@dataclass
class WithstandRequirement:
    """Step 3 — minimum required withstand voltages for equipment insulation."""

    location_id: str
    side: Literal["ac", "dc"]
    required_liwv_kv: float   # lightning impulse withstand voltage required
    required_siwv_kv: float   # switching impulse withstand voltage required


@dataclass
class StandardLevel:
    """Step 4 — nearest standard withstand level at or above the requirement."""

    location_id: str
    side: Literal["ac", "dc"]
    selected_liwv_kv: float
    selected_siwv_kv: float
    margin_liwv_pct: float    # headroom above required (%)
    margin_siwv_pct: float


@dataclass
class ClearanceResult:
    """Step 5 — minimum air clearances derived from the selected LIWV."""

    location_id: str
    phase_earth_m: float      # phase-to-earth minimum clearance
    phase_phase_m: float      # phase-to-phase minimum clearance
    altitude_correction: float  # Ka factor applied
    corrected_phase_earth_m: float
    corrected_phase_phase_m: float

    @property
    def note(self) -> str:
        return (
            "Clearances are indicative engineering estimates using simplified "
            "rod-plane gap relationship. Final values require detailed field "
            "analysis and site-specific verification."
        )


@dataclass
class ICResult:
    """Complete insulation coordination result for one equipment location."""

    location_id: str
    description: str
    side: Literal["ac", "dc"]
    connected_equipment: list[str]
    overvoltage: OvervoltageProfile
    arrester: ArresterSelection
    withstand: WithstandRequirement
    standard: StandardLevel
    clearance: ClearanceResult

    def summary_row(self) -> dict[str, object]:
        """Flat dictionary suitable for tabular export."""
        return {
            "location_id": self.location_id,
            "description": self.description,
            "side": self.side.upper(),
            "cov_kv": self.overvoltage.cov_kv,
            "tov_kv": self.overvoltage.tov_kv,
            "arrester_uc_kv": self.arrester.uc_kv,
            "arrester_ur_kv": self.arrester.ur_standard_kv,
            "arrester_up_kv": self.arrester.up_kv,
            "required_liwv_kv": self.withstand.required_liwv_kv,
            "selected_liwv_kv": self.standard.selected_liwv_kv,
            "required_siwv_kv": self.withstand.required_siwv_kv,
            "selected_siwv_kv": self.standard.selected_siwv_kv,
            "margin_liwv_pct": self.standard.margin_liwv_pct,
            "clearance_phase_earth_m": self.clearance.corrected_phase_earth_m,
            "clearance_phase_phase_m": self.clearance.corrected_phase_phase_m,
            "arrester_energy_class": self.arrester.energy_class,
        }
