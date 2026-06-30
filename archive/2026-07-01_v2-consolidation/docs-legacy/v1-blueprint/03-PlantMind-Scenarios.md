# PlantMind — 10 Real-World Scenarios
### Across LTTS's Three Core Business Segments

Each scenario is a real industrial situation where PlantMind's predict → decide → prove loop solves a concrete, expensive problem. These are your pitch stories — pick one per judge audience.

---

## SEGMENT A: SUSTAINABILITY (4 scenarios)
*Process engineering · Industrial automation · Energy transition*

---

### Scenario 1 — The Compressor That Never Had to Fail
**Industry:** Natural gas processing plant, Middle East
**Setting:** A centrifugal compressor on the gas-sweetening line runs 24/7. It has 21 sensors. Historically, 3 compressors fail per year — each failure costs $800K in lost throughput plus $200K in emergency repair.

**The pain today:** The plant's predictive tool flags "compressor bearing degradation — alert in 14 days." The maintenance engineer reads this alert alongside 47 others. He schedules a shutdown for bearing replacement — the most obvious action.

**What PlantMind does differently:**
PlantMind runs the Götze engine across four candidates:
- Replace bearing immediately → costs $200K, planned downtime 8 hours
- Reduce suction pressure 10% → costs near-zero, extends bearing life 22 days
- Reroute gas to standby compressor → costs $30K, zero downtime
- **Winner: reroute + reduce pressure** → Götze score 0.89 vs. replace's 0.54

The RED→GREEN chart shows: "replace" buys 8 days before next failure; "reroute + reduce" buys 28 days and shifts failure outside the current production campaign.

**Outcome:** $170K saved on this one decision. Multiplied across 6 compressors in the plant: $1M+ annual decision value.

**LTTS angle:** This is exactly the LTTS–Databricks partnership use case — "industrial AI for Energy, Petrochemicals and Industrials clients."

---

### Scenario 2 — The Wind Farm That Learned to Heal Itself
**Industry:** Offshore wind farm, North Sea
**Setting:** 80 turbines, each with gearbox, main bearing, and generator sensors. Gearbox replacement costs €500K and requires a specialized vessel (lead time: 3 weeks). Weather windows are narrow.

**The pain today:** Turbines are either run to failure (because planned maintenance is expensive) or maintained on fixed schedules regardless of actual condition. Both approaches waste money.

**What PlantMind does differently:**
PlantMind monitors all 80 turbines continuously. When turbine 34 shows gearbox bearing anomaly:
- Götze engine scores: replace now (€500K, 3-week wait) vs. reduce rotor speed 8% (near-zero cost, extends life 45 days)
- **Winner: reduce rotor speed** → life extended past next scheduled maintenance window — gearbox replacement folded into a planned visit that was already coming
- Energy objective term captures: 8% speed reduction = 7% energy output loss for 45 days = quantified trade-off, not a guess

**Outcome:** €500K gearbox replacement converted into a €12K planned-visit job. Energy loss is $18K — net saving €470K on one turbine decision.

**RED→GREEN proof:** Turbine 34's health curve crosses the failure threshold 3 weeks out (RED); with speed reduction, it flatlines above threshold for 45+ days (GREEN).

**LTTS angle:** LTTS serves major European energy clients; offshore wind is a stated Sustainability growth area.

---

### Scenario 3 — The Chemical Plant That Stopped Guessing Reactor Maintenance
**Industry:** Specialty chemicals plant, India
**Setting:** Batch reactor with heat exchanger, agitator, and jacket cooling sensors. A fouled heat exchanger that isn't caught in time causes a batch rejection — each batch worth ₹40 lakh.

**The pain today:** Fouling builds up gradually. The condition monitoring system says "fouling index above 0.7 — consider cleaning." The operator considers it and moves on — there's no calculation of what "consider" costs.

**What PlantMind does differently:**
PlantMind's Götze engine computes:
- Schedule CIP (clean-in-place) now: 4-hour downtime, ₹1.2L cleaning cost, 1 batch lost
- Reduce jacket temperature 5°C: reduces fouling rate 30%, extends to next planned shutdown
- Increase agitator speed: compensates for reduced heat transfer, zero downtime
- **Winner: agitator speed increase + reduce jacket temp** → 3 batches saved vs. immediate CIP

**Outcome:** Net saving: ₹40L × 3 batches = ₹1.2 crore from one maintenance decision.

**LTTS angle:** LTTS's Sustainability segment includes discrete manufacturing and process engineering — this is a direct client story.

---

### Scenario 4 — The Data Center That Cuts Cooling Waste by 18%
**Industry:** Hyperscale data center, Sustainability via energy
**Setting:** Cooling towers and CRAC units consume 40% of total data center energy. Predictive maintenance today catches failed fans or refrigerant leaks — but doesn't optimize across units.

