# Semiconductor Ecosystem Map + Six Research Reports

This note bundles two things:

1. A **visual map of the semiconductor manufacturing value chain** — front-end and back-end, the interconnect that makes chips and memory talk, manufacturing and test equipment, and the assembly / photonics / storage corners — each mapped to the public stocks that play in it.
2. **Six full STUPIDMEI research reports** (COHR, AVGO, CLS, ARM, NOW, FN), their recommendations, the formal audit results, and a careful explanation of **why our intrinsic targets sit well below Street targets**.

---

## Part 1 — The semiconductor value chain (visual map)

### 1. Front-end vs back-end overview
Front-end = turning a blank silicon wafer into patterned circuits (capital-intensive, physics-heavy). Back-end = cutting that wafer into dies and packaging / wiring / testing them into finished chips.

![Value chain](../semi_value_chain.png)

- **EDA & IP:** SNPS, CDNS, ARM
- **Fabless design:** NVDA, AMD, QCOM, AVGO, MRVL, AAPL silicon, MediaTek
- **IDM:** INTC, TXN, ADI, STM, Samsung; **Memory:** MU, Samsung, SK Hynix
- **Foundry:** TSM, Samsung Foundry, GFS, UMC, SMIC
- **WFE equipment:** ASML, AMAT, LRCX, KLAC, Tokyo Electron
- **Materials:** Shin-Etsu, SUMCO, ENTG, CCMP, Linde, TOK

### 2. How chips & memory talk — the interconnect stack
As transistor shrinks slow, performance increasingly comes from *moving data faster*, so interconnect is now a primary AI bottleneck and profit pool.

![Interconnect](../semi_interconnect.png)

- **On-die / die-to-die (chiplets):** UCIe, NVLink-C2C, Infinity Fabric; IP from SNPS, CDNS, AWE
- **Chip ↔ memory (HBM/DDR):** RMBS, SNPS, CDNS; HBM from MU, SK Hynix, Samsung
- **Chip ↔ chip (PCIe/CXL):** ALAB, AVGO, MRVL, MCHP, CRDO
- **Server ↔ server (switches/NICs):** AVGO, NVDA, MRVL; systems ANET, CSCO
- **Rack ↔ rack (optics/cabling):** COHR, LITE, InnoLight, FN, CRDO, APH, TEL

### 3. Manufacturing & test equipment by process step
The "Big 5" WFE (ASML, AMAT, LRCX, TEL, KLAC) are the truest picks-and-shovels — paid on fab capex regardless of which designer wins, but highly cyclical.

![Equipment](../semi_equipment.png)

- **Litho:** ASML (EUV monopoly), Canon, Nikon
- **Deposition / Etch / Implant / CMP / Clean:** AMAT, LRCX, TEL, ASMI, ACLS, Ebara, SCREEN
- **Process control (metrology/inspection):** KLAC, ONTO, CAMT, Nova
- **Back-end packaging equipment:** KLIC, ASMPT, BESI, Disco
- **Test:** TER (Teradyne), Advantest, FORM (probe cards), COHU, AEHR

### 4. Assembly · Photonics · Storage
The three highest-leverage corners of the AI build-out.

![Assembly Photonics Storage](../semi_assembly_photonics_storage.png)

- **Assembly / advanced packaging:** TSM (CoWoS/SoIC), Intel (Foveros), ASX, AMKR, JCET; equipment BESI, KLIC, ASMPT; substrates Ibiden, Shinko, AT&S. *CoWoS/HBM packaging is the literal supply bottleneck gating AI-GPU shipments.*
- **Photonics (optical I/O):** transceivers COHR, LITE, InnoLight, AAOI, assembly FN; co-packaged optics NVDA, AVGO, MRVL, Intel; optical DSP MRVL, CRDO. *Copper runs out of reach at AI bandwidths — light is how racks scale.*
- **Storage:** DRAM/HBM MU, Samsung, SK Hynix; NAND MU, Samsung, SK Hynix, Kioxia, SanDisk; SSD controllers SIMO, MRVL, Phison; HDD STX, WDC; systems PSTG, NTAP, DELL. *HBM + high-capacity NAND/SSD are where the AI cycle shows up inside the memory makers.*

---

## Part 2 — Six research reports

Every ticker has the full STUPIDMEI deliverable set in `output/<TICKER>/`: `<T>.json` (narrative), `<T>_inputs.json` (assumptions), `<T>_valuation.json` (deterministic math), `<T>_audit.json` (formal audit), `<T>.xlsx`, `<T>.pdf`. Prices are live yfinance closes pulled this session (2026-06-10). NOW reflects an apparent ~5:1 split in this dataset.

| Ticker | Role in the chain | Method | Price | 12m target | Upside | Call |
|---|---|---|---|---|---|---|
| **NOW** | Enterprise workflow SaaS | DCF | $106.97 | $112 | **+4%** | **HOLD** — only one near fair |
| **AVGO** | Custom XPUs + AI networking + VMware | SOTP | $392.16 | $370 | **−6%** | **HOLD, negative bias** |
| **FN** | Optical-module assembly | DCF | $586.00 | $234 | **−60%** | **SELL** (valuation) |
| **COHR** | Optical transceivers / lasers | DCF | $355.94 | $114 | **−68%** | **SELL** (valuation) |
| **CLS** | AI-server EMS | DCF | $371.86 | $112 | **−70%** | **SELL** (valuation) |
| **ARM** | Compute IP / royalties | DCF | $324.86 | $47 | **−86%** | **SELL** (valuation) |

These are genuine AI-ecosystem winners. The SELLs are **valuation calls, not quality calls** — each report gives the bull case its full due (8 catalysts apiece) and then lets the deterministic DCF render the verdict.

