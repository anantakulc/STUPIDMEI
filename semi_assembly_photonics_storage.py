import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(18, 11.5))
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

def box(x, y, w, h, title, body, fc, tc="white", ts=9.6, bs=7.9):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.3,rounding_size=1.0",
                 fc=fc, ec="white", lw=1.3, zorder=3))
    ax.text(x+w/2, y+h-1.5, title, ha="center", va="top",
            fontsize=ts, fontweight="bold", color=tc, zorder=4)
    ax.text(x+w/2, y+h/2-1.9, body, ha="center", va="center",
            fontsize=bs, color=tc, zorder=4, linespacing=1.35)

def header(x, y, w, text, color):
    ax.add_patch(FancyBboxPatch((x, y), w, 4,
                 boxstyle="round,pad=0.2,rounding_size=0.8",
                 fc=color, ec="none", zorder=3))
    ax.text(x+w/2, y+2, text, ha="center", va="center",
            fontsize=12.5, fontweight="bold", color="white", zorder=4)

HD="#111"
ASM="#7a3b00"; ASM2="#9c5a1e"
PHO="#0f6b7b"; PHO2="#138a9e"
STO="#5d3a8e"; STO2="#74519e"

ax.text(50, 97.8, "Assembly · Photonics · Storage", ha="center",
        fontsize=21, fontweight="bold", color=HD)
ax.text(50, 94.2, "Three high-leverage corners of the semiconductor ecosystem",
        ha="center", fontsize=11.5, color="#555", style="italic")

# ============ COLUMN 1 — ASSEMBLY / ADVANCED PACKAGING ============
header(3, 88, 30, "ASSEMBLY /\nPACKAGING".replace("\n"," "), ASM)
box(3, 73.5, 30, 13, "Advanced packaging\n(CoWoS · SoIC · Foveros)",
    "TSM (CoWoS leader)\nIntel (Foveros/EMIB)\nSamsung", ASM)
box(3, 59, 30, 13, "OSAT\n(outsourced assembly+test)",
    "ASX (ASE)  AMKR (Amkor)\nJCET  Powertech  Tongfu", ASM2)
box(3, 44.5, 30, 13, "Packaging equipment",
    "BESI (hybrid bonding)\nKLIC (K&S)  ASMPT\nCAMT / ONTO (inspect)", ASM)
box(3, 30, 30, 13, "Substrates & materials",
    "ABF substrates: Ibiden\nShinko · AT&S · Unimicron\nMaterials: ENTG", ASM2)

# ============ COLUMN 2 — PHOTONICS ============
header(35, 88, 30, "PHOTONICS\n(optical I/O)".replace("\n"," "), PHO)
box(35, 73.5, 30, 13, "Optical transceivers\n(800G / 1.6T modules)",
    "COHR (Coherent)  LITE (Lumentum)\nInnoLight · Eoptolink\nAAOI · module asm: FN", PHO)
box(35, 59, 30, 13, "Lasers & components",
    "COHR  LITE\nAAOI (Applied Opto)\nindium-phosphide lasers", PHO2)
box(35, 44.5, 30, 13, "Co-packaged optics (CPO)\n+ silicon photonics",
    "NVDA (CPO switches)\nAVGO  MRVL  Intel\n(emerging: optics in package)", PHO)
box(35, 30, 30, 13, "Optical DSP / retimers",
    "MRVL (electro-optics)\nCRDO  AVGO\n(drives the light signal)", PHO2)

# ============ COLUMN 3 — STORAGE ============
header(67, 88, 30, "STORAGE\n(memory + drives)".replace("\n"," "), STO)
box(67, 73.5, 30, 13, "DRAM + HBM\n(working memory)",
    "MU (Micron)  Samsung\nSK Hynix\nHBM = AI-leveraged slice", STO)
box(67, 59, 30, 13, "NAND flash\n(non-volatile)",
    "MU  Samsung  SK Hynix\n(Solidigm)  Kioxia\nSanDisk (ex-WDC)", STO2)
box(67, 44.5, 30, 13, "SSD controllers\n+ interface",
    "SIMO (Silicon Motion)\nMRVL  Phison\nRMBS (memory interface)", STO)
box(67, 30, 30, 13, "HDD + storage systems",
    "STX (Seagate)  WDC\nSystems: PSTG  NTAP  DELL", STO2)

# Bottom takeaway band
ax.add_patch(FancyBboxPatch((3, 13.5), 94, 11,
             boxstyle="round,pad=0.3,rounding_size=1.0",
             fc="#f1f1f4", ec="#cccccc", lw=1, zorder=2))
ax.text(50, 22.5, "Why these three matter for the AI build-out:", ha="center",
        fontsize=11, fontweight="bold", color=HD)
ax.text(50, 18.6,
        "ASSEMBLY: CoWoS / HBM packaging is the literal supply bottleneck gating AI-GPU shipments.\n"
        "PHOTONICS: copper runs out of reach at AI bandwidths — light (optics / co-packaged optics) is how racks scale.\n"
        "STORAGE: HBM + high-capacity NAND/SSD are where the AI cycle shows up inside the memory makers.",
        ha="center", va="center", fontsize=9.2, color="#333", linespacing=1.5)

plt.tight_layout()
plt.savefig("/home/user/STUPIDMEI/semi_assembly_photonics_storage.png", dpi=145,
            bbox_inches="tight", facecolor="white")
print("saved")