**The pain today:** When CRAC unit 7 degrades, the maintenance team replaces it on the next maintenance window. In the meantime, adjacent units compensate — silently running harder, degrading faster, and consuming 20% more energy.

**What PlantMind does differently:**
Götze engine evaluates: replace CRAC-7 now vs. rebalance load across CRAC-5, 6, 8 while scheduling replacement next week.
- Rebalancing reduces CRAC-5/6/8 overload → energy consumption drops 18%
- CRAC-7 replacement folded into planned maintenance — no emergency call-out fee
- **Energy term in Götze score:** captures the 18% saving explicitly — this is the Sustainability connection

**LTTS angle:** LTTS's Sustainability segment includes data-center engineering as a stated growth driver in FY26. Energy is the explicit Götze objective.

---

## SEGMENT B: MOBILITY (3 scenarios)
*Software-defined vehicles · Electrification · Transportation*

---

### Scenario 5 — The EV Battery That Knew It Was Dying Before It Stopped
**Industry:** Electric vehicle fleet operator, Europe
**Setting:** 200 delivery vans. Battery pack degradation is gradual. A van that fails mid-route costs €2,000 in roadside assist + route disruption. Battery replacement: €8,000 + 3-day workshop visit.

**The pain today:** Fleet telematics shows state-of-charge and range — not battery health or time-to-degradation. Batteries are replaced on fixed mileage cycles — some replaced too early, some too late.

**What PlantMind does differently:**
- Layer 2 (predict): cell temperature variance + voltage sag patterns → RUL in charge cycles
- Layer 4 (Götze): score "replace now" vs. "limit max charge to 80%" vs. "reassign to shorter routes"
- **Winner for van 147:** limit charge to 80% → extends battery life 40 cycles, eliminates mid-route failure risk, defers €8K replacement 6 months
- Energy term: 80% charge limit reduces fast-charging events → battery temperature lower → longevity gain

**Outcome:** €8,000 replacement deferred × 40 vans in similar condition = €320K fleet-level decision value.

**LTTS angle:** Software-Defined Mobility is a named Big Bet; electrification + EV lifecycle management is a stated focus.

---

### Scenario 6 — The Turbofan That Got a Second Opinion Before Grounding
**Industry:** Regional airline MRO (Maintenance, Repair, Overhaul)
**Setting:** (This is the NASA C-MAPSS story made real.) A regional carrier operates 60 turbofan engines. Current practice: MRO schedules engine shop visits on a fixed-cycle basis, regardless of actual degradation state.

**The pain today:** An engine flagged by predictive monitoring for "elevated HPC thermal stress" gets sent for a shop visit — at $1.2M per visit. But the visit reveals nothing requiring repair. The flag was a precaution.

**What PlantMind does differently:**
- Predict: HPC sensor degradation → RUL = 180 cycles (well above the 120-cycle shop-visit threshold)
- Diagnose: root cause = operating at unusually high power settings on short hops (not mechanical degradation)
- Götze score: reduce average power setting 3% (route re-optimization) → RUL extends to 240 cycles → shop visit deferred 2 months
- **Energy term:** 3% power reduction = 2.1% fuel burn reduction = $45K fuel saving over 60 cycles

**Outcome:** $1.2M shop visit deferred by 2 months + $45K fuel saving = $1.245M from one decision.

**LTTS angle:** LTTS serves aerospace & defence clients; MRO optimization under Software-Defined Mobility / embedded engineering.

---

### Scenario 7 — The Production Line Robot That Kept Working While Its Neighbor Was Repaired
**Industry:** Automotive body-shop, EV OEM plant
**Setting:** 12 welding robots in a line. A robot with degraded servo motor causes micro-positioning errors — resulting in weld quality defects caught only at inspection (2 stations downstream). Each defective body costs $3,200 in rework.

**The pain today:** Robot 7 is flagged. The line stops for 45 minutes for robot replacement. All 12 robots stand idle. The "Götze action" nobody considers: can Robot 8 partially compensate while Robot 7 runs at reduced speed?

**What PlantMind does differently:**
- Götze score: full stop vs. reduce Robot 7 speed 15% + redistribute 2 tasks to Robot 8 vs. replace servo immediately
- **Winner: redistribute + reduce speed** → throughput drops 8%, defect rate drops to zero, production continues for 6 hours until planned window
- Throughput term captures: 8% loss vs. 45-minute full stop = clear winner

**Outcome:** 45-minute stop = $28K lost throughput. Redistribute decision costs $2.3K in overtime planning. Net: $25.7K saved on a single robot event.

---

## SEGMENT C: TECH (3 scenarios)
*Semiconductors · MedTech · Next-gen compute*

---

