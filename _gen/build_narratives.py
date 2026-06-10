import json

DATE="2026-06-10"

def load(t):
    return json.load(open(f"output/{t}/{t}_valuation.json"))

def dcf_scen_rows(t, inputs):
    """Build narrative dcf_scenarios from valuation + inputs."""
    val=load(t)
    base_w=inputs["primary_method"]["inputs"]["wacc"]["value"]
    base_g=inputs["primary_method"]["inputs"]["terminal_growth"]["value"]
    sc_in={s["label"]:s for s in inputs["scenarios"]}
    out=[]
    for s in val["scenarios"]:
        lbl=s["label"]; kc=sc_in[lbl]["key_changes"]
        w=kc.get("wacc",base_w); g=kc.get("terminal_growth",base_g)
        fm=kc.get("fcf_multiplier",1.0)
        path=f"FCF x{fm:.2f} vs base" if fm!=1.0 else "base FCF path"
        out.append({"scenario":lbl,"wacc":f"{w*100:.2f}%","terminal_g":f"{g*100:.2f}%",
                    "fcf_path":path,"implied_px":round(s["implied_px"],0)})
    return out

def synth(t, descs):
    val=load(t); out=[]
    order={"Bull":None,"Base":None,"Bear":None}
    sc={s["label"]:s for s in val["scenarios"]}
    for lbl in ["Bull","Base","Bear"]:
        s=sc[lbl]
        out.append({"label":lbl,"prob":s["probability"],
                    "outcome_range":descs[lbl][0],"description":descs[lbl][1]})
    return out

def build(t, meta):
    val=load(t)
    px=val["current_price"]; tgt=round(val["blended_target"]); up=round(val["upside_pct"],1)
    inputs=json.load(open(f"output/{t}/{t}_inputs.json"))
    n={
      "ticker":t,"name":meta["name"],"listings":meta["listings"],"sector":meta["sector"],
      "date":DATE,"engine":"yfinance-data, equity-bull-case, equity-bear-case, dcf_compute, equity-audit",
      "recommendation":{"action":meta["action"],"tone":meta["tone"],"current_price":px,
        "target_12m":tgt,"upside_pct":up,"rationale":meta["rationale"],
        "next_earnings":meta["next_earnings"]},
      "snapshot":meta["snapshot"],
      "thesis":meta["thesis"],
      "bear_paragraph":meta["bear_paragraph"],
      "peers":meta["peers"],"peers_read":meta["peers_read"],
      "bull_catalysts":[{"id":i+1,"title":c[0],"body":c[1]} for i,c in enumerate(meta["bull_catalysts"])],
      "bear_breakers":[{"id":i+1,"title":c[0],"body":c[1]} for i,c in enumerate(meta["bear_breakers"])],
      "industry_type":"non-bank",
      "dcf_scenarios":dcf_scen_rows(t,inputs),
      "synthesis_paths":synth(t,meta["synthesis"]),
      "recommendation_table":meta["recommendation_table"],
      "catalysts_to_watch":meta["catalysts_to_watch"],
      "data_gaps":meta["data_gaps"],
      "business_overview":meta["business_overview"],
      "industry_position":meta["industry_position"],
      "historical_financials":meta["historical_financials"],
      "management":meta["management"],
      "key_risks":meta["key_risks"],
      "social_sentiment":meta["social_sentiment"],
    }
    json.dump(n,open(f"output/{t}/{t}.json","w"),indent=2)
    print(f"wrote output/{t}/{t}.json  target={tgt} upside={up}%")

def snap(rows): return [{"label":a,"value":b} for a,b in rows]

