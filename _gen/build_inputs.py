import json, os

def proj(year, rev, gpct, ebit, da=0.07, capex=0.05, wc=0.02, tax=0.21, note=""):
    fcf = rev*ebit*(1-tax) + rev*da - rev*capex - rev*wc
    return {"year": year, "fcf_b": round(fcf,3), "revenue_b": round(rev,3),
            "revenue_growth_pct": gpct, "ebit_margin": ebit, "tax_rate": tax,
            "da_pct_of_revenue": da, "capex_pct_of_revenue": capex,
            "wc_change_pct_of_revenue": wc, "rationale": note}

def dcf_inputs(tkr, price, shares, net_debt, method_reason, sector, wacc, wacc_comp,
               wacc_reason, tg, tg_reason, rows, cc, scenarios, blend_logic, weights_reason,
               adjud=""):
    return {
        "schema_version":"1.0","ticker":tkr,"currency":"USD","current_price":price,
        "shares_outstanding_b":shares,"net_debt_b":net_debt,
        "primary_method":{
            "name":"DCF","category":"intrinsic","reasoning":method_reason,
            "sector_hint":sector,
            "inputs":{
                "wacc":{"value":wacc,"components":wacc_comp,"reasoning":wacc_reason,
                        "adjudication_notes":adjud},
                "terminal_growth":{"value":tg,"reasoning":tg_reason},
                "forecast_horizon_years":len(rows),
                "fcf_projections":rows
            }
        },
        "cross_check":cc,
        "scenarios":scenarios,
        "blending_weights":{"cross_check":0.20},
        "blending_logic":blend_logic,
        "weights_reasoning":weights_reason
    }

def scen(label, kc, prob, preason, reason):
    return {"label":label,"key_changes":kc,"probability":prob,
            "probability_reasoning":preason,"reasoning":reason}

OUT={}

# ============================== COHR ==============================
rows=[
 proj(2026,6.96,20.0,0.13,0.08,0.06,0.025,note="FY26E +20%: datacom transceiver (800G/1.6T) ramp for AI clusters is the engine; telecom and industrial-laser segments recover modestly. Margin lifts as datacom mix rises."),
 proj(2027,8.18,17.5,0.155,0.08,0.06,0.022,note="+17.5%: 1.6T ramp and indium-phosphide laser vertical integration lift gross margin; deleveraging cuts interest drag."),
 proj(2028,9.41,15.0,0.175,0.08,0.055,0.02,note="+15%: AI optical content per cluster keeps compounding; operating leverage on the merged II-VI/Coherent cost base."),
 proj(2029,10.64,13.0,0.19,0.08,0.05,0.018,note="+13%: share gains in CPO-adjacent components; margin nears high-teens EBIT."),
 proj(2030,11.81,11.0,0.20,0.075,0.05,0.015,note="+11%: growth moderates off a larger base; materials and networking segments steady."),
 proj(2031,12.99,10.0,0.21,0.075,0.045,0.015,note="+10%: franchise scaling, ~21% EBIT margin."),
 proj(2032,14.03,8.0,0.22,0.07,0.045,0.012,note="+8%: deceleration continues."),
 proj(2033,14.94,6.5,0.225,0.07,0.04,0.01,note="+6.5%: approaching steady state, low-20s EBIT margin franchise."),
]
cc={"name":"Multiple","category":"relative",
    "reasoning":"EV/EBITDA is the right cross-check for a profitable optical-components maker. Peer set: optical/photonics and AI-networking names. A generous 22x forward EBITDA still anchors well below where the post-run share price sits.",
    "inputs":{"multiple_type":"EV/EBITDA","peer_median_multiple":22.0,"fy_estimate":1.45,
              "peers_used":["LITE","FN","AAOI","MRVL","APH"],
              "reasoning":"22x applied to FY26E EBITDA of ~$1.45B (≈21% margin on $6.96B). Rich for the cohort, chosen to give the AI-optical bull case its due."}}
