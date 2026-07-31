---
title: "Trimeric Redesign of a CAR-T Costimulatory Transmembrane Domain"
date: 2026-06-01
year: "2026"
weight: 1
selected: true
venue: "WEHI InSPIRE"
status: "Ongoing"
authors: "Supervised by Dr. Emma Petley · PIs: Prof. Matt Call & A/Prof. Melissa Call"
tags: ["protein engineering", "structural biology", "molecular dynamics"]
links:
  - name: "Program"
    url: "https://www.wehi.edu.au/education/undergraduate/inspire/"
summary: "Redesigning a CAR-T costimulatory transmembrane domain back into its native trimeric form, screened by 2 µs MD and validated by flow cytometry and degranulation assays."
draft: false
---

## Background

Chimeric antigen receptor (CAR) T cells rely on costimulatory domains to sustain activation,
and 4-1BB is among the most widely used. In its native context the receptor assembles as a
trimer, but conventional CAR constructs place its transmembrane domain (TMD) in an
architecture that does not preserve that geometry.

Building on the host lab's **proCAR3** design hypothesis, this project asks a direct
question: if the 4-1BBζ TMD is redesigned back into its natural trimeric form, does T cell
activation improve?

## Method

The work runs on two tracks.

**Dry lab — computational screening.** I independently ran 2 µs molecular dynamics
simulations across 4 candidate designs to test whether each assembles into a stable trimer,
using GROMACS with ΔG prediction, Rosetta, and ESM2 to guide and evaluate the designs.

**Wet lab — functional validation.** Collaborating with the team, I helped optimise 4 TMD
variants, then ran flow cytometry and degranulation assays against 2 tumour cell lines,
confirming surface expression before measuring function.

Techniques: flow cytometry, degranulation assay, HEK293T culture, GROMACS, ΔG prediction,
Rosetta, ESM2.

## Results

<!-- TODO: 这两处数值在 CV 的 PDF 文本层里被截断了(原文停在
     "surface expression (73–74" 和 "stable trimer assembly (achieving 85"),
     请按 CV 原稿把完整数字补进下面两行。 -->

- **Surface expression** was confirmed for the TMD variants across both tumour cell lines,
  establishing that the redesigned constructs traffic correctly before function is assessed.
- **Trimer assembly** remained stable across the MD screen, supporting the hypothesis that
  the redesigned TMD adopts and holds the intended trimeric form.

Work is ongoing, with functional comparison against the conventional 4-1BBζ architecture as
the current focus.

_Fully funded through the WEHI InSPIRE program._
