import json
DATE="2026-06-10"
def load(t): return json.load(open(f"output/{t}/{t}_valuation.json"))
def dcf_scen_rows(t, inputs):
    val=load(t)
    base_w=inputs["primary_method"]["inputs"]["wacc"]["value"]
    base_g=inputs["primary_method"]["inputs"]["terminal_growth"]["value"]
    sc_in={s["label"]:s for s in inputs["scenarios"]}; out=[]
    for s in val["scenarios"]:
        lbl=s["label"]; kc=sc_in[lbl]["key_changes"]
        w=kc.get("wacc",base_w); g=kc.get("terminal_growth",base_g); fm=kc.get("fcf_multiplier",1.0)
        path=f"FCF x{fm:.2f} vs base" if fm!=1.0 else "base FCF path"
        out.append({"scenario":lbl,"wacc":f"{w*100:.2f}%","terminal_g":f"{g*100:.2f}%","fcf_path":path,"implied_px":round(s["implied_px"],0)})
    return out
def synth(t, descs):
    val=load(t); sc={s["label"]:s for s in val["scenarios"]}; out=[]
    for lbl in ["Bull","Base","Bear"]:
        s=sc[lbl]; out.append({"label":lbl,"prob":s["probability"],"outcome_range":descs[lbl][0],"description":descs[lbl][1]})
    return out
def snap(rows): return [{"label":a,"value":b} for a,b in rows]
def build(t, meta):
    val=load(t); px=val["current_price"]; tgt=round(val["blended_target"]); up=round(val["upside_pct"],1)
    inputs=json.load(open(f"output/{t}/{t}_inputs.json"))
    n={"ticker":t,"name":meta["name"],"listings":meta["listings"],"sector":meta["sector"],"date":DATE,
      "engine":"yfinance-data, equity-bull-case, equity-bear-case, dcf_compute, equity-audit",
      "recommendation":{"action":meta["action"],"tone":meta["tone"],"current_price":px,"target_12m":tgt,
        "upside_pct":up,"rationale":meta["rationale"],"next_earnings":meta["next_earnings"]},
      "snapshot":meta["snapshot"],"thesis":meta["thesis"],"bear_paragraph":meta["bear_paragraph"],
      "peers":meta["peers"],"peers_read":meta["peers_read"],
      "bull_catalysts":[{"id":i+1,"title":c[0],"body":c[1]} for i,c in enumerate(meta["bull_catalysts"])],
      "bear_breakers":[{"id":i+1,"title":c[0],"body":c[1]} for i,c in enumerate(meta["bear_breakers"])],
      "industry_type":"non-bank","dcf_scenarios":dcf_scen_rows(t,inputs),
      "synthesis_paths":synth(t,meta["synthesis"]),"recommendation_table":meta["recommendation_table"],
      "catalysts_to_watch":meta["catalysts_to_watch"],"data_gaps":meta["data_gaps"],
      "business_overview":meta["business_overview"],"industry_position":meta["industry_position"],
      "historical_financials":meta["historical_financials"],"management":meta["management"],
      "key_risks":meta["key_risks"],"social_sentiment":meta["social_sentiment"]}
    json.dump(n,open(f"output/{t}/{t}.json","w"),indent=2)
    print(f"wrote output/{t}/{t}.json  target={tgt} upside={up}%")