sc=[
 scen("Bear",{"wacc":0.118,"terminal_growth":0.02,"fcf_multiplier":0.7},0.25,
   "A full quarter-weight. The datacom transceiver market is brutally competitive (InnoLight, Eoptolink), pricing resets each generation, and the stock has 5x'd off its low, leaving no margin for a single soft quarter.",
   "Transceiver pricing compresses faster than volume grows, CPO disintermediates pluggables sooner than expected, and the debt load amplifies the equity hit."),
 scen("Base",{},0.45,
   "Central case. AI optical content keeps compounding and the merged cost base delivers margin, but the share price already discounts a long, smooth ramp.",
   "Steady datacom-led growth decelerating from 20% to high-single-digits, EBIT margin grinding from 13% to low-20s."),
 scen("Bull",{"wacc":0.105,"terminal_growth":0.04,"fcf_multiplier":1.35},0.10,
   "Lower odds. Requires 1.6T and co-packaged-optics content to inflect faster than modeled and indium-phosphide vertical integration to lift margins above plan.",
   "Coherent becomes the preferred Western optical-engine supplier; revenue and margins beat the base path materially."),
]
OUT["COHR"]=dcf_inputs("COHR",355.94,0.195639,4.5,
  "Coherent generates positive and rising free cash flow with a clear AI-datacom revenue ramp and a deleveraging balance sheet, so a long-horizon FCFF DCF captures the path better than a trailing multiple. An EV/EBITDA cross-check anchors the rich post-run valuation.",
  "semiconductors-photonics",0.102,
  {"rf":0.043,"beta":1.45,"erp":0.05,"debt_weight":0.20,"cost_of_debt_after_tax":0.045},
  "Ke = 4.3% Rf + 1.45 beta x 5.0% ERP = 11.55%. Beta above the semi average for transceiver price-cyclicality and post-merger leverage. A ~20% after-tax debt weight on the remaining II-VI/Coherent debt pulls WACC to ~10.2%, inside the 9-12% semi band.",
  0.03,"3.0% terminal: optical content should outgrow GDP as clusters scale, but components face perpetual price pressure, so terminal sits at a mature-semis rate.",
  rows,cc,sc,
  "45% Base + 25% Bear + 10% Bull + 20% EV/EBITDA cross-check.",
  "Bear gets a heavy 25% because transceiver pricing resets and a 5x run leave the stock exposed to any single soft print. Base 45% for the constructive AI-optical ramp. Bull 10% for the CPO/1.6T acceleration. Cross-check 20% anchors intrinsic value against the peer multiple.",
  "10.2% is mid semi band; justified by transceiver cyclicality and residual leverage.")

# ============================== CLS ==============================
rows=[
 proj(2026,13.2,20.0,0.062,0.025,0.012,0.02,note="FY26E +20%: CCS (Connectivity & Cloud Solutions) hyperscaler hardware and 800G switching drive the ramp; ATS (Advanced Tech) steadier. Thin EMS margins by nature."),
 proj(2027,15.4,16.7,0.068,0.025,0.012,0.018,note="+16.7%: HPS (hardware platform solutions) and custom AI server programs scale; modest margin lift from mix and scale."),
 proj(2028,17.4,13.0,0.073,0.025,0.012,0.016,note="+13%: design-win-led growth with one to two anchor hyperscalers; operating margin grinds toward 7%."),
 proj(2029,19.1,10.0,0.077,0.025,0.011,0.014,note="+10%: growth normalizes as the AI build matures; margin near 7.5%."),
 proj(2030,20.8,9.0,0.08,0.025,0.011,0.012,note="+9%: steady compounding, low-8s operating margin (high for an EMS)."),
 proj(2031,22.3,7.0,0.082,0.025,0.01,0.01,note="+7%: deceleration continues."),
 proj(2032,23.6,6.0,0.083,0.025,0.01,0.01,note="+6%: approaching mature EMS growth."),
 proj(2033,24.8,5.0,0.084,0.025,0.01,0.008,note="+5%: steady state."),
]
cc={"name":"Multiple","category":"relative",
    "reasoning":"EV/EBIT cross-check against the EMS/ODM peer set. Even a generous re-rate multiple for an electronics-manufacturing-services company sits far below where the AI-fueled run has taken the shares.",
    "inputs":{"multiple_type":"EV/EBITDA","peer_median_multiple":14.0,"fy_estimate":1.0,
              "peers_used":["FLEX","JBL","SANM","FN","HPE"],
              "reasoning":"14x applied to FY26E EBITDA of ~$1.0B. Double the historical EMS multiple, granted for the AI-mix shift; still implies a value well below spot."}}
