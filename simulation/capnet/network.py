"""Capillary-to-arteriole network geometry.

Each capillary node is one capillary endothelial cell (cEC, 20 um long). Each
arteriole node lumps the three circumferential endothelial/smooth-muscle units
of one 20-um axial position of a parenchymal arteriole (PA), following the
arrangement of the published capillary-PA model (Moshkforoush et al. 2020).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

CELL_LENGTH_UM = 20.0      # cEC length used by Moshkforoush et al. 2020
PA_UNITS_PER_NODE = 3      # circumferential EC-SMC units per axial PA position
PA_NODES = 15              # 300 um arteriolar segment
ZONE2_NODE = 12            # recording site 240 um along the PA from the junction
CELLS_PER_SEGMENT = 3      # 60 um capillary segments between branch points
LEVELS = 4                 # branch orders of the capillary tree


@dataclass
class Network:
    n: int
    kind: np.ndarray                 # 0 = cEC, 1 = PA node
    dist_um: np.ndarray              # path distance from the PA junction (cEC) or along PA
    cap_edges: list = field(default_factory=list)   # cEC-cEC and cEC-PA junction edges
    pa_edges: list = field(default_factory=list)    # PA-PA axial edges
    tips: list = field(default_factory=list)        # terminal two-cell sites, list of index arrays
    sites: dict = field(default_factory=dict)       # named sites -> index arrays
    zone2: int = 0
    zone1: int = 0
    name: str = ""

    @property
    def cap(self) -> np.ndarray:
        return self.kind == 0

    @property
    def pa(self) -> np.ndarray:
        return self.kind == 1

    def laplacian(self, edges, weight=1.0) -> np.ndarray:
        L = np.zeros((self.n, self.n))
        for i, j in edges:
            L[i, i] += weight
            L[j, j] += weight
            L[i, j] -= weight
            L[j, i] -= weight
        return L


def _add_tree(nodes_kind, nodes_dist, cap_edges, root_parent, root_dist, levels, tips, level_sites, label):
    """Append a symmetric binary capillary tree whose first cell couples to root_parent."""

    def segment(level, parent, start_dist):
        idx = []
        prev = parent
        for c in range(CELLS_PER_SEGMENT):
            k = len(nodes_kind)
            nodes_kind.append(0)
            nodes_dist.append(start_dist + CELL_LENGTH_UM * (c + 0.5))
            cap_edges.append((prev, k))
            idx.append(k)
            prev = k
        end_dist = start_dist + CELL_LENGTH_UM * CELLS_PER_SEGMENT
        level_sites.setdefault((label, level), []).append(np.array(idx[-2:]))
        if level == levels:
            tips.append(np.array(idx[-2:]))
        else:
            segment(level + 1, idx[-1], end_dist)
            segment(level + 1, idx[-1], end_dist)
        return idx

    segment(1, root_parent, root_dist)


def build(topology: str = "T1") -> Network:
    """Build a network.

    T1: one 4-level binary capillary tree (45 cECs) on a 300-um PA segment.
    T2: two identical trees attached 120 um apart on the same PA segment.
    T3: T1 plus a 3-cell anastomosis joining tips 3 and 4 (different level-2 subtrees).
    """
    kind = [1] * PA_NODES
    dist = [CELL_LENGTH_UM * i for i in range(PA_NODES)]
    pa_edges = [(i, i + 1) for i in range(PA_NODES - 1)]
    cap_edges: list = []
    tips: list = []
    level_sites: dict = {}
    _add_tree(kind, dist, cap_edges, 0, 0.0, LEVELS, tips, level_sites, "a")
    if topology == "T2":
        _add_tree(kind, dist, cap_edges, 6, 0.0, LEVELS, tips, level_sites, "b")
    if topology == "T3":
        a = tips[3][-1]
        b = tips[4][-1]
        prev = a
        for c in range(CELLS_PER_SEGMENT):
            k = len(kind)
            kind.append(0)
            dist.append(np.nan)
            cap_edges.append((prev, k))
            prev = k
        cap_edges.append((prev, b))
    net = Network(n=len(kind), kind=np.array(kind), dist_um=np.array(dist, dtype=float),
                  cap_edges=cap_edges, pa_edges=pa_edges, tips=tips,
                  zone2=ZONE2_NODE, zone1=0, name=topology)
    net.sites = {f"tip{i}": t for i, t in enumerate(tips)}
    # single-site calibration positions on the first tree: last two cells of a level-l segment
    for lvl in range(1, LEVELS + 1):
        net.sites[f"level{lvl}"] = level_sites[("a", lvl)][0]
    return net


def site_distance(net: Network, site: np.ndarray) -> float:
    return float(np.nanmean(net.dist_um[site]))