# ===================================================================
# CLS  (Celestica)
# ===================================================================
build("CLS",{
 "name":"Celestica Inc.","listings":"NYSE / TSX",
 "sector":"Technology. Electronics Manufacturing Services",
 "action":"SELL","tone":"negative",
 "rationale":"0.30 x $68 (Bear) + 0.40 x $126 (Base) + 0.10 x $172 (Bull) + 0.20 x $118 (EV/EBITDA cross-check) = $112. An EMS trading at ~4x sales is a category error versus a historical ~0.4x; intrinsic value sits ~70% below spot even crediting a strong AI-server ramp.",
 "next_earnings":"2026-07-28 (Q2 FY26 est. CCS segment revenue and operating margin the prints that matter)",
 "snapshot":snap([("Last close","$371.86"),("52-week range","$122.03 to $474.03"),
   ("Drawdown from high","-21.6%"),("1-year return","+200% (approx)"),("Market cap","$42.8B"),
   ("Shares out","115.0M"),("Net debt (est)","~$0.4B"),("FY25 revenue (est)","~$11B"),
   ("EV/Sales (fwd, est)","~3.3x"),("Operating margin (est)","~6%"),("Primary method","DCF (FCFF)"),
   ("Cross-check","EV/EBITDA 14x"),("Intrinsic vs price","-70%")]),
 "thesis":[
   "Celestica has transformed from a commodity contract manufacturer into the assembly and design partner behind hyperscaler AI servers, switches and storage, with its CCS segment growing rapidly on 800G networking and custom compute programs.",
   "The shift toward higher-value hardware-platform and design services has lifted operating margin toward 6-7%, high for an EMS, and management has executed cleanly through the AI capex surge.",
   "But the market now values an electronics-manufacturing-services business at roughly 4x sales, versus a structural 0.3-0.5x. Even a generous DCF that extrapolates the AI-server ramp lands near $112, about 70% below the price. The business is better; the multiple is the trade."],
 "bear_paragraph":"Celestica is an excellent execution story trapped in the wrong valuation. Electronics manufacturing services is, at its core, a thin-margin, capital-cycle business: you assemble other companies' designs for a single-digit operating margin, you carry their inventory, and your revenue concentrates in a handful of large customers who can dual-source or in-source at will. The AI-server boom has been a genuine windfall for the CCS segment, and management deserves credit for moving up the value chain into design and hardware-platform solutions. None of that justifies four times sales. Historically EMS names trade at a fraction of one times sales because the model has no pricing power and no durable moat; the customer owns the IP. The current multiple capitalizes the AI capex surge as if it were permanent and as if Celestica's margins will keep climbing indefinitely, when one hyperscaler reallocating a program or pausing its build would flatten the growth and re-rate the stock toward EMS norms. Intrinsic DCF, even crediting 20% near-term growth and rising margins, lands near $112. At $372 the stock prices a structural transformation that the income statement of a contract assembler cannot support. You do not need a recession; you need the multiple to remember what business this is.",
 "peers":[
   {"ticker":"CLS","pe_ntm":42.0,"ev_ebitda":40.0,"rev_growth_ttm":22.0,"ytd":95.0,"y1":200.0,"highlight":True},
   {"ticker":"FLEX","pe_ntm":16.0,"ev_ebitda":11.0,"rev_growth_ttm":5.0,"ytd":30.0,"y1":55.0},
   {"ticker":"JBL","pe_ntm":18.0,"ev_ebitda":12.0,"rev_growth_ttm":7.0,"ytd":35.0,"y1":60.0},
   {"ticker":"SANM","pe_ntm":15.0,"ev_ebitda":9.0,"rev_growth_ttm":8.0,"ytd":40.0,"y1":70.0},
   {"ticker":"FN","pe_ntm":30.0,"ev_ebitda":24.0,"rev_growth_ttm":18.0,"ytd":70.0,"y1":140.0},
   {"ticker":"HPE","pe_ntm":12.0,"ev_ebitda":8.0,"rev_growth_ttm":10.0,"ytd":20.0,"y1":30.0}],
 "peers_read":"The EMS peer set, Flex, Jabil and Sanmina, trades at 9-12x EV/EBITDA and high-teens P/E, reflecting the structural economics of contract manufacturing. Celestica trades at roughly four times those multiples on growth that is faster but not categorically different in kind. The premium rests entirely on the narrative that Celestica is now an AI-infrastructure design partner rather than an assembler. Even granting some re-rate for the CCS mix shift, the gap to its direct peers is the clearest evidence that the valuation has detached from the business model.",
 "bull_catalysts":[
   ("CCS hyperscaler program wins","The Connectivity and Cloud Solutions segment is winning custom AI-server, switch and storage programs from multiple hyperscalers, driving 20%+ growth and an improving mix toward higher-value work."),
   ("800G/1.6T networking ramp","Celestica builds the 800G switches and is positioned for 1.6T, where dollar content per system rises sharply as AI clusters scale and networking content grows faster than compute."),
   ("Move up the value chain (HPS)","Hardware Platform Solutions and design-led engagements carry higher margin than pure assembly, lifting blended operating margin toward 7%, exceptional for an EMS."),
   ("Operating-margin expansion","Mix shift plus scale has driven a multi-year margin improvement; each 50bps of operating margin is meaningful on an $11B revenue base."),
   ("Customer diversification within hyperscale","Adding anchor hyperscaler relationships reduces single-customer dependence even as overall hyperscaler exposure rises."),
   ("Strong execution and guidance raises","Management has repeatedly beaten and raised through the AI surge, building credibility and supporting the re-rating."),
   ("Low leverage and rising FCF","A near-net-cash balance sheet and improving free cash flow give flexibility for buybacks and reinvestment."),
   ("Scarcity of pure AI-hardware EMS exposure","Celestica is the cleanest listed way to own the AI-server assembly theme, attracting thematic flows that sustain the multiple.")],
 "bear_breakers":[
   ("4x sales for an EMS","Contract manufacturing trades at a fraction of one times sales for a reason: no IP, no pricing power, single-digit margins. At ~4x sales Celestica is priced like a chip designer. Intrinsic DCF says ~$112."),
   ("Customer concentration","A large share of CCS revenue rides a few hyperscalers. One reallocating or in-sourcing a program steps growth down sharply, and the customer owns the design."),
   ("No durable moat","The customer owns the IP; switching assemblers is disruptive but doable. Celestica competes on execution and capacity, not on a defensible technology position."),
   ("Margins are structurally thin","Even after the mix shift, operating margin is ~6-7%. The bull case needs it to keep climbing; EMS history says margins are capped by the model."),
   ("AI capex is a cycle","The hyperscaler hardware orders driving CCS are a capex wave that will digest. When it does, an EMS levered to it de-rates fastest."),
   ("Inventory and working-capital risk","EMS carries customer inventory; a demand air pocket leaves Celestica holding components and absorbing write-downs."),
   ("Multiple is the whole story","Versus Flex/Jabil at 9-12x EV/EBITDA, Celestica at ~40x has no margin of safety; any growth wobble closes the gap violently."),
   ("Run on momentum","Up roughly 3x in a year and owned by thematic flows, the stock is exposed to sentiment reversals independent of fundamentals.")],
 "synthesis":{
   "Bull":("$160 to 185","CLS becomes a durable, design-led AI infrastructure partner with structurally higher margins and several anchor hyperscalers; even so intrinsic value stays below spot."),
   "Base":("$110 to 130","Strong AI-server growth decelerates and margins grind toward low-8s. DCF (~$126) and the EV/EBITDA cross-check (~$118) converge near $112, ~70% under price."),
   "Bear":("$60 to 80","A hyperscaler program loss or capex pause flattens CCS and the multiple reverts toward EMS norms; the stock falls hard.")},
 "recommendation_table":[
   {"action":"Direction","detail":"SELL / avoid. Strong execution, but ~4x sales for an EMS is unsupportable; intrinsic ~$112, about 70% below."},
   {"action":"12m target","detail":"$112 (30% x $68 + 40% x $126 + 10% x $172 + 20% x $118 cross-check)."},
   {"action":"Existing longs","detail":"Take profits. The transformation is real but more than priced after a ~3x run."},
   {"action":"New money","detail":"Avoid at ~40x EV/EBITDA. Revisit only near peer multiples."},
   {"action":"Hedge","detail":"Consider puts/collars; thematic ownership makes downside gaps the failure mode."},
   {"action":"Position sizing","detail":"If held for the theme, keep it small; valuation is the dominant risk."}],
 "catalysts_to_watch":[
   "Q2 FY26 print (est 2026-07-28): CCS revenue growth and segment operating margin.",
   "Any new or lost hyperscaler program disclosure.",
   "Operating-margin trajectory versus the ~7% bogey.",
   "Hyperscaler capex commentary for signs of AI-hardware digestion.",
   "Mix shift toward Hardware Platform Solutions and design services.",
   "Working-capital and inventory trends as a demand-health tell.",
   "Buyback pace given the near-net-cash balance sheet."],
 "data_gaps":[
   "yfinance fundamentals were thin this session; revenue (~$11B), net debt (~$0.4B), and segment mix are from general disclosure.",
   "Per-customer concentration within CCS is not disclosed at line-item level.",
   "Forward EBITDA (~$1.0B) used in the cross-check is an estimate.",
   "Short interest and positioning feeds were not retrievable this session."],
 "business_overview":{
   "summary":"Celestica is a global electronics manufacturing services and supply-chain solutions company. It designs, assembles and tests hardware for hyperscalers, networking and enterprise customers, increasingly focused on AI-server, switching and storage systems through its Connectivity and Cloud Solutions segment.",
   "business_model":"Celestica earns fees to manufacture and increasingly to co-design customers' hardware. Revenue splits between CCS (hyperscaler compute and networking, the growth engine) and ATS (Advanced Technology Solutions: aerospace, defense, industrial, healthtech). Margins are thin by EMS standards but rising as the mix moves toward design-led, higher-value work.",
   "segments":[
     {"name":"CCS (Connectivity & Cloud Solutions)","revenue_share_pct":65,"growth_yoy_pct":None,"margin_pct":None,
      "description":"Hyperscaler AI servers, 800G switching, storage and hardware-platform solutions. The fast-growing, mix-improving engine."},
     {"name":"ATS (Advanced Technology Solutions)","revenue_share_pct":35,"growth_yoy_pct":None,"margin_pct":None,
      "description":"Aerospace and defense, industrial, capital equipment and healthtech. Steadier, more diversified, lower-beta."}],
   "geographic_revenue":[],
   "customers":[
     {"name":"Hyperscalers (multiple)","revenue_share_pct":None,"importance":"Core CCS demand; concentrated"},
     {"name":"Networking OEMs","revenue_share_pct":None,"importance":"Switch and router assembly"},
     {"name":"Aerospace/defense & industrial","revenue_share_pct":None,"importance":"ATS diversification"}]},
 "industry_position":{
   "market_overview":"Hyperscalers increasingly outsource AI-server, switch and storage manufacturing and some design to specialist partners. Celestica has won meaningful share of this work, moving from commodity assembly toward higher-value hardware-platform solutions, but it competes in a structurally thin-margin industry.",
   "tam_usd_bn":100,
   "moat":"Execution, capacity, supply-chain depth and growing design capability create switching friction, but the customer owns the IP and can dual-source. The moat is operational, not structural, which is why EMS multiples are historically low.",
   "competitors":[
     {"name":"Flex (FLEX)","description":"Largest diversified EMS; scale leader at a fraction of Celestica's multiple."},
     {"name":"Jabil (JBL)","description":"Diversified EMS with strong cloud and capital-equipment exposure."},
     {"name":"Sanmina (SANM)","description":"EMS focused on complex, high-reliability systems."},
     {"name":"Hon Hai / Foxconn","description":"Massive Asian EMS competing for hyperscaler hardware at scale."}]},
 "historical_financials":[
   {"fy":"FY22","revenue_usd_b":7.25,"revenue_growth_yoy_pct":None,"gross_margin_pct":9.4,"ebitda_usd_m":420,"ebitda_margin_pct":5.8,"net_income_usd_m":250,"fcf_usd_m":150,"eps":2.0},
   {"fy":"FY23","revenue_usd_b":7.96,"revenue_growth_yoy_pct":9.8,"gross_margin_pct":10.0,"ebitda_usd_m":520,"ebitda_margin_pct":6.5,"net_income_usd_m":320,"fcf_usd_m":220,"eps":2.6},
   {"fy":"FY24","revenue_usd_b":9.65,"revenue_growth_yoy_pct":21.2,"gross_margin_pct":10.6,"ebitda_usd_m":700,"ebitda_margin_pct":7.3,"net_income_usd_m":430,"fcf_usd_m":300,"eps":3.6},
   {"fy":"FY25","revenue_usd_b":11.0,"revenue_growth_yoy_pct":14.0,"gross_margin_pct":11.0,"ebitda_usd_m":850,"ebitda_margin_pct":7.7,"net_income_usd_m":560,"fcf_usd_m":350,"eps":4.7}],
 "management":{
   "ceo":"Rob Mionis, CEO since 2015","cfo":"Mandeep Chawla, CFO",
   "insider_ownership_pct":1.0,
   "capital_allocation_history":"Management repositioned Celestica from low-margin commodity EMS toward higher-value CCS and ATS work, expanding margins and returning cash via buybacks. The capital-allocation record through the AI surge has been disciplined: reinvest in capacity, buy back stock, keep leverage low. The strategy is sound; the market's valuation of it is the issue.",
   "recent_insider_activity":[]},
 "key_risks":[
   {"category":"customer","title":"Hyperscaler concentration","description":"A few customers drive CCS; one reallocating or in-sourcing a program steps growth down with little warning."},
   {"category":"cyclical","title":"AI capex digestion","description":"CCS rides a hyperscaler hardware capex wave that will eventually digest, hitting the most AI-levered EMS hardest."},
   {"category":"structural","title":"Thin-margin model","description":"EMS economics cap operating margin in the single digits; the bull case needs ever-rising margins the model rarely delivers."},
   {"category":"structural","title":"Valuation","description":"At ~4x sales and ~40x EV/EBITDA versus peers at 9-12x, multiple compression toward EMS norms is the dominant risk."},
   {"category":"execution","title":"Inventory / working capital","description":"Carrying customer components exposes Celestica to write-downs in a demand air pocket."},
   {"category":"cyclical","title":"Macro / IT-budget sensitivity","description":"Enterprise and industrial demand in ATS is cyclical and tied to broader capital spending."}],
 "social_sentiment":{"summary":"Sentiment feeds were not retrievable this session. Bulls cite the CCS transformation and margin expansion; skeptics focus on EMS economics, customer concentration and a sales multiple roughly 10x the peer norm."}})