sc=[
 scen("Bear",{"wacc":0.13,"terminal_growth":0.02,"fcf_multiplier":0.7},0.30,
   "A heavy 30%. EMS is a thin-margin, customer-concentrated, cyclical business; CLS trades at ~4x sales versus a historical ~0.4x. A single hyperscaler program loss or capex pause re-rates it violently.",
   "Hyperscaler hardware orders digest, customer concentration bites, and the multiple collapses back toward EMS norms."),
 scen("Base",{},0.40,
   "Central case. CCS keeps winning AI server and networking programs and margins grind up, but the valuation already prices a chip-like trajectory onto an EMS cost structure.",
   "Steady design-win-led growth decelerating from 20% to mid-single-digits, operating margin grinding from 6% to low-8s."),
 scen("Bull",{"wacc":0.115,"terminal_growth":0.035,"fcf_multiplier":1.3},0.10,
   "Low odds. Requires CLS to become a structurally higher-margin design partner (HPS/ODM mix) and to add multiple anchor hyperscalers.",
   "Celestica re-rates as a design-led AI infrastructure partner rather than a contract assembler; margins and growth beat the base path."),
]
OUT["CLS"]=dcf_inputs("CLS",371.86,0.114973,0.4,
  "Celestica produces positive and growing free cash flow with an AI-server-driven revenue ramp, so an FCFF DCF is appropriate. The key tension is that an EMS cost structure caps margins, so an EV/EBITDA cross-check against manufacturing-services peers disciplines the rich post-run multiple.",
  "electronics-manufacturing",0.115,
  {"rf":0.043,"beta":1.60,"erp":0.05,"debt_weight":0.10,"cost_of_debt_after_tax":0.05},
  "Ke = 4.3% Rf + 1.60 beta x 5.0% ERP = 12.3%. High beta for EMS cyclicality, thin margins and customer concentration. Low net debt keeps WACC near Ke at ~11.5%.",
  0.03,"3.0% terminal: contract manufacturing is a GDP-plus business at best once the AI build matures; no durable pricing power to justify more.",
  rows,cc,sc,
  "40% Base + 30% Bear + 10% Bull + 20% EV/EBITDA cross-check.",
  "Bear gets a full 30% because an EMS at ~4x sales is historically extreme and customer concentration plus capex cyclicality are concrete near-term risks. Base 40% for continued AI program wins. Bull only 10% because a durable margin re-rate is hard for a contract assembler. Cross-check 20% anchors against manufacturing-services norms.",
  "11.5% is upper-band for the equity risk in a thin-margin, concentrated EMS.")

# ============================== ARM ==============================
rows=[
 proj(2026,4.9,22.0,0.30,0.03,0.03,0.01,note="FY26E (Mar) +22%: royalty inflection as Armv9 (higher royalty rate) and Compute Subsystems (CSS) penetrate smartphone and data-center sockets; licensing strong on AI design starts."),
 proj(2027,6.0,22.0,0.33,0.03,0.03,0.01,note="+22%: data-center CPU traction (Grace, hyperscaler custom Arm silicon) and CSS royalties compound; operating margin expands on royalty mix."),
 proj(2028,7.2,20.0,0.36,0.03,0.025,0.01,note="+20%: Armv9 royalty per chip keeps rising; automotive and IoT add breadth."),
 proj(2029,8.5,18.0,0.38,0.03,0.025,0.008,note="+18%: royalty base broadens across compute; margins toward high-30s."),
 proj(2030,9.9,16.0,0.40,0.03,0.02,0.008,note="+16%: durable IP-royalty compounding; ~40% operating margin."),
 proj(2031,11.2,13.0,0.42,0.03,0.02,0.006,note="+13%: growth moderates off a larger royalty base."),
 proj(2032,12.4,11.0,0.43,0.03,0.02,0.006,note="+11%: maturing, low-40s operating margin."),
 proj(2033,13.5,9.0,0.44,0.03,0.018,0.005,note="+9%: approaching steady-state IP franchise economics."),
]
cc={"name":"Multiple","category":"relative",
    "reasoning":"ARM is an IP-licensing franchise with software-like margins, so an EV/EBITDA (or P/E) cross-check against premium IP and design-software peers is the relevant relative anchor. Even a rich multiple lands below the extreme spot valuation.",
    "inputs":{"multiple_type":"EV/EBITDA","peer_median_multiple":45.0,"fy_estimate":1.6,
              "peers_used":["SNPS","CDNS","NVDA","ADI","KLAC"],
              "reasoning":"45x applied to FY26E EBITDA of ~$1.6B. A premium IP multiple in line with EDA leaders; still implies a value below the ~70x-sales spot."}}
