---
title: "Computational Design of CrtW and CrtZ for Enhanced Astaxanthin Biosynthesis"
date: 2025-09-01
year: "2025"
weight: 2
selected: true
venue: "ZJU"
venueLogo: "images/logos/zju.svg"
lab: "Zhou Lab"
status: "Ongoing"
authors: "Advised by Dr. Yangwei Jiang & [Prof. Ruhong Zhou](http://iqb.zju.edu.cn/en/a/rencai/zzjs/2021/1220/75.html)"
tags: ["enzyme engineering", "protein design", "molecular dynamics"]
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

## Method

The design campaign combined two complementary signals across 320 residues, producing
**268 candidates**:

- **Structure-based design** — Rosetta FuncLib
- **Sequence-based design** — ESM2 and ThermoMPNN

The top 6 candidates then went through **2 µs molecular dynamics simulations**, which probe
what static predictions cannot: how the substrate is positioned over time, and how stable
the ligand-binding pocket stays.

Tools: Rosetta, GROMACS, ESM2, PyMOL, AlphaFold3, HPLC.

{{< figure src="images/projects/crtw-strategy.png"
  caption="Design strategy — structure-based and sequence-based screening feeding into MD evaluation." >}}

## Results

- **G142P + I192L** emerged as the strongest design, giving the most extended substrate
  positioning and the most stable ligand-binding pocket of the candidates — outperforming
  what the static structural predictions suggested, with no loss of protein stability.
- Carried into the wet lab, the top mutant **confirmed the predicted improvement in vitro,
  reaching +46.7% yield over wild-type**.

{{< figure src="images/projects/crtw-result-single.png"
  caption="Single mutants." >}}

{{< figure src="images/projects/crtw-result-double.png"
  caption="Double mutants, including G142P + I192L." >}}

The MD stage is what separated the winning design from candidates that looked comparable on
structure alone.