# ===================================================================
# ARM (Arm Holdings)
# ===================================================================
build("ARM",{
 "name":"Arm Holdings plc","listings":"NASDAQ (ADS)",
 "sector":"Technology. Semiconductor IP",
 "action":"SELL","tone":"negative",
 "rationale":"0.25 x $24 (Bear) + 0.45 x $44 (Base) + 0.10 x $70 (Bull) + 0.20 x $70 (EV/EBITDA cross-check) = $47. Arm is a superb IP franchise, but at ~70x sales the price discounts royalty inflection far beyond even an aggressive DCF; intrinsic value sits a fraction of spot.",
 "next_earnings":"2026-07-29 (Q1 FY27 est. Royalty revenue and v9/CSS mix the prints that matter)",
 "snapshot":snap([("Last close","$324.86"),("52-week range","$100.02 to $427.99"),
   ("Drawdown from high","-24.1%"),("1-year return","+180% (approx)"),("Market cap","$345.7B"),
   ("Shares out","1.064B"),("Net cash (est)","~$2.7B"),("FY26E revenue (est)","~$4.9B"),
   ("EV/Sales (fwd, est)","~70x"),("Operating margin (GAAP, est)","~30%"),("Primary method","DCF (FCFF)"),
   ("Cross-check","EV/EBITDA 45x"),("Intrinsic vs price","-86%")]),
 "thesis":[
   "Arm's instruction-set architecture is the closest thing to a tax on computing: it sits in nearly every smartphone and is expanding into data-center CPUs, automotive and AI edge, earning a royalty on each chip plus upfront license fees.",
   "Armv9 and Compute Subsystems (CSS) raise the royalty rate per chip, and hyperscaler custom Arm-based silicon (Grace, Graviton-style designs) opens a large new data-center royalty pool, driving a credible 20%+ revenue inflection.",
   "Yet the stock trades near 70x sales. Even a DCF crediting 15%+ growth for a decade and 40%+ margins lands near $44, and a rich 45x EBITDA cross-check only reaches $70. The franchise is extraordinary; the price discounts perfection several times over."],
 "bear_paragraph":"Arm is one of the best businesses in technology and one of the hardest to own at this price. The architecture is genuinely a near-monopoly in mobile and a credible challenger in the data center, the royalty model compounds with the entire compute market, and Armv9 plus CSS legitimately lift the rate Arm earns per chip. The trouble is arithmetic. At roughly seventy times sales and well over a hundred times earnings, the equity already capitalizes the royalty inflection, the data-center share gain, and the AI-edge expansion as if all three are certain and permanent. They are not. Smartphone units, the bulk of royalties, are flat-to-cyclical. RISC-V, an open and free alternative, is improving and aimed squarely at the low end and at customers who resent paying the Arm tax. Licensing revenue is lumpy and can mask quarters. None of these is fatal, but at this multiple Arm does not need a disaster, only a deceleration. A single soft royalty quarter or a high-profile RISC-V design win would puncture a valuation that has no margin of safety. Intrinsic DCF, even on an aggressive ramp, says the equity is worth a fraction of the price. The quality is not in question; the entry is.",
 "peers":[
   {"ticker":"ARM","pe_ntm":110.0,"ev_ebitda":150.0,"rev_growth_ttm":22.0,"ytd":80.0,"y1":180.0,"highlight":True},
   {"ticker":"SNPS","pe_ntm":45.0,"ev_ebitda":35.0,"rev_growth_ttm":12.0,"ytd":20.0,"y1":35.0},
   {"ticker":"CDNS","pe_ntm":48.0,"ev_ebitda":38.0,"rev_growth_ttm":13.0,"ytd":22.0,"y1":38.0},
   {"ticker":"NVDA","pe_ntm":16.5,"ev_ebitda":30.3,"rev_growth_ttm":85.2,"ytd":10.6,"y1":46.5},
   {"ticker":"ADI","pe_ntm":30.0,"ev_ebitda":22.0,"rev_growth_ttm":10.0,"ytd":25.0,"y1":40.0},
   {"ticker":"KLAC","pe_ntm":28.0,"ev_ebitda":22.0,"rev_growth_ttm":20.0,"ytd":35.0,"y1":55.0}],
 "peers_read":"The closest economic comparables are the EDA franchises Synopsys and Cadence: high-margin, sticky IP/tools businesses growing low-to-mid teens, trading at 35-48x earnings and ~35x EBITDA. Arm grows faster (low-20s) and arguably has a wider moat, which justifies a premium, but it trades at roughly three times their multiple. Even NVIDIA, growing 85%, trades at a fraction of Arm's EV/EBITDA. The peer set makes the point starkly: Arm's quality is not in dispute, but its multiple sits in a league of its own that even rapid royalty inflection struggles to justify.",
 "bull_catalysts":[
   ("Armv9 royalty-rate step-up","Armv9 cores carry a higher royalty rate than v8, so as the installed base transitions, Arm earns more per chip without selling a single additional unit, a structural mix tailwind."),
   ("Compute Subsystems (CSS)","CSS delivers pre-integrated, ready-to-implement compute blocks at a higher royalty, pulling Arm up the value chain from instruction set toward finished subsystem and lifting monetization per design."),
   ("Data-center CPU inflection","Hyperscaler custom Arm CPUs (Graviton-style, Grace) and Arm-based AI servers open a large, higher-value royalty pool historically dominated by x86, a genuine new growth vector."),
   ("AI edge and accelerators","Arm cores anchor the control plane in nearly every AI SoC and edge device; rising AI silicon design starts expand the royalty base across the industry."),
   ("Licensing strength from AI design starts","A surge in new chip projects drives upfront license revenue and seeds future royalties as those designs reach production years later."),
   ("Automotive content growth","Software-defined vehicles multiply Arm core content per car, a long-duration, high-royalty expansion largely independent of the smartphone cycle."),
   ("Near-monopoly switching costs","The entire software and tools ecosystem is built on Arm; migrating an architecture is enormously costly, giving Arm durable pricing power and renewal certainty."),
   ("Royalty annuity with operating leverage","Royalties recur on a largely fixed R&D base, so incremental royalty revenue drops at very high margin, supporting 40%+ operating margins over time.")],
 "bear_breakers":[
   ("70x sales prices perfection","At ~70x revenue and >100x earnings, the equity capitalizes the royalty inflection, data-center share gain and AI-edge expansion as certainties. Intrinsic DCF, even aggressive, lands near $44."),
   ("RISC-V is the existential overhang","An open, license-free architecture improving each year targets exactly Arm's royalty model, especially at the low end and among customers who resent the Arm tax. Every RISC-V design win is a permanent royalty loss."),
   ("Smartphone units are flat-to-cyclical","The royalty base is still dominated by mobile, where unit growth is anemic. Royalty growth relies on rate (v9/CSS), which is finite, not on volume."),
   ("Licensing is lumpy","Upfront license revenue can swing quarters and mask underlying royalty trends; a soft licensing quarter against this multiple gaps the stock."),
   ("Customer concentration and conflict","Large licensees (including Qualcomm, with whom Arm has litigated) can push back on pricing or accelerate RISC-V to reduce dependence."),
   ("Float and ownership distortion","SoftBank's ~90% ownership leaves a small float that amplifies volatility and arguably inflates the price versus a freely traded equity."),
   ("China exposure","A meaningful royalty share runs through Arm China, a separately governed entity with historical control disputes and geopolitical risk."),
   ("No margin of safety","Versus EDA peers at 35-48x earnings, Arm at >100x has nothing to cushion a deceleration; the multiple is the risk.")],
 "synthesis":{
   "Bull":("$65 to 75","Royalty inflection runs hot, Arm captures large data-center CPU share and monetizes AI design starts aggressively; even this lands well below the current price on intrinsic and a 45x EBITDA cross-check."),
   "Base":("$40 to 50","v9/CSS lift royalty per chip and data-center adoption grows steadily; DCF (~$44) and a generous cross-check frame fair value far under spot."),
   "Bear":("$20 to 30","RISC-V takes low-end share, a smartphone air pocket hits royalties, and the IP premium compresses toward EDA-peer multiples.")},
 "recommendation_table":[
   {"action":"Direction","detail":"SELL / avoid on valuation. Best-in-class IP franchise, but ~70x sales prices several years of perfect inflection. Intrinsic ~$47."},
   {"action":"12m target","detail":"$47 (25% x $24 + 45% x $44 + 10% x $70 + 20% x $70 cross-check)."},
   {"action":"Existing longs","detail":"Trim aggressively into strength; the quality does not justify the multiple after a ~3x run."},
   {"action":"New money","detail":"Avoid. Even a 45x EBITDA cross-check sits ~80% below spot."},
   {"action":"Hedge","detail":"Long holders should hedge; thin float and high multiple make downside gaps acute."},
   {"action":"Position sizing","detail":"Own only at small size for the franchise optionality; valuation dominates the risk."}],
 "catalysts_to_watch":[
   "Q1 FY27 print (est 2026-07-29): royalty revenue growth and v9/CSS mix.",
   "Data-center CPU design wins and Arm-server share commentary.",
   "Any major RISC-V design win at a large customer.",
   "Smartphone unit trends and the royalty-rate trajectory.",
   "Licensing pipeline (AI design starts) and its lumpiness.",
   "Arm China governance and royalty-flow developments.",
   "SoftBank ownership/float actions."],
 "data_gaps":[
   "yfinance fundamentals were thin this session; revenue (~$4.9B FY26E), net cash (~$2.7B) and margin splits are from general disclosure.",
   "Royalty-versus-licensing mix and per-customer concentration are not available at line-item level this session.",
   "Forward EBITDA (~$1.6B) used in the cross-check is an estimate.",
   "Arm China financial detail and short interest were not retrievable this session."],
 "business_overview":{
   "summary":"Arm Holdings designs and licenses the instruction-set architecture and processor IP that powers nearly all smartphones and a growing share of data-center, automotive and embedded chips. It does not manufacture chips; it earns license fees when customers adopt its designs and royalties on every chip shipped using them.",
   "business_model":"Two revenue streams: licensing (upfront fees for access to Arm IP and architectures) and royalties (a per-chip fee, often a percentage of chip ASP, paid on every unit shipped). Royalties are a long-duration annuity that compounds with the compute market; Armv9 and CSS raise the rate per chip. R&D is largely fixed, so incremental royalties are high-margin.",
   "segments":[
     {"name":"Royalty","revenue_share_pct":60,"growth_yoy_pct":None,"margin_pct":None,
      "description":"Per-chip fees across smartphones, data center, automotive, IoT and AI. The recurring annuity; v9/CSS lift the rate."},
     {"name":"Licensing & other","revenue_share_pct":40,"growth_yoy_pct":None,"margin_pct":None,
      "description":"Upfront fees for IP and architecture access, including ATA/flexible-access agreements. Lumpy; leads future royalties."}],
   "geographic_revenue":[],
   "customers":[
     {"name":"Apple","revenue_share_pct":None,"importance":"Architecture licensee; high-value mobile and Mac silicon"},
     {"name":"Qualcomm / MediaTek","revenue_share_pct":None,"importance":"Major mobile SoC royalty payers"},
     {"name":"Hyperscalers (AWS, etc.)","revenue_share_pct":None,"importance":"Custom Arm data-center CPUs, the new growth pool"},
     {"name":"NVIDIA","revenue_share_pct":None,"importance":"Grace CPU and Arm-based AI systems"}]},
 "industry_position":{
   "market_overview":"Arm's architecture is the default for mobile and embedded compute and is expanding into the data center and automotive as power efficiency and custom silicon matter more. The competitive frontier is x86 (Intel, AMD) in servers and the open RISC-V architecture across the cost-sensitive and ideologically-motivated edges.",
   "tam_usd_bn":250,
   "moat":"An enormous installed software and tools ecosystem built on Arm creates near-insurmountable switching costs and durable pricing power, the textbook IP-royalty moat. The principal threat is RISC-V, which sidesteps the licensing model entirely and improves each year.",
   "competitors":[
     {"name":"RISC-V (open architecture)","description":"License-free ISA improving rapidly; the structural long-term threat to the royalty model."},
     {"name":"Intel / AMD (x86)","description":"Incumbent server architecture Arm is taking share from in the data center."},
     {"name":"Synopsys / Cadence","description":"Adjacent IP/EDA franchises; closest economic comparables, not direct ISA rivals."}]},
 "historical_financials":[
   {"fy":"FY23","revenue_usd_b":2.68,"revenue_growth_yoy_pct":None,"gross_margin_pct":95.0,"ebitda_usd_m":650,"ebitda_margin_pct":24.3,"net_income_usd_m":520,"fcf_usd_m":400,"eps":0.5},
   {"fy":"FY24","revenue_usd_b":3.23,"revenue_growth_yoy_pct":20.5,"gross_margin_pct":95.0,"ebitda_usd_m":850,"ebitda_margin_pct":26.3,"net_income_usd_m":300,"fcf_usd_m":600,"eps":0.3},
   {"fy":"FY25","revenue_usd_b":4.0,"revenue_growth_yoy_pct":23.8,"gross_margin_pct":96.0,"ebitda_usd_m":1200,"ebitda_margin_pct":30.0,"net_income_usd_m":800,"fcf_usd_m":900,"eps":0.75},
   {"fy":"FY26E","revenue_usd_b":4.9,"revenue_growth_yoy_pct":22.5,"gross_margin_pct":96.0,"ebitda_usd_m":1600,"ebitda_margin_pct":32.7,"net_income_usd_m":1100,"fcf_usd_m":1200,"eps":1.0}],
 "management":{
   "ceo":"Rene Haas, CEO since 2022","cfo":"Jason Child, CFO",
   "insider_ownership_pct":90.0,
   "capital_allocation_history":"Arm is ~90% owned by SoftBank, which relisted it in 2023. Capital allocation centers on heavy R&D reinvestment to push into data center and AI; no meaningful dividend or buyback given the small float and growth focus. The strategy of moving up-stack (CSS, subsystems) is sound, but the controlling-shareholder structure and thin float distort the equity's pricing and liquidity.",
   "recent_insider_activity":[]},
 "key_risks":[
   {"category":"structural","title":"RISC-V encroachment","description":"An open, license-free architecture targeting Arm's royalty model; each design win is a permanent royalty loss, especially at the low end."},
   {"category":"structural","title":"Valuation","description":"At ~70x sales and >100x earnings there is no margin of safety; any deceleration re-rates the stock sharply."},
   {"category":"cyclical","title":"Smartphone dependence","description":"Royalties still lean on flat-to-cyclical mobile units; rate gains (v9/CSS) are finite."},
   {"category":"customer","title":"Licensee conflict / concentration","description":"Large licensees can dispute pricing (e.g., Qualcomm litigation) or accelerate RISC-V to cut dependence."},
   {"category":"regulatory","title":"Arm China / geopolitics","description":"A meaningful royalty share runs through a separately governed Arm China amid US-China tensions and historical control disputes."},
   {"category":"structural","title":"Float and control","description":"~90% SoftBank ownership leaves a thin float that amplifies volatility and may inflate the price."}],
 "social_sentiment":{"summary":"Sentiment feeds were not retrievable this session. Bulls frame Arm as a compute-royalty monopoly with a data-center inflection; skeptics focus on RISC-V, smartphone dependence, thin float and a multiple with no margin of safety."}})

