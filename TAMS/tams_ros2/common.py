from dataclasses import dataclass
from typing import Dict

PHASES = ["Reach", "Align", "Grasp", "Transport", "Pre-release", "Release"]
VIEWS = ["EIH", "GT", "GS"]

VIEW_WEIGHTS: Dict[str, Dict[str, float]] = {
    "Reach": {"EIH": 0.23, "GT": 0.50, "GS": 0.27},
    "Align": {"EIH": 0.60, "GT": 0.20, "GS": 0.20},
    "Grasp": {"EIH": 0.60, "GT": 0.20, "GS": 0.20},
    "Transport": {"EIH": 0.25, "GT": 0.30, "GS": 0.45},
    "Pre-release": {"EIH": 0.55, "GT": 0.25, "GS": 0.20},
    "Release": {"EIH": 0.55, "GT": 0.25, "GS": 0.20},
}

@dataclass
class BitrateTargets:
    eih: float
    gt: float
    gs: float

    def as_dict(self) -> Dict[str, float]:
        return {"EIH": self.eih, "GT": self.gt, "GS": self.gs}


def allocate_bitrate(phase: str, uplink_budget_mbps: float, minimum_stream_mbps: float) -> BitrateTargets:
    if phase not in VIEW_WEIGHTS:
        phase = "Reach"
    budget = max(float(uplink_budget_mbps), 0.0)
    floor = max(float(minimum_stream_mbps), 0.0)
    stream_count = len(VIEWS)
    if budget < stream_count * floor:
        equal = budget / stream_count if stream_count else 0.0
        return BitrateTargets(equal, equal, equal)
    remaining = budget - stream_count * floor
    weights = VIEW_WEIGHTS[phase]
    return BitrateTargets(
        floor + weights["EIH"] * remaining,
        floor + weights["GT"] * remaining,
        floor + weights["GS"] * remaining,
    )
