# National Security Assessment: Weight Theft Risks in Frontier Labs

**Policy teardown memo**  
**Primary lens:** Leopold Aschenbrenner’s *Situational Awareness* on state-level race dynamics, adapted into concrete security requirements for frontier model weights.  
**Audience:** Lab CISOs, board risk committees, policymakers, preparedness / security teams.

---

## 1. Why weights are a national-security object

Frontier model weights are not ordinary SaaS IP. They are:

- A **compressed artifact of $10^{25}$+ FLOP training runs** and proprietary data mixtures.
- A **force multiplier** for cyber operations, influence, and automated R&D once paired with scaffolding.
- A **proliferation vector**: once exfiltrated, weights can be fine-tuned, ablated, and served outside the originating lab’s safety stack.

Aschenbrenner’s strategic warning is blunt: as models approach transformative capability, **nation-state espionage** incentives rise faster than typical corporate security culture adapts. Treating weights like source code behind a VPN is a category error.

This memo evaluates corporate cybersecurity baselines against state-level threats and proposes **SCIF-grade / air-gapped controls for models trained above $\sim 10^{26}$ FLOPs** (adjust thresholds as eval science matures).

---

## 2. Threat model (who and how)

| Adversary | Objective | Likely vectors |
|---|---|---|
| Peer nation intelligence services | Acquire weights + training recipes; skip $B-scale CapEx | Insider recruitment, supply-chain implants, cloud lateral movement, compromised contractor laptops |
| Sophisticated cybercriminals | Resell weights / API keys; ransom | Phishing, endpoint malware, misconfigured object stores |
| Competing labs / contractors | Parameter or data theft | Over-permissioned vendors, shared clusters, research collab sprawl |
| Insiders (ideological or coerced) | Leak checkpoints | USB, encrypted channels, steganographic exfil, “research export” abuse |

**Critical path insight:** The highest EV attacks are rarely glamorous zero-days against training kernels. They are **identity, endpoint, and backup-path** failures: a researcher laptop with Hugging Face tokens, an S3 bucket with loose IAM, a checkpoint sync job to a “temporary” staging project.

Open-weights ecology raises a second issue: even *partial* technical understanding of **refusal directions and safety circuitry** (mechanistic interpretability) means that stolen aligned weights can be surgically degraded. Defensive research on refusal vectors is therefore part of risk assessment—not a how-to for attackers, but a measure of **how brittle post-exfiltration safety is**.

---

## 3. Corporate baseline vs. state-level reality

Typical “strong” corporate controls:

- SSO + MFA, EDR, laptop disk encryption
- VPC isolation, secrets managers, periodic pen tests
- Model APIs behind auth and rate limits
- Employee security training

Necessary, **not sufficient** against a motivated MSS:

1. **EDR assumes the endpoint is the perimeter.** State actors can burn zero-days or use coerced insiders with legitimate access.
2. **Cloud shared responsibility** blurs who owns checkpoint ACLs across training, eval, and research accounts.
3. **Research culture optimizes for iteration speed**—copying checkpoints to personal projects, sharing via chat, spinning ad-hoc endpoints.
4. **Third-party clusters and annotator vendors** expand the TCB (trusted computing base) beyond the lab’s HR perimeter.
5. **Safety layers sitting only at the API** do nothing once raw weights leave.

Aschenbrenner’s race framing implies that as strategic value rises, the correct comparison set is **weapons-adjacent information security**, not consumer internet companies.

---

## 4. Capability threshold: why $\sim 10^{26}$ FLOPs

Absolute FLOP cutoffs are crude but **administratively useful**. Below some scale, weights are valuable commercially; above it, they become strategically sensitive:

- Training cost and data uniqueness make reacquisition hard for most actors.
- Agent scaffolding + tool use amplify misuse potential.
- Fine-tunes and ablation can strip refusal behavior faster than labs can patch APIs.

**Policy proposal:** Models (and intermediate checkpoints) from runs **≥ $10^{26}$ FLOPs**—or models that pass a designated dangerous-capability eval suite regardless of FLOPs—enter **Tier-0 Weight Custody**.