# ===================================================================
# NOW (ServiceNow)
# ===================================================================
build("NOW",{
 "name":"ServiceNow, Inc.","listings":"NYSE",
 "sector":"Technology. Enterprise Software (SaaS)",
 "action":"HOLD","tone":"neutral",
 "rationale":"0.20 x $69 (Bear) + 0.55 x $119 (Base) + 0.05 x $173 (Bull) + 0.20 x $120 (EV/EBITDA cross-check) = $112. Roughly fair: a high-quality 20% compounder with 30%+ FCF margins priced about right. The one name in this basket where intrinsic value meets the market.",
 "next_earnings":"2026-07-23 (Q2 FY26 est. Subscription revenue, cRPO and Now Assist ACV the prints that matter)",
 "snapshot":snap([("Last close","$106.97"),("52-week range","$81.24 to $211.48"),
   ("Drawdown from high","-49.4% (split-adjusted range)"),("Note","Prices reflect ~5:1 split in this dataset"),
   ("Market cap","$110.3B"),("Shares out","1.031B"),("Net cash (est)","~$6B"),
   ("FY25 revenue (est)","~$13B"),("Subscription gross margin","~85%"),("FCF margin (est)","~31%"),
   ("Primary method","DCF (FCFF)"),("Cross-check","EV/EBITDA 28x"),("Intrinsic vs price","+4%")]),
 "thesis":[
   "ServiceNow is the system of action for enterprise IT and increasingly for HR, customer service and security workflows, with ~98% renewal rates and net revenue retention around 115% that make its ~20% growth unusually durable and visible.",
   "Now Assist, its generative-AI layer, is a credible second pricing lever: charging for AI agents and assistants on top of the existing platform expands ARPU without a new sales motion, and early ACV traction supports the upsell thesis.",
   "Unlike the rest of this basket, the valuation is defensible. A DCF on normalized cash margins lands near $119 and an EV/EBITDA cross-check near $120, both close to the $107 price. Quality compounder, roughly fair, modest upside."],
 "bear_paragraph":"ServiceNow is the highest-quality business in this group, which is precisely why the bear case is about price and pace rather than collapse. The platform is genuinely sticky, renewal rates sit near ninety-eight percent, and net retention above one hundred fifteen percent means the company grows even if it never signs another logo. The risk is twofold. First, the multiple: even after a drawdown, the stock trades at a premium that assumes twenty-percent growth and expanding margins continue largely uninterrupted, so any deceleration below the high-teens, whether from a macro-driven freeze in enterprise IT budgets or simple law-of-large-numbers gravity on a thirteen-billion-dollar revenue base, would compress the multiple. Second, and more subtly, generative AI is double-edged for a company whose pricing has historically tracked seats and workflows: if AI agents let enterprises do more with fewer licensed users, the same technology ServiceNow is monetizing through Now Assist could erode the seat-based core it sits on. Neither risk is acute, and the base case remains a steady compounder. But at this valuation the upside is modest and the burden of proof is on continued flawless execution, which is why intrinsic value and the market price sit almost on top of each other.",
 "peers":[
   {"ticker":"NOW","pe_ntm":45.0,"ev_ebitda":28.0,"rev_growth_ttm":20.0,"ytd":5.0,"y1":-10.0,"highlight":True},
   {"ticker":"CRM","pe_ntm":24.0,"ev_ebitda":16.0,"rev_growth_ttm":9.0,"ytd":10.0,"y1":15.0},
   {"ticker":"WDAY","pe_ntm":28.0,"ev_ebitda":18.0,"rev_growth_ttm":15.0,"ytd":12.0,"y1":20.0},
   {"ticker":"ADBE","pe_ntm":22.0,"ev_ebitda":15.0,"rev_growth_ttm":10.0,"ytd":8.0,"y1":5.0},
   {"ticker":"SNOW","pe_ntm":120.0,"ev_ebitda":80.0,"rev_growth_ttm":28.0,"ytd":20.0,"y1":40.0},
   {"ticker":"INTU","pe_ntm":30.0,"ev_ebitda":22.0,"rev_growth_ttm":12.0,"ytd":15.0,"y1":25.0}],
 "peers_read":"Among premium SaaS, ServiceNow sits at the higher end on EV/EBITDA (~28x) but is backed by the best growth-durability profile in the group: faster than Salesforce, Workday or Adobe, with comparable or better retention and margins. It is far cheaper than hypergrowth Snowflake. The read is that NOW commands a deserved premium to mature SaaS for its growth-plus-margin combination, but that premium is now fair rather than cheap. Versus its own history the multiple has compressed, which is what brings intrinsic value and price into line.",
 "bull_catalysts":[
   ("Now Assist genAI monetization","ServiceNow charges for AI agents and assistants on top of existing subscriptions, a high-margin upsell to the installed base that expands ARPU without a new go-to-market and is ramping in ACV."),
   ("~98% renewal, 115%+ net retention","The platform's stickiness means revenue compounds from the existing base alone; expansion within accounts drives most growth, making the ~20% rate unusually visible."),
   ("Platform expansion beyond IT","ITSM remains the anchor, but HR, customer service, security operations and now creator/low-code workflows broaden the TAM and deepen account penetration."),
   ("Operating-leverage and FCF","FCF margin near 31% and rising; a largely fixed platform cost base means incremental subscription revenue drops at high margin, funding buybacks and R&D."),
   ("Large enterprise standardization","ServiceNow is increasingly the standard workflow platform for large enterprises and governments, a durable, multi-year displacement of legacy and homegrown tools."),
   ("cRPO visibility","Current remaining performance obligations give multi-quarter revenue visibility and de-risk the near-term growth path."),
   ("Net-cash balance sheet","A net-cash position and strong FCF allow consistent buybacks that compound per-share value and offset SBC over time."),
   ("AI-agent platform optionality","If autonomous enterprise agents become standard, ServiceNow's workflow data and orchestration layer position it to be the control plane, a large optional upside.")],
 "bear_breakers":[
   ("Premium multiple, modest upside","At ~28x EBITDA the price already credits durable 20% growth and margin expansion; intrinsic DCF (~$119) sits barely above spot, so the risk/reward is balanced, not asymmetric."),
   ("Law of large numbers","On a ~$13B revenue base, sustaining 20% growth gets mathematically harder each year; deceleration toward the mid-teens would compress the multiple."),
   ("AI could erode seat-based pricing","If AI agents let enterprises accomplish more with fewer licensed users, the same genAI wave ServiceNow monetizes could undercut its seat-linked core."),
   ("Enterprise IT-budget sensitivity","A macro-driven freeze in enterprise software budgets slows new bookings and expansion, the swing factor in any given year."),
   ("SBC dilution","Stock-based compensation is a real cost that flatters non-GAAP margins; buybacks offset rather than shrink the count, tempering per-share compounding."),
   ("Competitive encroachment","Salesforce, Microsoft and platform vendors increasingly overlap ServiceNow's workflow turf, pressuring the long-run expansion runway."),
   ("Now Assist ACV is early","The genAI upsell is promising but still small; if attach rates or pricing disappoint, a key part of the growth-reacceleration narrative weakens."),
   ("Valuation leaves little error margin","Unlike a deep-value name, NOW must execute to justify the price; there is limited cushion if growth or margins wobble.")],
 "synthesis":{
   "Bull":("$165 to 175","Now Assist becomes a large, fast-growing second engine and net retention re-accelerates; the platform compounds above plan and the multiple re-expands."),
   "Base":("$110 to 125","Steady ~20% growth with FCF margin grinding into the low-30s; DCF (~$119) and the EV/EBITDA cross-check (~$120) sit just above the $107 price."),
   "Bear":("$65 to 80","An enterprise-budget freeze or AI-driven seat compression slows growth below the high-teens and the premium multiple de-rates.")},
 "recommendation_table":[
   {"action":"Direction","detail":"HOLD. Best business in the basket, priced about fair; intrinsic ~$112 versus $107 spot."},
   {"action":"12m target","detail":"$112 (20% x $69 + 55% x $119 + 5% x $173 + 20% x $120 cross-check)."},
   {"action":"Existing longs","detail":"Hold the compounder. Add on macro-driven pullbacks toward the bear zone."},
   {"action":"New money","detail":"Starter position acceptable; scale in on weakness given the balanced risk/reward."},
   {"action":"Hedge","detail":"Less urgent than the rest of the basket; quality and net cash cushion the downside."},
   {"action":"Position sizing","detail":"Core-quality weight justified by durability; modest upside argues against over-sizing."}],
 "catalysts_to_watch":[
   "Q2 FY26 print (est 2026-07-23): subscription revenue, cRPO growth and guidance.",
   "Now Assist (genAI) ACV and attach-rate disclosures.",
   "Net revenue retention and renewal-rate trends.",
   "Enterprise IT-budget commentary as a macro tell.",
   "Operating and FCF margin trajectory toward the mid-30s.",
   "Competitive moves from Salesforce/Microsoft on workflow.",
   "Buyback pace versus SBC."],
 "data_gaps":[
   "Prices in this dataset reflect an apparent ~5:1 split (1.03B shares, ~$107); fundamentals normalized accordingly.",
   "yfinance fundamentals were thin this session; revenue (~$13B), net cash (~$6B) and FCF margin (~31%) are from general disclosure.",
   "GAAP EBIT understates cash earnings; DCF uses a normalized cash-margin proxy with that reasoning stated in the inputs.",
   "Now Assist ACV and net-retention specifics were not retrievable at line-item level this session."],
 "business_overview":{
   "summary":"ServiceNow is an enterprise-software company whose cloud platform digitizes and automates workflows, starting in IT service and operations management and extending into HR, customer service, security operations and low-code application development. It is the system of action large enterprises use to run cross-functional processes.",
   "business_model":"ServiceNow sells multi-year SaaS subscriptions priced by module and user, with high gross margins (~85% subscription) and strong renewal and expansion economics. Growth comes mainly from expanding within existing accounts (net retention ~115%) plus new logos, with Now Assist adding an AI-based upsell layer.",
   "segments":[
     {"name":"Subscription","revenue_share_pct":97,"growth_yoy_pct":None,"margin_pct":85,
      "description":"Recurring platform subscriptions across ITSM/ITOM, HR, customer service, security and creator workflows, plus Now Assist genAI. The whole business, essentially."},
     {"name":"Professional services & other","revenue_share_pct":3,"growth_yoy_pct":None,"margin_pct":None,
      "description":"Implementation and training; low-margin, run roughly at cost to drive subscription adoption."}],
   "geographic_revenue":[],
   "customers":[
     {"name":"Large enterprises (Global 2000)","revenue_share_pct":None,"importance":"Core base; deep multi-module penetration"},
     {"name":"Governments / public sector","revenue_share_pct":None,"importance":"Large, sticky workflow deployments"},
     {"name":"Regulated industries (financials, healthcare)","revenue_share_pct":None,"importance":"High-value, compliance-driven adoption"}]},
 "industry_position":{
   "market_overview":"Enterprises are standardizing fragmented, homegrown and legacy workflow tools onto unified cloud platforms, and layering generative AI on top to automate work. ServiceNow is the leader in IT workflow and a fast expander across enterprise functions, competing with Salesforce, Microsoft and point solutions.",
   "tam_usd_bn":300,
   "moat":"A single platform of record for cross-functional workflows creates deep switching costs: once processes, integrations and data live in ServiceNow, ripping it out is enormously disruptive. Near-98% renewal and 115%+ net retention quantify the moat. The risk is that AI reshapes how workflow software is priced and consumed.",
   "competitors":[
     {"name":"Salesforce (CRM)","description":"Overlapping in customer service and platform/low-code; largest SaaS competitor by breadth."},
     {"name":"Microsoft","description":"Power Platform, Dynamics and Copilot increasingly encroach on workflow automation."},
     {"name":"Atlassian / point solutions","description":"Targeted ITSM and developer-workflow tools at the lower end."},
     {"name":"Workday (WDAY)","description":"Adjacent in HR/finance workflows; partner and occasional competitor."}]},
 "historical_financials":[
   {"fy":"FY22","revenue_usd_b":7.25,"revenue_growth_yoy_pct":None,"gross_margin_pct":78.0,"ebitda_usd_m":1600,"ebitda_margin_pct":22.1,"net_income_usd_m":325,"fcf_usd_m":2180,"eps":0.32},
   {"fy":"FY23","revenue_usd_b":8.97,"revenue_growth_yoy_pct":23.7,"gross_margin_pct":79.0,"ebitda_usd_m":2150,"ebitda_margin_pct":24.0,"net_income_usd_m":1730,"fcf_usd_m":2700,"eps":1.6},
   {"fy":"FY24","revenue_usd_b":10.98,"revenue_growth_yoy_pct":22.4,"gross_margin_pct":79.0,"ebitda_usd_m":2900,"ebitda_margin_pct":26.4,"net_income_usd_m":1430,"fcf_usd_m":3400,"eps":1.3},
   {"fy":"FY25","revenue_usd_b":13.0,"revenue_growth_yoy_pct":18.4,"gross_margin_pct":80.0,"ebitda_usd_m":3700,"ebitda_margin_pct":28.5,"net_income_usd_m":2000,"fcf_usd_m":4050,"eps":1.9}],
 "management":{
   "ceo":"Bill McDermott, CEO since 2019","cfo":"Gina Mastantuono, CFO",
   "insider_ownership_pct":1.0,
   "capital_allocation_history":"Under McDermott ServiceNow has reinvested heavily in platform and AI while expanding margins steadily and beginning consistent buybacks to offset SBC. The capital-allocation record is disciplined and execution has been remarkably consistent (renewals near 98%). The model self-funds growth; the open question is how AI reshapes pricing, not whether management executes.",
   "recent_insider_activity":[]},
 "key_risks":[
   {"category":"structural","title":"Valuation / modest upside","description":"At ~28x EBITDA the price credits durable 20% growth; intrinsic value sits only modestly above spot, so risk/reward is balanced."},
   {"category":"cyclical","title":"Enterprise IT-budget sensitivity","description":"A macro-driven software-budget freeze slows bookings and expansion, the key swing factor in any year."},
   {"category":"structural","title":"AI seat-pricing risk","description":"If AI agents reduce licensed-user counts, generative AI could erode the seat-based core even as Now Assist monetizes it."},
   {"category":"competitive","title":"Platform encroachment","description":"Salesforce and Microsoft increasingly overlap ServiceNow's workflow turf, pressuring the long-run expansion runway."},
   {"category":"structural","title":"Law of large numbers","description":"Sustaining 20% on a $13B base gets harder each year; deceleration compresses the premium multiple."},
   {"category":"structural","title":"SBC dilution","description":"Stock-based comp flatters non-GAAP margins; buybacks offset rather than shrink the count."}],
 "social_sentiment":{"summary":"Sentiment feeds were not retrievable this session. Bulls highlight best-in-class durability and the Now Assist AI upsell; skeptics focus on a premium multiple, law-of-large-numbers deceleration and the double-edged effect of AI on seat-based pricing."}})

