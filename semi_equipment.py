import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ============================================================
# DIAGRAM B — Manufacturing & Test equipment by process step
# ============================================================
fig, ax = plt.subplots(figsize=(17, 11))
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

def box(x, y, w, h, title, body, fc, tc="white", ts=10, bs=8.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.3,rounding_size=1.1",
                 fc=fc, ec="white", lw=1.4, zorder=3))
    ax.text(x+w/2, y+h-1.7, title, ha="center", va="top",
            fontsize=ts, fontweight="bold", color=tc, zorder=4)
    ax.text(x+w/2, y+h/2-2.0, body, ha="center", va="center",
            fontsize=bs, color=tc, zorder=4, linespacing=1.35)

FE="#1f4e79"; PC="#b8860b"; BE="#7a3b00"; TE="#0f7b6c"; HD="#111"

ax.text(50, 97.5, "Semiconductor Manufacturing & Test — Equipment by Step",
        ha="center", fontsize=20, fontweight="bold", color=HD)
ax.text(50, 94, "Front-end wafer processing (blue) → Process control (gold) → Back-end packaging (brown) → Test (teal)",
        ha="center", fontsize=10.5, color="#555", style="italic")

# ---- Front-end wafer process steps (repeated 100s of times) ----
ax.text(50, 90, "FRONT-END WAFER PROCESSING  (loop repeated for every layer)",
        ha="center", fontsize=12, fontweight="bold", color=FE)

box(4,  77, 21, 10.5, "Lithography\n(pattern the layer)",
    "ASML  (EUV monopoly)\nCanon · Nikon (DUV)", FE)
box(27, 77, 21, 10.5, "Deposition\n(add material: CVD/PVD/ALD)",
    "AMAT  LRCX\nTEL · ASMI (ASM Intl)", FE)
box(50, 77, 21, 10.5, "Etch\n(carve the pattern)",
    "LRCX (leader)\nAMAT · TEL", FE)
box(73, 77, 23, 10.5, "Implant / CMP / Clean",
    "Implant: AMAT  ACLS (Axcelis)\nCMP: AMAT · Ebara\nClean: SCREEN · TEL", FE)

# ---- Process control (spans across) ----
box(14, 63, 72, 9, "PROCESS CONTROL — Metrology & Inspection  (checks every step; yield police)",
    "KLAC (Process-control leader)   ·   ONTO (Onto Innovation)   ·   CAMT (Camtek)   ·   Nova",
    PC, tc="#222")

# ---- Back-end packaging ----
ax.text(50, 58.5, "BACK-END  —  ASSEMBLY & PACKAGING", ha="center",
        fontsize=12, fontweight="bold", color=BE)
box(6,  44, 27, 11, "Dicing / Die attach\n/ Wire bond",
    "KLIC (Kulicke & Soffa)\nASMPT  Disco", BE)
box(37, 44, 27, 11, "Advanced packaging\n(2.5D/3D, hybrid bond)",
    "BESI (hybrid bonding)\nASMPT · AMAT", BE)
box(68, 44, 28, 11, "Inspection (packaging)\n+ Substrates",
    "CAMT (Camtek)  ONTO\nSubstrates: Ibiden · Shinko · AT&S", BE)

# ---- Test ----
ax.text(50, 39.5, "TEST  —  does the chip actually work?", ha="center",
        fontsize=12, fontweight="bold", color=TE)
box(8,  24, 26, 12, "Automated Test Equipment\n(ATE — the testers)",
    "TER (Teradyne)\nADTTF / 6857 (Advantest,\ndominant in AI/HBM test)", TE)
box(38, 24, 26, 12, "Probe cards\n(touch each die on wafer)",
    "FORM (FormFactor)\nTechnoprobe", TE)
box(68, 24, 28, 12, "Handlers / Burn-in\n/ System-level test",
    "COHU (Cohu)\nAdvantest · Aehr (AEHR)", TE)

# Flow arrows
ax.add_patch(FancyArrowPatch((50, 63), (50, 56), arrowstyle="-|>",
             mutation_scale=18, lw=2.2, color="#555", zorder=2))
ax.add_patch(FancyArrowPatch((50, 44), (50, 36), arrowstyle="-|>",
             mutation_scale=18, lw=2.2, color="#555", zorder=2))

ax.text(50, 17, "WFE (wafer-fab equipment) = the front-end + process-control tools.   "
                "The 'Big 5' WFE: ASML · AMAT · LRCX · TEL · KLAC.",
        ha="center", fontsize=10, color="#444", style="italic")
ax.text(50, 13.6, "Picks-and-shovels logic: these vendors get paid on fab CAPEX regardless of which chip designer wins — but they are highly cyclical.",
        ha="center", fontsize=9.5, color="#444", style="italic")

plt.tight_layout()
plt.savefig("/home/user/STUPIDMEI/semi_equipment.png", dpi=145,
            bbox_inches="tight", facecolor="white")
print("B saved")