sc=[
 scen("Bear",{"wacc":0.125,"terminal_growth":0.03,"fcf_multiplier":0.7},0.25,
   "A real quarter-weight. At ~70x sales the stock prices flawless royalty inflection; RISC-V encroachment, a smartphone-unit air pocket, or licensing lumpiness each puncture the multiple.",
   "Royalty-rate gains disappoint, RISC-V takes share at the low end, and the IP premium compresses."),
 scen("Base",{},0.45,
   "Central case. Armv9 and CSS lift royalty per chip and data-center adoption grows, but even this constructive path sits below the current price.",
   "Royalty inflection plays out as modeled, ~20% revenue CAGR with operating margin expanding toward 40%."),
 scen("Bull",{"wacc":0.105,"terminal_growth":0.045,"fcf_multiplier":1.4},0.10,
   "Lower odds. Requires Arm to capture a large data-center CPU share, monetize AI design starts aggressively, and push CSS/royalty rates above plan.",
   "Arm becomes the default compute-IP platform across mobile, data center and AI edge; royalties and margins beat materially."),
]
OUT["ARM"]=dcf_inputs("ARM",324.86,1.064054,-2.7,
  "Arm is a high-margin IP-licensing franchise with strong and growing free cash flow, so an FCFF DCF on its royalty-and-licensing model is appropriate. Because the stock trades at an extreme sales multiple, an EV/EBITDA cross-check against premium IP/EDA peers disciplines the target.",
  "semiconductors-ip",0.11,
  {"rf":0.043,"beta":1.40,"erp":0.05,"debt_weight":0.0,"cost_of_debt_after_tax":0.0},
  "Ke = 4.3% Rf + 1.40 beta x 5.0% ERP = 11.3%. Net-cash balance sheet means WACC equals Ke at ~11.0%. Beta reflects high-multiple volatility offset by the annuity-like royalty base.",
  0.04,"4.0% terminal: Arm's royalty base compounds with the entire compute market and Armv9 lifts royalty per chip, supporting an above-GDP terminal rate for a durable IP monopoly-adjacent franchise.",
  rows,cc,sc,
  "45% Base + 25% Bear + 10% Bull + 20% EV/EBITDA cross-check.",
  "Bear 25% because a ~70x-sales valuation is exquisitely sensitive to any royalty or smartphone-unit disappointment and to RISC-V. Base 45% for the royalty inflection playing out. Bull 10% for a data-center share grab. Cross-check 20% anchors against premium IP/EDA multiples.",
  "11.0% equals Ke on a net-cash balance sheet; mid-band for a high-quality IP franchise.")

# ============================== NOW ==============================
rows=[
 proj(2026,15.6,20.0,0.22,0.03,0.02,wc=-0.02,note="FY26E +20%: subscription revenue compounds on platform expansion (ITSM, ITOM, security, and AI 'Now Assist' upsell). EBIT margin uses a normalized cash-earnings proxy above GAAP given deferred-revenue and SBC dynamics."),
 proj(2027,18.7,20.0,0.24,0.03,0.02,wc=-0.02,note="+20%: Now Assist (genAI) ACV ramps as a new pricing lever; net revenue retention stays ~115%+."),
 proj(2028,22.1,18.0,0.26,0.03,0.02,wc=-0.018,note="+18%: enterprise platform standardization and AI seats lift ARPU; operating leverage builds."),
 proj(2029,25.6,16.0,0.27,0.03,0.018,wc=-0.016,note="+16%: durable mid-teens growth as the install base matures; FCF margin in the low-30s."),
 proj(2030,29.2,14.0,0.28,0.03,0.018,wc=-0.014,note="+14%: growth normalizes; platform breadth sustains pricing power."),
 proj(2031,32.7,12.0,0.29,0.03,0.015,wc=-0.012,note="+12%: maturing growth, high-20s EBIT margin."),
 proj(2032,36.0,10.0,0.30,0.03,0.015,wc=-0.01,note="+10%: approaching steady-state SaaS economics."),
 proj(2033,39.2,9.0,0.30,0.03,0.015,wc=-0.01,note="+9%: durable franchise, ~30% normalized margin."),
]
cc={"name":"Multiple","category":"relative",
    "reasoning":"EV/FCF (proxied via EV/EBITDA on a normalized basis) cross-check against high-quality enterprise-SaaS compounders, the relevant peer cohort for a 20% grower with 30%+ FCF margins.",
    "inputs":{"multiple_type":"EV/EBITDA","peer_median_multiple":28.0,"fy_estimate":4.2,
              "peers_used":["CRM","WDAY","ADBE","SNOW","INTU"],
              "reasoning":"28x applied to FY26E normalized EBITDA of ~$4.2B. In line with premium SaaS compounders; lands near spot, reflecting that NOW is richly but not absurdly valued versus its growth-plus-margin profile."}}