# ===================================================================
# COHR
# ===================================================================
build("COHR",{
 "name":"Coherent Corp.","listings":"NYSE",
 "sector":"Technology. Photonics & Optical Networking",
 "action":"SELL","tone":"negative",
 "rationale":"0.25 x $51 (Bear) + 0.45 x $121 (Base) + 0.10 x $184 (Bull) + 0.20 x $140 (EV/EBITDA cross-check) = $114. Intrinsic DCF lands ~68% below a share that has roughly 5x'd off its 52-week low. A real AI-optical franchise, priced for a decade of flawless 1.6T execution.",
 "next_earnings":"2026-08-12 (Q4 FY26 est. Datacom transceiver run-rate and indium-phosphide margin the prints that matter)",
 "snapshot":snap([("Last close","$355.94"),("52-week range","$76.88 to $440.00"),
   ("Drawdown from high","-19.1%"),("1-year return","+360% (approx, off $77 low)"),
   ("Market cap","$69.6B"),("Shares out","195.6M"),("Net debt (est)","~$4.5B"),
   ("FY25 revenue (est)","~$5.8B"),("EV/Sales (fwd, est)","~12x"),
   ("Primary method","DCF (FCFF)"),("Cross-check","EV/EBITDA 22x"),
   ("Beta (est)","1.45"),("Intrinsic vs price","-68%")]),
 "thesis":[
   "Coherent is a genuine winner of the AI-optical buildout: it supplies the 800G and 1.6T datacom transceivers and the indium-phosphide lasers inside them that connect accelerators across the data center, a market growing faster than compute itself.",
   "The II-VI merger gave it vertical integration from laser chip to finished module plus a recovering industrial-laser and telecom base, and deleveraging steadily lifts equity value as interest expense falls.",
   "The problem is price. At roughly 12x sales for a components maker whose datacom margins are perpetually reset each generation, an intrinsic DCF lands near $114 against a $356 stock. The franchise is real; the multiple prices a flawless decade."],
 "bear_paragraph":"Coherent is a good company wearing a valuation built for a different kind of business. Optical transceivers are a volume game where every generation, 400G to 800G to 1.6T, resets unit pricing downward, and Chinese competitors InnoLight and Eoptolink win share on cost. The bull case extrapolates the current AI-datacom surge into a smooth decade, but components demand is lumpy and tied to a handful of hyperscaler build schedules. The deeper threat is architectural: co-packaged optics aims to move the optical engine inside the switch package, which over time disintermediates the pluggable transceiver that drives Coherent's growth. Stack on roughly $4.5B of net debt inherited from the II-VI deal, a beta near 1.45, and a stock that has risen fivefold off its low, and you have an instrument that gaps on any soft quarter. You do not need a recession. You need one transceiver price war or one hyperscaler pausing its optical orders, and a 12x-sales multiple has nowhere to hide. Intrinsic DCF says the equity is worth a third of the price even on a constructive ramp. That gap is the thesis.",
 "peers":[
   {"ticker":"COHR","pe_ntm":48.0,"ev_ebitda":50.0,"rev_growth_ttm":24.0,"ytd":120.0,"y1":360.0,"highlight":True},
   {"ticker":"LITE","pe_ntm":28.0,"ev_ebitda":22.0,"rev_growth_ttm":18.0,"ytd":60.0,"y1":110.0},
   {"ticker":"FN","pe_ntm":30.0,"ev_ebitda":24.0,"rev_growth_ttm":18.0,"ytd":70.0,"y1":140.0},
   {"ticker":"AAOI","pe_ntm":40.0,"ev_ebitda":35.0,"rev_growth_ttm":30.0,"ytd":90.0,"y1":150.0},
   {"ticker":"MRVL","pe_ntm":46.8,"ev_ebitda":93.7,"rev_growth_ttm":27.6,"ytd":223.5,"y1":318.9},
   {"ticker":"APH","pe_ntm":32.0,"ev_ebitda":24.0,"rev_growth_ttm":20.0,"ytd":45.0,"y1":70.0}],
 "peers_read":"Across the optical cohort Coherent screens at the richest end on EV/EBITDA despite mid-20s growth that is in line with, not ahead of, Lumentum and Fabrinet. The market is paying a premium for vertical integration (own-laser content) and the perception that Coherent is the Western champion of AI optics. That premium is defensible directionally but extreme in magnitude: peers growing similarly trade at roughly half the multiple. The honest read is that the whole cohort has re-rated on AI optics and Coherent has re-rated the most.",
 "bull_catalysts":[
   ("1.6T datacom transceiver ramp","The step from 800G to 1.6T roughly doubles dollar content per optical link, and Coherent is designed into the leading hyperscaler and switch-vendor programs. Datacom is already the fastest-growing segment and 1.6T extends the runway through the back half of the decade."),
   ("Indium-phosphide vertical integration","Owning the laser chip (from the II-VI side) lets Coherent capture margin that module-only assemblers pay away, and secures supply of the scarcest component in a transceiver. As datacom mix rises, blended gross margin should expand."),
   ("Deleveraging lifts equity value","Roughly $4.5B of net debt from the merger means every dollar of debt paydown and every step down in interest expense transfers value from creditors to equity, a mechanical tailwind independent of revenue."),
   ("Co-packaged optics optionality","If CPO scales, the optical-engine and laser content moves but does not disappear, and Coherent's laser-chip franchise positions it to supply the engines rather than be disintermediated. It is both a risk and an option."),
   ("Telecom and industrial-laser recovery","The non-datacom segments (telecom transport, industrial and materials-processing lasers) are cyclically depressed; a recovery adds growth that is uncorrelated with the AI capex cycle."),
   ("Western-supply-chain preference","Hyperscalers increasingly want non-Chinese optical supply for security and resilience, which favors Coherent against InnoLight and Eoptolink on strategic accounts even at a price premium."),
   ("Operating leverage on merged cost base","The II-VI/Coherent integration synergies are still flowing through; incremental datacom revenue drops at high contribution margin against a largely fixed manufacturing footprint."),
   ("Scarcity bid for AI-optical exposure","There are few liquid, profitable, pure-ish ways to own AI optical networking; that scarcity keeps a structural bid under the shares regardless of intrinsic value, which is itself a (momentum) catalyst.")],
 "bear_breakers":[
   ("12x sales for a components maker","Coherent trades around 12x revenue with single-digit-to-teens FCF margins. Optical components historically trade at 2-4x sales. The entire thesis requires that this time the multiple is permanent. Intrinsic DCF says fair value is near $123, roughly a third of the price."),
   ("Every generation resets pricing","400G, 800G, 1.6T: each transition cuts per-bit pricing and invites new entrants. Volume growth has to outrun price erosion every single year just to stand still on revenue. That is a treadmill, not a moat."),
   ("Chinese cost competition","InnoLight and Eoptolink dominate transceiver volume on cost and are moving up the speed curve. On any account where security is not the deciding factor, Coherent competes on price it cannot win."),
   ("Co-packaged optics is a structural threat","The industry's roadmap to put optics inside the switch package exists specifically to remove the pluggable transceiver. Even partial CPO adoption caps the TAM the bull case extrapolates."),
   ("Customer and program concentration","Datacom revenue rides a few hyperscaler build schedules. A single program pause or design shift steps the fastest-growing line down with little warning, exactly the lumpiness a 12x multiple cannot absorb."),
   ("Leverage amplifies the equity hit","Roughly $4.5B net debt and a 1.45 beta mean a revenue or margin miss hits the equity disproportionately. Deleveraging cuts both ways: it helps in good times and bites in a downturn."),
   ("Fivefold run on momentum","A stock up roughly 5x off its low is owned by momentum and thematic flows. In any AI-sentiment wobble, weak hands sell first, and a name this extended can give back 30-50% on no fundamental change."),
   ("Margins are thin where it matters","Even in the bull case, blended EBIT margin reaches only the low-20s. This is not a software annuity; it is a capital- and labor-intensive manufacturer dressed in an AI multiple.")],
 "synthesis":{
   "Bull":("$170 to 200","1.6T and CPO content inflect faster than modeled, indium-phosphide integration lifts margins above plan, and the Western-supply premium holds. Even so, intrinsic value sits well below the current price."),
   "Base":("$110 to 140","Datacom-led growth decelerates gracefully and margins grind to the low-20s. Intrinsic DCF (~$121) and the EV/EBITDA cross-check (~$140) converge near $123, far under spot."),
   "Bear":("$45 to 70","A transceiver price war or a hyperscaler optical-order pause flattens datacom, CPO accelerates, and the multiple collapses toward components norms; the leveraged equity falls hard.")},
 "recommendation_table":[
   {"action":"Direction","detail":"SELL / avoid. Excellent AI-optical franchise, but intrinsic DCF (~$114) sits ~68% below the $356 price."},
   {"action":"12m target","detail":"$114 (25% x $51 + 45% x $121 + 10% x $184 + 20% x $140 cross-check)."},
   {"action":"Existing longs","detail":"Take profits or hedge. A fivefold gain off the low has more than discounted the AI-optical thesis."},
   {"action":"New money","detail":"Do not chase 12x sales. Revisit only on a major de-rate toward the cross-check zone."},
   {"action":"Hedge","detail":"Long holders should consider collars given 1.45 beta and the leveraged balance sheet."},
   {"action":"Position sizing","detail":"If owned for the theme, keep it small; the valuation gap is the dominant risk."}],
 "catalysts_to_watch":[
   "Q4 FY26 print (est 2026-08-12): datacom transceiver revenue run-rate and 1.6T mix.",
   "Datacom gross-margin trajectory as indium-phosphide vertical integration ramps.",
   "Net-debt paydown pace and interest-expense step-down.",
   "Any hyperscaler commentary on optical-order pacing or a shift toward co-packaged optics.",
   "Competitive pricing actions from InnoLight and Eoptolink at 800G/1.6T.",
   "Telecom and industrial-laser segment recovery as a non-AI growth source.",
   "Co-packaged-optics roadmap milestones from switch vendors."],
 "data_gaps":[
   "yfinance fundamentals were thin this session; net debt (~$4.5B), FY25 revenue (~$5.8B) and segment splits are from general disclosure, not a live filing extract.",
   "Per-customer datacom concentration is undisclosed; hyperscaler exposure is inferred from industry reporting.",
   "Forward EBITDA used in the cross-check (~$1.45B) is an estimate, not a pulled consensus figure.",
   "Short interest and options-positioning feeds were not retrievable this session."],
 "business_overview":{
   "summary":"Coherent is a vertically integrated photonics and optical-networking company formed by II-VI's acquisition of the original Coherent. It designs and manufactures lasers, optical components and the datacom transceivers that move data between AI accelerators, plus telecom transport optics, industrial lasers and engineered materials.",
   "business_model":"Revenue comes from selling optical hardware: datacom transceivers and components to hyperscalers and switch vendors, telecom transport optics to carriers, and industrial lasers and materials to manufacturers. Owning the laser-chip layer (indium phosphide, gallium arsenide) lets it capture component margin that module-only assemblers pay away.",
   "segments":[
     {"name":"Networking (Datacom + Telecom)","revenue_share_pct":55,"growth_yoy_pct":None,"margin_pct":None,
      "description":"800G/1.6T datacom transceivers for AI clusters (the growth engine) plus telecom transport optics. Datacom is compounding fast; telecom is cyclical."},
     {"name":"Lasers","revenue_share_pct":25,"growth_yoy_pct":None,"margin_pct":None,
      "description":"Industrial and materials-processing lasers; cyclically depressed, a recovery option."},
     {"name":"Materials","revenue_share_pct":20,"growth_yoy_pct":None,"margin_pct":None,
      "description":"Engineered materials and compound-semiconductor substrates, including silicon carbide; supplies internal and external customers."}],
   "geographic_revenue":[],
   "customers":[
     {"name":"Hyperscalers (via switch/OEM programs)","revenue_share_pct":None,"importance":"Datacom transceiver demand, the growth engine"},
     {"name":"Networking OEMs","revenue_share_pct":None,"importance":"Switch and router optical content"},
     {"name":"Telecom carriers","revenue_share_pct":None,"importance":"Transport optics, cyclical"}]},
 "industry_position":{
   "market_overview":"AI clusters need vast optical interconnect because copper runs out of reach at high bandwidth. Datacom transceiver demand is growing faster than compute, and the roadmap from 800G to 1.6T and toward co-packaged optics is the battleground. Coherent is one of a few vertically integrated Western suppliers.",
   "tam_usd_bn":40,
   "moat":"Vertical integration from laser chip to finished module is a genuine advantage on supply security and margin, and Western-supply preference helps on strategic accounts. The moat is real but narrow: it does not stop per-generation price erosion or the structural threat from co-packaged optics.",
   "competitors":[
     {"name":"Lumentum (LITE)","description":"Closest Western optical peer; strong in datacom lasers and transceivers."},
     {"name":"InnoLight / Eoptolink","description":"Chinese transceiver leaders that dominate volume on cost."},
     {"name":"Fabrinet (FN)","description":"Contract assembler for many optical programs; partner and competitor for content."},
     {"name":"Marvell / Broadcom","description":"Own the optical-DSP and switch silicon; drivers of CPO that could disintermediate pluggables."}]},
 "historical_financials":[
   {"fy":"FY22","revenue_usd_b":3.32,"revenue_growth_yoy_pct":None,"gross_margin_pct":35.0,"ebitda_usd_m":600,"ebitda_margin_pct":18.1,"net_income_usd_m":250,"fcf_usd_m":150,"eps":1.6},
   {"fy":"FY23","revenue_usd_b":5.16,"revenue_growth_yoy_pct":55.4,"gross_margin_pct":33.0,"ebitda_usd_m":850,"ebitda_margin_pct":16.5,"net_income_usd_m":-260,"fcf_usd_m":200,"eps":-1.9},
   {"fy":"FY24","revenue_usd_b":4.71,"revenue_growth_yoy_pct":-8.7,"gross_margin_pct":35.0,"ebitda_usd_m":900,"ebitda_margin_pct":19.1,"net_income_usd_m":-160,"fcf_usd_m":300,"eps":-1.1},
   {"fy":"FY25","revenue_usd_b":5.8,"revenue_growth_yoy_pct":23.1,"gross_margin_pct":38.0,"ebitda_usd_m":1150,"ebitda_margin_pct":19.8,"net_income_usd_m":350,"fcf_usd_m":450,"eps":2.2}],
 "management":{
   "ceo":"Jim Anderson, CEO (appointed 2024, ex-Lattice Semiconductor)","cfo":"Sherri Luther, CFO",
   "insider_ownership_pct":1.0,
   "capital_allocation_history":"Coherent is the product of II-VI's debt-funded $7B acquisition of the original Coherent in 2022. The post-merger priority has been integration, margin expansion and deleveraging rather than buybacks. The new CEO has pushed portfolio focus and a datacom-led growth strategy. No dividend; cash goes to debt paydown and capacity.",
   "recent_insider_activity":[]},
 "key_risks":[
   {"category":"structural","title":"Co-packaged optics disintermediation","description":"Industry roadmaps to embed optics in the switch package threaten the pluggable transceiver that drives Coherent's growth; even partial adoption caps the TAM."},
   {"category":"cyclical","title":"Per-generation price erosion","description":"Each speed transition resets unit pricing downward; volume must outrun price every year, leaving margins perpetually pressured."},
   {"category":"customer","title":"Hyperscaler order lumpiness","description":"Datacom revenue rides a few build schedules; a pause or design shift steps the growth line down abruptly."},
   {"category":"execution","title":"Leverage and integration","description":"Roughly $4.5B net debt and ongoing II-VI integration amplify any operational miss into the equity."},
   {"category":"regulatory","title":"Chinese competition and trade policy","description":"InnoLight/Eoptolink cost leadership and shifting export rules affect both competitive position and addressable accounts."},
   {"category":"structural","title":"Valuation","description":"At ~12x sales the equity prices a flawless decade; intrinsic DCF sits ~65% lower, so multiple compression is the dominant risk."}],
 "social_sentiment":{"summary":"Sentiment feeds were not retrievable this session. Bull commentary frames Coherent as the Western AI-optics champion; skeptics focus on transceiver price erosion, CPO risk and the extreme sales multiple after a fivefold run."}})
print("COHR done")