### Formal audit results
All six were audited with the `equity-audit` skill (re-run every compute script, diff against published, recompute every blended target, re-verify prices).

| Ticker | Verdict | Reproducible | Notable finding |
|---|---|---|---|
| COHR | PASS_WITH_NOTES | ✅ byte-for-byte | First draft probabilities summed to 1.05 (bull 0.15); **caught and corrected to 1.0** |
| FN | PASS_WITH_NOTES | ✅ byte-for-byte | Same 1.05 → 1.0 correction |
| AVGO | PASS_WITH_NOTES | ✅ byte-for-byte | SOTP `blended_target` is the base aggregate ($368); narrative target ($370) is the probability-weighted blend — both now disclosed |
| CLS | PASS_WITH_NOTES | ✅ byte-for-byte | Core finding rests on live price + disclosed revenue estimate |
| ARM | PASS_WITH_NOTES | ✅ byte-for-byte | −86% gap is assumption-sensitive (disclosed) but driven by a verified ~70x-sales price |
| NOW | PASS_WITH_NOTES | ✅ byte-for-byte | Least assumption-sensitive; intrinsic ≈ price |

**What "PASS_WITH_NOTES" means here:** the math is fully reproducible and the live prices / share counts / market caps are real same-session yfinance pulls. The *fundamentals* (net debt, revenue, segment margins, historical financials, peer multiples) are domain estimates — yfinance `.history`/`.info`/`.financials` returned thin/NaN this session and the FUNDA/ADANOS data sources were unauthenticated — so they are flagged in each report's `data_gaps` and in the audit. The directional conclusions are robust to reasonable error in those estimates; the one most sensitive to assumptions (ARM) says so explicitly.

---

## Part 3 — Why our targets sit so far below the Street

This is the most important thing to understand about these reports. The gap is **structural and methodological**, not a modeling error.

### a) Different method: intrinsic DCF vs forward-multiple comps
Our targets come from a **discounted-cash-flow** model anchored to fundamentals: project free cash flow, discount it at a fair WACC (10–12% for these tech betas), add a mature terminal value (3–4% perpetual growth). Most sell-side price targets are built from **forward multiples** — apply a peer/历史 P/E, EV/EBITDA or EV/Sales to next year's estimate and roll it forward. In a thematic melt-up, multiple-based targets *follow the price up*: the stock re-rates, the comp set re-rates, the target re-rates. A DCF refuses to do that.

### b) These stocks trade at extreme sales multiples
The underlying cash margins simply cannot support the prices on any disciplined DCF:

| Ticker | EV/Sales (≈) | Operating margin | The tension |
|---|---|---|---|
| ARM | ~70x | ~30% (rising) | IP royalty franchise, but no cash flow justifies 70x sales for years |
| COHR | ~12x | ~13% | Components maker margins reset every optical generation |
| FN | ~6x | ~12–13% | Contract assembler economics, designer's multiple |
| CLS | ~4x | ~6–8% | EMS historically trades ~0.4x sales |
| NOW | ~8.5x | ~30% FCF margin | A 20% grower with 30% FCF margin *can* support this — hence HOLD, not SELL |

### c) The reverse-DCF: what the price actually implies
The cleanest way to see the gap is to invert the model — solve for how much free cash flow the market is paying for, expressed as a multiple of our **base-case** FCF path:

| Ticker | Price implies this ×base-case FCF | Where the price sits vs our scenarios |
|---|---|---|
| **ARM** | **7.75×** | above our Bull case |
| **CLS** | **2.90×** | above our Bull case |
| **COHR** | **2.62×** | above our Bull case |
| **FN** | **2.55×** | above our Bull case |
| **NOW** | **0.90×** | below our Base case (i.e., slightly cheap) |

Read the ARM row literally: to justify today's price, you must believe ARM generates roughly **eight times** the free cash flow our base DCF projects over the next decade — and the current price is *above* even the optimistic Bull scenario we modeled. For COHR, CLS and FN the market is paying ~2.5–2.9× our base FCF and is, again, *above* our Bull case. That is the entire "below Street" gap in one number: the Street (and the market) is capitalizing a far longer and steeper cash-flow trajectory — or far higher permanent terminal multiples — than a value-disciplined model will grant.

### d) Honest caveat: where this model is weakest
A DCF like this **systematically reads "expensive" for high-multiple compounders during a thematic boom**, for three reasons it cannot fully escape:

1. **Duration of hypergrowth.** We decelerate growth toward a mature terminal rate within ~8 years. If AI optical / IP / server demand compounds at 20%+ for *15* years, our terminal value is too low. The market is betting on the longer runway.
2. **Terminal economics.** We apply a 3–4% perpetual growth and a normal WACC. The Street implicitly assumes these franchises keep a premium multiple forever, which a Gordon-growth terminal cannot replicate.
3. **Momentum is real and can persist.** Intrinsic value is a gravity, not a timer. A stock can stay 2–3× above DCF fair value for years while the narrative holds. Our model will be "early" (i.e., wrong) for as long as the multiple persists.

**So treat these as value-discipline flags, not trade timers.** The message is not "short ARM tomorrow." It is: *at these prices you are paying several times what the cash flows justify, the margin of safety is negative, and the burden of proof is entirely on continued flawless, multi-year execution.* NOW is the one name where intrinsic value and price meet — which is exactly why it is the only HOLD-and-add in the basket rather than a SELL.

---

*Methodology lives in `_schema/` (SPEC_v2.md, VALUATION_SCHEMA.md, the compute scripts, render_excel.py, render_pdf.py). Same inputs always produce the same outputs; the Excel and PDF layouts are locked templates. Fundamentals flagged in each report's `data_gaps` should be refreshed against live filings before acting.*