sc=[
 scen("Bear",{"wacc":0.115,"terminal_growth":0.03,"fcf_multiplier":0.78},0.20,
   "A fifth-weight. The main risks are a macro-driven enterprise IT-budget slowdown, genAI displacing some workflow seats, and a high multiple that de-rates on any growth deceleration below 18%.",
   "Seat-based growth slows as AI agents compress headcount-linked licensing, and the premium multiple compresses."),
 scen("Base",{},0.55,
   "Central case, high conviction. ServiceNow has ~98% renewal, 115%+ net retention and a credible AI-monetization lever; 20% growth with expanding FCF margin is the most likely path.",
   "Platform expansion and Now Assist upsell sustain ~20% growth with FCF margin grinding into the low-30s."),
 scen("Bull",{"wacc":0.095,"terminal_growth":0.045,"fcf_multiplier":1.25},0.05,
   "Modest odds. Requires Now Assist genAI ACV to become a large, fast-growing second engine and net retention to re-accelerate.",
   "AI agents become a major new revenue line; growth re-accelerates and the platform compounds above plan."),
]
OUT["NOW"]=dcf_inputs("NOW",106.97,1.031308,-6.0,
  "ServiceNow is a high-margin, high-retention enterprise-software compounder with strong free cash flow, so an FCFF DCF on its subscription model is the right primary method. Because GAAP EBIT understates cash earnings (deferred revenue, SBC), the EBIT-margin inputs use a normalized cash-earnings proxy with that reasoning stated. An EV/EBITDA cross-check against SaaS peers anchors the multiple.",
  "software-saas",0.10,
  {"rf":0.043,"beta":1.20,"erp":0.05,"debt_weight":0.0,"cost_of_debt_after_tax":0.0},
  "Ke = 4.3% Rf + 1.20 beta x 5.0% ERP = 10.3%. Beta moderate for a durable subscription model with high recurring revenue. Net-cash balance sheet sets WACC ~ Ke at 10.0%.",
  0.04,"4.0% terminal: a sticky enterprise platform with 98% renewal and a broadening AI monetization lever supports an above-GDP terminal rate.",
  rows,cc,sc,
  "55% Base + 20% Bear + 5% Bull + 20% EV/EBITDA cross-check.",
  "Base gets a high 55% because the subscription model's visibility (98% renewal, 115%+ NRR) makes the central path unusually reliable. Bear 20% for an enterprise-budget/AI-seat-displacement scenario. Bull only 5% because much of the AI optionality is already in the price. Cross-check 20% anchors against premium SaaS multiples.",
  "10.0% equals Ke on net cash; low-mid band, fitting a high-quality recurring-revenue platform.")