### Scenario 8 — The Fab That Caught a Reticle Problem Before It Scrapped 200 Wafers
**Industry:** Semiconductor fabrication, Logic node
**Setting:** A lithography tool's illumination uniformity sensor (equivalent to our temperature sensors) drifts. Each scrapped wafer batch = $120K. The tool runs 24/7 with 4-hour preventive maintenance windows every 2 weeks.

**The pain today:** The illumination drift is detected — but only after 3 batches are scrapped. The predictive system would have flagged it 6 hours earlier if the threshold were tuned. But tuning thresholds is manual and risky.

**What PlantMind does differently:**
- Predict: sensor drift trajectory → estimated first batch-failure in 4.2 hours (within the prediction horizon)
- Götze score: take tool offline now (2-batch throughput loss = $240K) vs. reduce exposure dose 1.5% (compensates for drift, no throughput loss, tool runs to next planned window)
- **Winner: exposure dose reduction** → Götze score 0.91 vs. offline's 0.23
- Real cost saving: $240K avoided downtime vs. $0 cost adjustment

**Outcome:** 2 batches × $120K = $240K saved from one dose-adjustment decision.

**LTTS angle:** Tech segment — semiconductors explicitly named as a focus area under the Tech segment in FY26.

---

### Scenario 9 — The MRI Machine That Scheduled Its Own Maintenance Window
**Industry:** Hospital radiology department / MedTech OEM
**Setting:** MRI system has cryogenic helium cooling, gradient coils, and RF amplifiers — all with sensor data. Unexpected MRI downtime during business hours: $12,000/hour in lost scans + patient rescheduling costs. Planned maintenance: $2,500/visit.

**The pain today:** MRI maintenance is scheduled on fixed 6-month cycles. An unexpected helium compressor degradation causes the system to quench mid-week — $12K/hour for 6 hours = $72K loss.

**What PlantMind does differently:**
- Predict: helium compressor vibration + temperature → RUL = 18 days
- Götze score: emergency compressor service now (disruptive) vs. schedule maintenance on upcoming Saturday (6 days away, within the 18-day window)
- **Winner: scheduled Saturday** → Götze score 0.94 vs. emergency's 0.31 (emergency = 3× cost, disrupts patient bookings)
- Proof: health curve crosses failure threshold day 18 (RED); with Saturday maintenance, it resets to GREEN

**LTTS angle:** MedTech is the sixth named Big Bet under Lakshya-31. Medical device digital services is a stated LTTS FY26 revenue line.

---

### Scenario 10 — The GPU Cluster That Stopped Running Hot and Started Running Smart
**Industry:** AI compute infrastructure / Next-gen compute
**Setting:** A 512-GPU training cluster. GPU memory bandwidth degradation causes training jobs to slow by 15% and increases thermal events (throttling). Each throttling event wastes 8 minutes of compute at $4.20/GPU-hour. 512 GPUs × 8 minutes × 20 events/day = $470K/year in wasted compute.

**The pain today:** GPU health monitoring shows degradation but the action is always "replace GPU" — which requires job migration, takes 4 hours, and wastes 2,048 GPU-hours at $8,601 per replacement event.

**What PlantMind does differently:**
- Predict: memory bandwidth degradation + thermal signature → time to throttling onset
- Götze score: replace GPU now (4-hour job migration) vs. reduce GPU memory clock 5% (eliminates throttling, slight throughput cost) vs. migrate this job to a healthier node
- **Winner: migrate job + reduce clock** → Götze score 0.87 vs. replace's 0.33
- Energy term captures: 5% clock reduction = 3.2% power reduction per GPU = measurable energy saving

**Outcome:** $8,601 replacement avoided per event. Over 20 monthly events: $172K/month, $2M/year in compute cluster efficiency.

**LTTS angle:** "Next-Gen Compute & AI Infra" is one of the six Lakshya-31 Big Bets — this scenario is the most direct possible mapping.

---

## SCENARIO SELECTION GUIDE FOR JUDGES

| Judge background | Lead with | Supporting |
|---|---|---|
| Process / Chemical engineering | Scenario 3 (chemical plant) | Scenario 1 (compressor) |
| Energy / Utilities | Scenario 2 (wind) or 4 (data center) | Scenario 1 |
| Automotive | Scenario 5 (EV battery) or 7 (robot) | Scenario 6 |
| Aerospace | Scenario 6 (turbofan) | Scenario 5 |
| Semiconductor / MedTech | Scenario 8 (fab) or 9 (MRI) | Scenario 10 |
| AI / Cloud infra | Scenario 10 (GPU cluster) | Scenario 4 |
| C-suite / strategy | Scenario 1 + 6 (biggest $ numbers) | Any |

**The NASA C-MAPSS dataset maps directly to Scenario 6 (turbofan).** Use Scenario 6 in the technical demo. Use Scenario 1 or 2 as your pitch narrative — they're easier for non-engineers to picture.

---

*Scenarios v1.0 · PlantMind · LTTS EI Hackathon 2026*
