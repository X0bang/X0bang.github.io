---
title: "Computational Design of CrtW and CrtZ for Enhanced Astaxanthin Biosynthesis"
date: 2025-09-01
year: "2025"
weight: 2
selected: true
venue: "ZJU"
venueLogo: "images/logos/zju-eagle.png"
lab: "Zhou Lab"
thumbPoster: "images/projects/crtw-poster.jpg"
thumb: "images/projects/crtw-design.mp4"
status: "Ongoing"
authors: "Supervised by Dr. Yangwei Jiang · PI: [Prof. Ruhong Zhou](http://iqb.zju.edu.cn/en/a/rencai/zzjs/2021/1220/75.html)"
tags: ["enzyme engineering", "protein engineering", "structural biology", "molecular dynamics"]
links:
  - name: "Code"
    url: "https://github.com/X0bang/crtw-enzyme-design"
summary: "Combining Rosetta FuncLib with protein language models to redesign the rate-limiting astaxanthin ketolase, validated in vitro at +46.7% yield."
draft: false
---

## Background

Astaxanthin is a high-value carotenoid whose microbial production is throttled by a single
step: **CrtW**, the β-carotene ketolase, is the rate-limiting enzyme in the pathway.
Improving it is the most direct route to higher yield — but static structural prediction on
its own is a weak guide to which mutations will actually pay off.

The reaction needs both ends of β-carotene — IUPAC C4 and C4′ — brought up to the di-iron
centre. That gives the design problem a concrete test a static score cannot answer: does the
substrate actually sit where the chemistry needs it, and does it stay there?

## Method

**Two independent tracks.** The whole pipeline was run twice, once from an AlphaFold3 model
and once from an ESMFold model, and only mutations that reached the top 50 of *both* were
treated as high-confidence. Fifteen did.

Each track ran the same stages: Rosetta FastRelax over 100 conformations, a single-point
ΔΔG scan across 193 positions × 19 amino acids, a ThermoMPNN scan alongside it, and
percentile cross-ranking to merge the two signals. Surviving single points were then
enumerated into roughly 86,000 pairs and rescored.

{{< figure src="images/projects/crtw/screening-single.png"
  caption="Single-point screening, top 20 in each track. V192L ranks first in both; A234L is second in the ESMFold track and ninth in the AlphaFold3 track. The two that went on to MD are highlighted." >}}

**Molecular dynamics.** Candidates went into all-atom MD as full membrane systems —
~168,000 atoms in a mixed POPE/POPG bilayer with water and ions, CHARMM36m, GROMACS 2024.2
— for **12 × 500 ns, 6 µs of sampling in total**.

Tools: Rosetta, GROMACS, ESM2, ThermoMPNN, AlphaFold3, PyMOL, HPLC.

## Results

**A234L is the design that works.** In wild-type CrtW the C4′ end is well placed 96.6% of
the time but C4 — the first ketolation site — reaches its target zone only **10.2%** of the
time, which is a structural account of why the enzyme is slow. The single mutation
Ala234→Leu raises C4 to **96.4%** while holding C4′ at 98.8%.

Carried into the wet lab, A234L **confirmed the prediction in vitro at +46.7% yield over
wild-type**.

{{< figure src="images/projects/crtw/consensus-md.png"
  caption="Left: mutations ranked by both tracks, with the consensus set picked out. Right: how each system held the substrate over 500 ns." >}}

Requiring both ends to be on target *at the same time* separates the candidates sharply.

{{< figure src="images/projects/crtw/joint-positioning.png"
  caption="C4 against C4′ across the run, coloured by time. Only A234L holds both ends in their target zones simultaneously — 95.2% of frames against wild-type's 10.2%." >}}

**Two mutations that each work can fail together.** V192L ranked first in both screening
tracks and A234L was the best performer in MD, so the pair looked like the obvious
combination. It collapsed: joint on-target occupancy fell to **1.8%**, C4′ to 2.8%, and
backbone RMSD was the highest of any system. Two leucines in the same pocket compress the
space β-carotene needs to extend into, and the substrate curls. This is negative epistasis,
and no amount of single-point ranking would have predicted it.

{{< figure src="images/projects/crtw/performance-heatmap.png"
  caption="Five systems against five measures. The V192L+A234L row is red throughout." >}}

The catalytic centre itself is coordinated by seven histidines, and tracking their NE2
atoms against both ends of the substrate shows how the pocket is reorganised.

{{< figure src="images/projects/crtw/his-distances.png"
  caption="His NE2 to each ketolation site, averaged over the run. Blue is close, red is far." >}}

A separate lesson came from the 27-mutation FuncLib design, which scored well on substrate
positioning but turned out to carry **His165→Leu** — a member of the HXXH iron-coordinating
motif. Positioning says nothing about whether the metal centre survives; the screen needed
the catalytic histidines locked before it ran, not after.

MD is what separated the design that worked from the one that looked strictly better on
paper.

_The project is ongoing._