# ============================== FN ==============================
rows=[
 proj(2026,4.0,18.0,0.125,0.02,0.02,0.02,note="FY26E (Jun) +18%: datacom optical-module assembly for AI (800G/1.6T) drives the ramp; Fabrinet is the contract manufacturer behind the leading transceiver and silicon-photonics programs."),
 proj(2027,4.66,16.5,0.128,0.02,0.02,0.018,note="+16.5%: 1.6T volume scales and new optical-engine programs onshore; modest margin lift from mix and scale."),
 proj(2028,5.31,14.0,0.131,0.02,0.018,0.016,note="+14%: AI optical content keeps compounding; margins inch up on automation."),
 proj(2029,5.95,12.0,0.134,0.02,0.018,0.014,note="+12%: growth normalizes; FN remains a key Western/Thai assembly node."),
 proj(2030,6.55,10.0,0.136,0.02,0.016,0.012,note="+10%: steady compounding on a larger base."),
 proj(2031,7.07,8.0,0.138,0.02,0.016,0.01,note="+8%: deceleration continues."),
 proj(2032,7.57,7.0,0.139,0.02,0.015,0.01,note="+7%: maturing growth."),
 proj(2033,8.0,5.7,0.14,0.02,0.015,0.008,note="+5.7%: approaching steady state, ~14% operating margin franchise."),
]
cc={"name":"Multiple","category":"relative",
    "reasoning":"EV/EBITDA cross-check against optical-component and contract-manufacturing peers. Even a generous multiple for an asset-light optical assembler lands below the post-run share price.",
    "inputs":{"multiple_type":"EV/EBITDA","peer_median_multiple":15.0,"fy_estimate":0.58,
              "peers_used":["COHR","LITE","SANM","FLEX","AAOI"],
              "reasoning":"15x applied to FY26E EBITDA of ~$0.58B (≈14.5% margin on $4.0B). Generous for a contract optical assembler; still implies a value below spot."}}
sc=[
 scen("Bear",{"wacc":0.125,"terminal_growth":0.02,"fcf_multiplier":0.72},0.25,
   "A full quarter-weight. FN is customer-concentrated (a few large transceiver/networking OEMs), margins are thin, and the shares have ~2.5x'd off the low. A single program shift or a move to in-house/CPO assembly hurts.",
   "Optical-module volumes digest, a key customer in-sources or shifts to co-packaged optics, and the multiple compresses."),
 scen("Base",{},0.45,
   "Central case. FN keeps winning AI optical assembly and margins inch up, but the valuation already prices a long, smooth datacom ramp.",
   "Datacom-led growth decelerating from 18% to mid-single-digits, operating margin grinding from 12.5% to ~14%."),
 scen("Bull",{"wacc":0.105,"terminal_growth":0.035,"fcf_multiplier":1.3},0.10,
   "Lower odds. Requires 1.6T and co-packaged-optics assembly to flow to FN at scale and margins to expand above plan.",
   "Fabrinet becomes the default high-complexity optical-engine assembler; revenue and margins beat the base path."),
]
OUT["FN"]=dcf_inputs("FN",586.00,0.035830,-0.9,
  "Fabrinet generates steady, positive free cash flow as the contract assembler behind the leading AI optical-module programs, so an FCFF DCF is appropriate. Because it is a thin-margin assembler trading at a rich post-run multiple, an EV/EBITDA cross-check against optical and manufacturing peers disciplines the target.",
  "optical-manufacturing",0.108,
  {"rf":0.043,"beta":1.30,"erp":0.05,"debt_weight":0.0,"cost_of_debt_after_tax":0.0},
  "Ke = 4.3% Rf + 1.30 beta x 5.0% ERP = 10.8%. Net-cash balance sheet sets WACC = Ke at 10.8%. Beta reflects customer concentration and datacom cyclicality offset by a debt-free balance sheet.",
  0.03,"3.0% terminal: optical assembly is a GDP-plus business once the AI build matures; thin margins and customer concentration cap the durable growth rate.",
  rows,cc,sc,
  "45% Base + 25% Bear + 10% Bull + 20% EV/EBITDA cross-check.",
  "Bear 25% because customer concentration, thin margins and a ~2.5x run leave little room for error, and co-packaged optics is a structural overhang. Base 45% for the continued AI optical ramp. Bull 10% for a CPO/1.6T assembly win. Cross-check 20% anchors against optical/manufacturing multiples.",
  "10.8% equals Ke on net cash; mid-band for a concentrated, thin-margin assembler.")

for t,d in OUT.items():
    p=f"output/{t}/{t}_inputs.json"
    json.dump(d, open(p,"w"), indent=2)
    print("wrote", p, "| horizon", len(d["primary_method"]["inputs"]["fcf_projections"]))
