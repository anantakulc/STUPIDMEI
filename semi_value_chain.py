import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(17, 11))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

FE = "#1f4e79"   # front-end blue
FE2 = "#2e6da4"
BE = "#7a3b00"   # back-end brown/orange
EQ = "#4a7c2f"   # equipment green
MAT = "#5d3a8e"  # materials purple
HD = "#111111"

def box(x, y, w, h, title, tickers, fc, tc="white"):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.3,rounding_size=1.2",
                 fc=fc, ec="white", lw=1.5, zorder=3))
    ax.text(x + w/2, y + h - 2.3, title, ha="center", va="top",
            fontsize=10.5, fontweight="bold", color=tc, zorder=4)
    ax.text(x + w/2, y + h/2 - 2.2, tickers, ha="center", va="center",
            fontsize=8.2, color=tc, zorder=4, linespacing=1.45)

def arrow(x1, y1, x2, y2, color="#444"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                 arrowstyle="-|>", mutation_scale=18,
                 lw=2, color=color, zorder=2))

# Title
ax.text(50, 97.5, "Semiconductor Manufacturing Value Chain", ha="center",
        fontsize=20, fontweight="bold", color=HD)
ax.text(50, 94, "Front-end (design + wafer fab)  →  Back-end (assembly, packaging, test)",
        ha="center", fontsize=11.5, color="#555", style="italic")

# Band labels
ax.text(2, 88, "FRONT-END", fontsize=13, fontweight="bold", color=FE, rotation=90, va="center")
ax.text(2, 30, "BACK-END", fontsize=13, fontweight="bold", color=BE, rotation=90, va="center")

# ---- FRONT-END design flow (top row) ----
box(8,  78, 20, 11, "1. EDA & IP\n(design tools / cores)",
    "SNPS  CDNS\nARM  (Siemens EDA)", MAT)
box(33, 78, 20, 11, "2. Chip Design (Fabless)",
    "NVDA  AMD  QCOM\nAVGO  AAPL  MRVL\nMediaTek", FE2)
box(58, 78, 20, 11, "3. IDM (design + own fab)",
    "INTC  TXN  MU\nADI  STM  Samsung", FE2)
box(81, 78, 13.5, 11, "Memory",
    "MU  Samsung\nSK Hynix", FE2)

# ---- FRONT-END manufacturing core (middle) ----
box(33, 60, 28, 12.5, "4. FOUNDRY (wafer fabrication)",
    "TSM  Samsung Foundry\nGFS  UMC  SMIC", FE)

# Equipment feeding the fab (left)
box(4, 56, 24, 17, "5. WFE Equipment\n(builds the fab tools)",
    "ASML  (litho/EUV)\nAMAT  LRCX  KLAC\nTokyo Electron\nAdvantest (test)", EQ)

# Materials feeding the fab (right)
box(66, 56, 30, 17, "6. Materials & Chemicals",
    "Shin-Etsu  SUMCO (wafers)\nENTG  CCMP  Linde\nAir Liquide (gases)\nTOK (photoresist)", MAT)

# ---- BACK-END (bottom) ----
box(8,  35, 26, 12.5, "7. OSAT\n(outsourced assembly + test)",
    "ASX (ASE)  AMKR\nJCET  Powertech  Tongfu", BE)
box(38, 35, 26, 12.5, "8. Advanced Packaging\n(CoWoS / HBM stacking)",
    "TSM (CoWoS)  ASX\nAMKR  Besi  Camtek", BE)
box(68, 35, 28, 12.5, "9. Test Equipment\n+ Final Test",
    "TER (Teradyne)\nAdvantest  Cohu", BE)

# ---- END MARKETS ----
box(20, 13, 60, 11, "END MARKETS / SYSTEMS",
    "Data center & AI (NVDA, AVGO, DELL, SMCI)   ·   Smartphones (AAPL, QCOM)\n"
    "Autos (NXPI, ON, TXN)   ·   Industrial / PCs   ·   Hyperscalers (MSFT, GOOGL, AMZN, META)",
    "#333")

# Arrows: design -> foundry
arrow(43, 78, 45, 72.7, FE)
arrow(68, 78, 55, 72.7, FE)
# equipment + materials -> foundry
arrow(28, 64, 33, 66, EQ)
arrow(66, 64, 61, 66, MAT)
# foundry -> back-end
arrow(40, 60, 24, 47.7, BE)
arrow(47, 60, 51, 47.7, BE)
arrow(54, 60, 80, 47.7, BE)
# back-end -> end markets
arrow(34, 35, 42, 24.2, "#333")
arrow(64, 35, 58, 24.2, "#333")

# Legend
ax.text(50, 6.5, "Front-end = turning silicon wafers into patterned circuits (the hard, capital-intensive part).   "
                 "Back-end = cutting, stacking, wiring and testing those dies into finished chips.",
        ha="center", fontsize=9, color="#555", style="italic")

plt.tight_layout()
plt.savefig("/home/user/STUPIDMEI/semi_value_chain.png", dpi=145, bbox_inches="tight",
            facecolor="white")
print("saved")