Boards should revisit the numeric gate annually as algorithmic efficiency shifts the FLOP–capability mapping.

---

## 5. Recommended SCIF-level / air-gap requirements (Tier-0)

### 5.1 Custody and topology

1. **Air-gapped training enclave** for Tier-0 final stages: no general internet egress; allowlisted update mirrors only via diode / manual media where feasible.
2. **Weight SCIF analogue:** physically controlled rooms or equivalently controlled HSMs / sealed clusters for checkpoint storage; dual-control access (two-person rule) for export jobs.
3. **No Tier-0 weights on laptops.** Ever. Research happens via mediated interfaces (thin clients, locked notebooks, or lossy API eval hooks).
4. **Cryptographic compartmentation:** per-checkpoint keys in HSMs; decrypt only onto attested training nodes.

### 5.2 Identity and insider risk

5. **Cleared / high-assurance personnel** for Tier-0 access; continuous evaluation; foreign travel briefings.
6. **Just-in-time access** with time-boxed roles; default deny across projects.
7. **Behavioral analytics** on checkpoint read volume, unusual serialization, and off-hours access—tuned for espionage, not only ransomware.

### 5.3 Supply chain and contractors

8. **Hardware attestation** (secure boot, measured launch) for training nodes; signed firmware bills of materials.
9. **Vendor isolation:** annotators and eval contractors never receive Tier-0 weights; use distilled / red-teamed proxies.
10. **Cloud secondary:** if public cloud is unavoidable, dedicated hosts + customer-controlled keys + contractual audit rights; prefer sovereign or dedicated regions.

### 5.4 Detection and response

11. **Canary checkpoints** and watermarking research to detect leaks in the wild.
12. **Exfil drills** quarterly: red-team attempts to move a fake Tier-0 artifact past controls.
13. **Kill-switch playbooks** for API keys and staging mirrors within minutes of suspected compromise.
14. **Mandatory incident reporting** timelines to designated national authorities for confirmed Tier-0 theft (jurisdiction-dependent).

### 5.5 Safety after theft (assume breach)

15. Plan as if **weights will eventually leak**. Invest in:
    - Robustness to refusal ablation and linear steering attacks
    - Rapid fingerprinting of stolen derivatives
    - Staged capability releases so a single checkpoint is not “the whole stack”
16. Pair security with **interpretability-informed** evaluations of how easily safety features can be removed post-exfiltration (see portfolio mech-interp artifact).

---

## 6. Governance checklist for boards

- [ ] Has the lab inventoried all checkpoints ≥ threshold and their storage locations?
- [ ] Is there a named executive owner for Tier-0 custody (not only the CISO backlog)?
- [ ] Are interconnect / cloud architectures reviewed against nation-state TTPs annually?
- [ ] Do research incentives still reward copying weights to unmanaged environments?
- [ ] Is there a tested 24-hour response plan with government coordination contacts?
- [ ] Are open publications reviewed for operational security (opsec) on training stack details?

---

## 7. Policy options beyond the firm

1. **Mandatory reporting** of Tier-0 theft attempts to a national cyber center.
2. **Export-control clarity** for foundation-model weights above defined capability/FLOP gates.
3. **Information-sharing** among frontier labs on IOCs without sharing proprietary model IP.
4. **Public–private surge capacity** for forensic response when a strategically significant checkpoint leaks.
5. **Funding defensive mech-interp** as security R&D, not only as science.

---

## 8. Bottom line

Corporate cybersecurity built for SaaS breach economics underprices **state-driven weight theft**. Aschenbrenner’s situational picture implies that as FLOPs and capability cross strategic thresholds, frontier labs must adopt **weapons-grade custody**: air-gapped enclaves, two-person control, attested hardware, zero laptop residency for Tier-0 artifacts, and assume-breach safety engineering.

The goal is not paranoia theater. It is to make successful exfiltration of $≥10^{26}$-FLOP weights **expensive, slow, noisy, and incomplete**—and to ensure that even a successful theft does not instantly yield an unaligned, production-ready strategic asset.

---

*Companion artifacts:* `code/refusal-vector-steering` (defensive interpretability), portfolio simulators for strategic context on compute scale.