# ===================================================================
# FN (Fabrinet)
# ===================================================================
build("FN",{
 "name":"Fabrinet","listings":"NYSE",
 "sector":"Technology. Optical & Electronic Manufacturing",
 "action":"SELL","tone":"negative",
 "rationale":"0.25 x $144 (Bear) + 0.45 x $245 (Base) + 0.10 x $338 (Bull) + 0.20 x $268 (EV/EBITDA cross-check) = $234. A well-run optical assembler, but ~6x sales for a thin-margin contract manufacturer prices a flawless AI-optical decade; intrinsic value sits ~60% below spot.",
 "next_earnings":"2026-08-17 (Q4 FY26 est. Datacom revenue and optical-program mix the prints that matter)",
 "snapshot":snap([("Last close","$586.00"),("52-week range","$236.86 to $748.89"),
   ("Drawdown from high","-21.8%"),("1-year return","+140% (approx)"),("Market cap","$21.0B"),
   ("Shares out","35.8M"),("Net cash (est)","~$0.9B"),("FY25 revenue (est)","~$3.4B"),
   ("EV/Sales (fwd, est)","~5x"),("Operating margin (est)","~12.5%"),("Primary method","DCF (FCFF)"),
   ("Cross-check","EV/EBITDA 15x"),("Intrinsic vs price","-57%")]),
 "thesis":[
   "Fabrinet is the trusted contract manufacturer behind the industry's most complex optical modules, assembling the 800G and 1.6T transceivers and silicon-photonics engines that the leading optical and networking vendors design but do not build themselves.",
   "Its precision optical-packaging expertise, scaled Thai manufacturing base and long relationships with the top transceiver and networking customers make it the default high-complexity optical assembler, riding the same AI-interconnect wave as the component makers.",
   "But Fabrinet earns a ~12-13% operating margin as an assembler and now trades near 6x sales. Even a DCF that extrapolates the AI-optical ramp lands near $245 against a $586 stock. A great operator, priced like the chip designers it serves."],
 "bear_paragraph":"Fabrinet is a superbly run business that the market has decided to value as something it is not. At its core Fabrinet is a contract manufacturer: it assembles and tests optical modules that other companies design, earning a low-teens operating margin for precision and reliability rather than for owning intellectual property. That is a genuinely good version of a structurally modest business, and the AI-optical boom has been a windfall, filling its Thai lines with high-complexity 800G and 1.6T work. None of it justifies six times sales. The customer concentration is real, a handful of large transceiver and networking OEMs drive the bulk of revenue, and any one of them shifting programs, dual-sourcing, or moving toward co-packaged optics that changes the assembly footprint would dent the growth the multiple extrapolates. Co-packaged optics is the structural wildcard: it does not eliminate assembly, but it could move where the value sits and disrupt the pluggable-module volumes Fabrinet rides today. With only thirty-six million shares the stock is thin and moves hard in both directions, and it has roughly tripled off its low. Intrinsic DCF, even on a constructive ramp, says fair value is a little over four hundred dollars below the price. You are paying a designer's multiple for an assembler's economics.",
 "peers":[
   {"ticker":"FN","pe_ntm":30.0,"ev_ebitda":24.0,"rev_growth_ttm":18.0,"ytd":55.0,"y1":140.0,"highlight":True},
   {"ticker":"COHR","pe_ntm":48.0,"ev_ebitda":50.0,"rev_growth_ttm":24.0,"ytd":120.0,"y1":360.0},
   {"ticker":"LITE","pe_ntm":28.0,"ev_ebitda":22.0,"rev_growth_ttm":18.0,"ytd":60.0,"y1":110.0},
   {"ticker":"SANM","pe_ntm":15.0,"ev_ebitda":9.0,"rev_growth_ttm":8.0,"ytd":40.0,"y1":70.0},
   {"ticker":"FLEX","pe_ntm":16.0,"ev_ebitda":11.0,"rev_growth_ttm":5.0,"ytd":30.0,"y1":55.0},
   {"ticker":"AAOI","pe_ntm":40.0,"ev_ebitda":35.0,"rev_growth_ttm":30.0,"ytd":90.0,"y1":150.0}],
 "peers_read":"Fabrinet sits awkwardly between two cohorts. Against optical-component makers Coherent and Lumentum it grows similarly but owns less IP, yet it trades at a comparable or higher multiple. Against its true economic peers, contract manufacturers Sanmina and Flex at 9-11x EV/EBITDA, it trades at more than double on growth that is faster but built on the same thin-margin assembly model. The market is pricing Fabrinet as an optical-technology play; its income statement says contract manufacturer. That gap between perceived and actual business model is the core of the valuation risk.",
 "bull_catalysts":[
   ("1.6T optical assembly ramp","As the industry moves from 800G to 1.6T, dollar content and assembly complexity per module rise, and Fabrinet is designed into the leading programs as the build partner of choice."),
   ("Default high-complexity assembler","Fabrinet's precision optical-packaging and test capability is hard to replicate at scale, making it the trusted partner for the most demanding transceiver and silicon-photonics work."),
   ("Customer relationships with optical leaders","Long-standing relationships with the top transceiver and networking vendors give Fabrinet first call on new high-volume optical programs."),
   ("Scaled, cost-advantaged Thai base","A large, efficient Thai manufacturing footprint offers cost and capacity advantages and supply-chain resilience outside China."),
   ("Silicon-photonics and CPO assembly option","If co-packaged optics and silicon-photonics scale, the complex assembly and test could flow to Fabrinet, turning a perceived threat into a content opportunity."),
   ("Steady margin and strong FCF","A consistent low-teens operating margin, disciplined cost control and a net-cash balance sheet produce reliable free cash flow and buybacks."),
   ("Non-optical diversification","Automotive, industrial and sensor assembly provide a secondary, less AI-correlated revenue base."),
   ("Scarcity of optical-assembly exposure","Fabrinet is the cleanest listed proxy for AI optical-module assembly, attracting thematic flows that support the multiple.")],
 "bear_breakers":[
   ("6x sales for an assembler","Fabrinet earns a ~12-13% operating margin assembling others' designs, yet trades near 6x sales. Contract manufacturers trade at 1-2x. Intrinsic DCF says ~$245."),
   ("Customer concentration","A few large transceiver/networking OEMs drive most revenue. One shifting programs or dual-sourcing steps growth down sharply, and Fabrinet owns none of the IP."),
   ("Co-packaged optics overhang","CPO could move the optical engine into the switch package, disrupting the pluggable-module volumes Fabrinet assembles today; even partial adoption caps the extrapolated TAM."),
   ("No IP, no pricing power","Fabrinet competes on execution and capacity, not technology ownership; the customer can move the work, capping margins and durability."),
   ("Thin float, high volatility","With ~36M shares the stock gaps hard in both directions and is exposed to thematic-flow reversals."),
   ("AI-optical cycle risk","The datacom surge driving growth is a capex wave that will digest; an assembler levered to it de-rates fastest when it does."),
   ("Margins are structurally capped","Even the bull case reaches only ~14% operating margin; this is not a technology-margin business dressed in an AI multiple."),
   ("Tripled on momentum","Up roughly 3x off its low and owned by thematic flows, the stock has more than discounted the AI-optical assembly thesis.")],
 "synthesis":{
   "Bull":("$320 to 360","1.6T and CPO assembly flow to Fabrinet at scale and margins expand above plan; even so intrinsic value stays below the current price."),
   "Base":("$230 to 270","Datacom-led growth decelerates and margins inch toward 14%; DCF (~$245) and the EV/EBITDA cross-check (~$268) frame fair value well under spot."),
   "Bear":("$130 to 160","A key customer in-sources or shifts to co-packaged optics and the multiple compresses toward contract-manufacturing norms.")},
 "recommendation_table":[
   {"action":"Direction","detail":"SELL / avoid on valuation. Excellent operator, but ~6x sales for an assembler is unsupportable; intrinsic ~$234."},
   {"action":"12m target","detail":"$234 (25% x $144 + 45% x $245 + 10% x $338 + 20% x $268 cross-check)."},
   {"action":"Existing longs","detail":"Take profits after a ~3x run; the assembly thesis is more than priced."},
   {"action":"New money","detail":"Avoid at ~6x sales. Revisit nearer contract-manufacturing multiples or on a major de-rate."},
   {"action":"Hedge","detail":"Thin float makes downside gaps acute; long holders should consider collars."},
   {"action":"Position sizing","detail":"If held for the theme, keep small; valuation is the dominant risk."}],
 "catalysts_to_watch":[
   "Q4 FY26 print (est 2026-08-17): datacom revenue and optical-program mix.",
   "1.6T program ramp and any new optical-assembly wins.",
   "Customer-concentration commentary and any program shifts.",
   "Co-packaged-optics roadmap signals from optical and switch vendors.",
   "Operating-margin trajectory versus the ~14% ceiling.",
   "Non-optical (automotive/industrial) diversification trends.",
   "Buyback pace given the net-cash balance sheet."],
 "data_gaps":[
   "yfinance fundamentals were thin this session; revenue (~$3.4B), net cash (~$0.9B) and margins are from general disclosure.",
   "Per-customer concentration is undisclosed at line-item level; optical-OEM exposure is inferred from industry reporting.",
   "Forward EBITDA (~$0.58B) used in the cross-check is an estimate.",
   "Short interest and positioning feeds were not retrievable this session."],
 "business_overview":{
   "summary":"Fabrinet is a precision optical and electronic contract manufacturer based in Thailand. It provides advanced optical packaging, assembly and testing for the world's leading optical-communications and networking companies, building the complex transceivers and photonic modules those firms design but outsource.",
   "business_model":"Fabrinet earns manufacturing fees to assemble and test customers' optical and electro-mechanical products, concentrated in datacom/telecom optical modules with a secondary base in automotive, industrial, medical and sensor products. It owns the process and manufacturing know-how, not the product IP; margins are low-teens, reflecting the contract-manufacturing model.",
   "segments":[
     {"name":"Optical communications","revenue_share_pct":80,"growth_yoy_pct":None,"margin_pct":None,
      "description":"Datacom (800G/1.6T transceivers, silicon-photonics engines, the AI growth engine) and telecom transport optics for the leading optical and networking OEMs."},
     {"name":"Non-optical","revenue_share_pct":20,"growth_yoy_pct":None,"margin_pct":None,
      "description":"Automotive, industrial, medical and sensor assembly; steadier, less AI-correlated diversification."}],
   "geographic_revenue":[],
   "customers":[
     {"name":"Leading transceiver/optical OEMs","revenue_share_pct":None,"importance":"Core datacom demand; concentrated"},
     {"name":"Networking equipment vendors","revenue_share_pct":None,"importance":"Optical content for switches/routers"},
     {"name":"Automotive & industrial OEMs","revenue_share_pct":None,"importance":"Non-optical diversification"}]},
 "industry_position":{
   "market_overview":"AI clusters require vast optical interconnect, and the optical-component vendors that design transceivers largely outsource the complex assembly and test to specialists. Fabrinet is the leading high-complexity optical assembler, competing with in-house manufacturing and other contract manufacturers, with co-packaged optics as the key structural wildcard.",
   "tam_usd_bn":30,
   "moat":"Precision optical-packaging and test capability at scale is genuinely hard to replicate and creates real switching friction on complex programs. But it is operational know-how, not product IP; the customer owns the design and can move the work, which caps the moat and the margin.",
   "competitors":[
     {"name":"In-house manufacturing (COHR, etc.)","description":"Vertically integrated optical makers that assemble their own modules, bypassing Fabrinet."},
     {"name":"Sanmina / Flex","description":"Large contract manufacturers that can take optical/electro-mechanical assembly work."},
     {"name":"Asian optical EMS","description":"Lower-cost regional assemblers competing on price for higher-volume programs."}]},
 "historical_financials":[
   {"fy":"FY22","revenue_usd_b":2.26,"revenue_growth_yoy_pct":None,"gross_margin_pct":12.4,"ebitda_usd_m":290,"ebitda_margin_pct":12.8,"net_income_usd_m":215,"fcf_usd_m":180,"eps":5.9},
   {"fy":"FY23","revenue_usd_b":2.65,"revenue_growth_yoy_pct":17.3,"gross_margin_pct":12.6,"ebitda_usd_m":345,"ebitda_margin_pct":13.0,"net_income_usd_m":265,"fcf_usd_m":210,"eps":7.2},
   {"fy":"FY24","revenue_usd_b":2.93,"revenue_growth_yoy_pct":10.6,"gross_margin_pct":12.6,"ebitda_usd_m":390,"ebitda_margin_pct":13.3,"net_income_usd_m":300,"fcf_usd_m":250,"eps":8.2},
   {"fy":"FY25","revenue_usd_b":3.4,"revenue_growth_yoy_pct":16.0,"gross_margin_pct":12.8,"ebitda_usd_m":460,"ebitda_margin_pct":13.5,"net_income_usd_m":360,"fcf_usd_m":300,"eps":9.9}],
 "management":{
   "ceo":"Seamus Grady, CEO since 2017","cfo":"Csaba Sverha, CFO",
   "insider_ownership_pct":2.0,
   "capital_allocation_history":"Fabrinet has been a disciplined operator: steady capacity investment in Thailand, a net-cash balance sheet and consistent buybacks that have shrunk the share count over time. Management has navigated the optical cycle well and avoided overextension. The execution record is strong; the question is the multiple the market now assigns to a contract-manufacturing model.",
   "recent_insider_activity":[]},
 "key_risks":[
   {"category":"customer","title":"Customer concentration","description":"A few optical OEMs drive most revenue; one shifting programs or dual-sourcing steps growth down sharply."},
   {"category":"structural","title":"Co-packaged optics","description":"CPO could move the optical engine into the switch package, disrupting the pluggable-module volumes Fabrinet assembles."},
   {"category":"structural","title":"Valuation","description":"At ~6x sales for a low-teens-margin assembler, multiple compression toward contract-manufacturing norms is the dominant risk."},
   {"category":"cyclical","title":"AI-optical capex digestion","description":"The datacom surge is a capex wave; an assembler levered to it de-rates fastest when it digests."},
   {"category":"structural","title":"Thin float / volatility","description":"~36M shares make the stock gap hard in both directions on thematic flows."},
   {"category":"regulatory","title":"Geographic / trade exposure","description":"Concentrated Thai manufacturing and global optical supply chains carry trade-policy and concentration risk."}],
 "social_sentiment":{"summary":"Sentiment feeds were not retrievable this session. Bulls frame Fabrinet as the indispensable AI optical-module assembler; skeptics focus on contract-manufacturing economics, customer concentration, co-packaged-optics risk and a sales multiple far above its true peers."}})
