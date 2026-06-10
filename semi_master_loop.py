import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(figsize=(23, 14))
ax.set_xlim(0, 116); ax.set_ylim(0, 100); ax.axis("off")

# ---- color palette ----
C_DES="#5d3a8e"; C_FAB="#1f4e79"; C_EQ="#4a7c2f"; C_MAT="#7a5a1e"
C_PKG="#7a3b00"; C_PHO="#0f6b7b"; C_TEST="#0f7b6c"; C_SYS="#b03060"
C_END="#333333"; HD="#0b0b0b"

def box(cx, cy, w, h, title, sub, fc, tc="white", ts=11, ss=8.0):
    ax.add_patch(FancyBboxPatch((cx-w/2, cy-h/2), w, h,
                 boxstyle="round,pad=0.3,rounding_size=1.2",
                 fc=fc, ec="white", lw=2, zorder=5))
    ax.text(cx, cy+h/2-1.7, title, ha="center", va="top", fontsize=ts,
            fontweight="bold", color=tc, zorder=6)
    ax.text(cx, cy+h/2-h*0.40, sub, ha="center", va="center", fontsize=ss,
            color=tc, zorder=6, linespacing=1.3)

# ---- loop node centers (clockwise from top-left) ----
N={
 1:(20,82, C_DES), 2:(50,88, C_DES), 3:(80,78, C_FAB),
 4:(90,52, C_PKG), 5:(80,24, C_PHO), 6:(50,15, C_TEST),
 7:(20,24, C_SYS), 8:(9,53, C_END),
}

def arrow(c1, c2, rad=-0.18, color="#555", lw=2.6, r=12.5):
    (x1,y1),(x2,y2)=c1,c2
    d=np.hypot(x2-x1,y2-y1); ux,uy=(x2-x1)/d,(y2-y1)/d
    sx,sy=x1+ux*r, y1+uy*r; ex,ey=x2-ux*r, y2-uy*r
    ax.add_patch(FancyArrowPatch((sx,sy),(ex,ey),connectionstyle=f"arc3,rad={rad}",
                 arrowstyle="-|>",mutation_scale=24,lw=lw,color=color,zorder=3))

# clockwise loop arrows 1->2->3->4->5->6->7->8->1
seq=[1,2,3,4,5,6,7,8,1]
for a,b in zip(seq,seq[1:]):
    arrow((N[a][0],N[a][1]),(N[b][0],N[b][1]))

# center label
ax.text(50,52,"THE\nSEMICONDUCTOR\nLOOP",ha="center",va="center",
        fontsize=20,fontweight="bold",color=HD,linespacing=1.25)
ax.text(50,43,"demand & $ from end markets\nfund the next design cycle",ha="center",
        va="center",fontsize=9,color="#666",style="italic",linespacing=1.2)

# ---- the eight loop stages ----
box(*N[1][:2],26,15,"1 · DESIGN & IP",
    "EDA tools: SNPS  CDNS\nProcessor IP: ARM\n(the blueprint + building blocks)",N[1][2])
box(*N[2][:2],30,15,"2 · CHIP DESIGN",
    "Fabless: NVDA AMD QCOM\nAVGO MRVL AAPL\nIDM: INTC TXN  Memory: MU",N[2][2])
box(*N[3][:2],26,16,"3 · FRONT-END FAB (Foundry)",
    "TSM  Samsung  GFS\nUMC  SMIC\nlitho->deposition->etch->loop",N[3][2])
box(*N[4][:2],24,16,"4 · ASSEMBLY &\nADVANCED PACKAGING",
    "CoWoS/SoIC: TSM\nOSAT: ASX AMKR JCET\nhybrid-bond eqpt: BESI KLIC",N[4][2])
box(*N[5][:2],24,15,"5 · PHOTONICS (optical I/O)",
    "Transceivers: COHR LITE\nAssembly: FN  CPO: AVGO\nDSP: MRVL CRDO",N[5][2])
box(*N[6][:2],26,14,"6 · TEST",
    "ATE: TER  Advantest\nProbe cards: FORM\nHandlers: COHU AEHR",N[6][2])
box(*N[7][:2],26,16,"7 · SYSTEM INTEGRATION",
    "Interconnect: ALAB CRDO AVGO\nSwitches/NIC: NVDA MRVL\nStorage: MU STX WDC SIMO",N[7][2])
box(*N[8][:2],15,17,"8 · END\nMARKETS",
    "AI / data center\nMSFT GOOGL\nAMZN META\nphones autos",N[8][2],ts=10,ss=7.6)

# ---- feeder blocks into the fab (equipment + materials) ----
box(104,84,18,14,"WFE EQUIPMENT",
    "ASML (EUV monopoly)\nAMAT  LRCX  TEL  KLAC",C_EQ,ts=10,ss=7.8)
box(106,62,16,13,"MATERIALS",
    "wafers: Shin-Etsu\nSUMCO  gases: Linde\nENTG  TOK (resist)",C_MAT,ts=10,ss=7.6)
# feeder arrows into foundry (node 3)
ax.add_patch(FancyArrowPatch((96,82),(89,79),arrowstyle="-|>",mutation_scale=20,
             lw=2.4,color=C_EQ,zorder=4))
ax.add_patch(FancyArrowPatch((98,62),(89,73),arrowstyle="-|>",mutation_scale=20,
             lw=2.4,color=C_MAT,zorder=4))
ax.text(104,74,"build / supply\nthe fab",ha="center",fontsize=7.5,color="#555",style="italic")

# ---- process-control note spanning fab+packaging+test ----
ax.text(50,97.5,"The Semiconductor Loop — One Connected Cycle",ha="center",
        fontsize=22,fontweight="bold",color=HD)
ax.text(50,94,"Blueprint -> wafer -> finished package -> tested chip -> system -> end market -> funds the next design",
        ha="center",fontsize=11,color="#555",style="italic")

# process control callout (feeds steps 3,4,6)
box(50,30,20,6.5,"PROCESS CONTROL / YIELD",
    "metrology & inspection: KLAC ONTO CAMT",  "#8a6d1e", ts=8.5, ss=7.2)
for tgt in [(80,78),(90,52),(50,15)]:
    ax.add_patch(FancyArrowPatch((50,33),(tgt[0]*0.62+50*0.38, tgt[1]*0.62+30*0.38),
                 arrowstyle="-",lw=1.0,color="#b8a25a",ls=(0,(3,3)),zorder=2))

# legend strip
ax.text(50,4.5,"Bottlenecks (pricing power): ASML EUV  ·  TSM leading-edge foundry  ·  CoWoS/HBM packaging   |   "
               "'Sell the picks': WFE + materials (cyclical, capex-driven)",
        ha="center",fontsize=9,color="#333",
        bbox=dict(boxstyle="round,pad=0.5",fc="#f2f2f4",ec="#cccccc"))

plt.tight_layout()
plt.savefig("/home/user/STUPIDMEI/semi_master_loop.png",dpi=150,bbox_inches="tight",facecolor="white")
print("saved master loop")
