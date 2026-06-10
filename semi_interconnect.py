import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ============================================================
# DIAGRAM A — "How chips & memory talk" (interconnect hierarchy)
# ============================================================
fig, ax = plt.subplots(figsize=(16, 11))
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

def box(x, y, w, h, title, body, fc, tc="white", ts=10.5, bs=8.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.3,rounding_size=1.2",
                 fc=fc, ec="white", lw=1.5, zorder=3))
    ax.text(x+w/2, y+h-1.9, title, ha="center", va="top",
            fontsize=ts, fontweight="bold", color=tc, zorder=4)
    ax.text(x+w/2, y+h/2-2.4, body, ha="center", va="center",
            fontsize=bs, color=tc, zorder=4, linespacing=1.4)

C1="#5d3a8e"; C2="#1f4e79"; C3="#2e6da4"; C4="#0f7b6c"; C5="#7a3b00"; HD="#111"

ax.text(50, 97.5, "How Chips & Memory Talk — the Interconnect Stack",
        ha="center", fontsize=20, fontweight="bold", color=HD)
ax.text(50, 94, "Shortest reach (inside the package) at top  →  longest reach (across the data center) at bottom",
        ha="center", fontsize=11, color="#555", style="italic")

box(8, 80, 84, 11, "1. On-die / die-to-die  (chiplets inside one package)",
    "Standards: UCIe · NVLink-C2C · Infinity Fabric   |   Interface IP: SNPS  CDNS   |   SerDes IP: AWE (Alphawave)",
    C1)
box(8, 66, 84, 11, "2. Chip ↔ Memory  (the HBM / DDR interface)",
    "Memory PHY & controller IP: RMBS (Rambus)  SNPS  CDNS   |   HBM stacks: MU  SK Hynix  Samsung",
    C2)
box(8, 52, 84, 11, "3. Chip ↔ Chip on the board  (PCIe / CXL fabric)",
    "Retimers & CXL/PCIe switches: ALAB (Astera)  AVGO  MRVL  MCHP   |   SerDes / DSP: CRDO (Credo)",
    C3)
box(8, 38, 84, 11, "4. Server ↔ Server  (the network: switches, NICs, DPUs)",
    "Switch silicon: AVGO (Tomahawk/Jericho)  NVDA (Spectrum/Mellanox)  MRVL   |   Systems: ANET  CSCO",
    C4)
box(8, 22, 84, 12, "5. Rack ↔ Rack  (optics & cabling)",
    "Optical transceivers: COHR  LITE  InnoLight   |   Module assembly: FN (Fabrinet)\n"
    "Active electrical cables: CRDO   |   Connectors: APH (Amphenol)  TEL (TE)  Molex",
    C5)

# down-arrows between layers
for y in [80, 66, 52, 38]:
    ax.add_patch(FancyArrowPatch((50, y), (50, y-3), arrowstyle="-|>",
                 mutation_scale=16, lw=2, color="#666", zorder=2))

ax.text(50, 16.5, "Key idea: as transistor shrinks slow down, performance increasingly comes from MOVING DATA faster,",
        ha="center", fontsize=10, color="#444", style="italic")
ax.text(50, 13.2, "so interconnect (SerDes, retimers, switches, optics) is now a primary AI bottleneck — and a primary profit pool.",
        ha="center", fontsize=10, color="#444", style="italic")

plt.tight_layout()
plt.savefig("/home/user/STUPIDMEI/semi_interconnect.png", dpi=145,
            bbox_inches="tight", facecolor="white")
print("A saved")
