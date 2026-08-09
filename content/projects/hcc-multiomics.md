---
title: "Sex Dimorphism in DEN/TCPOBOP-Induced Hepatocellular Carcinoma"
date: 2026-03-01
year: "2025"
weight: 4
selected: true
venue: "ZJU Medicine"
venueLogo: "images/logos/zju-medicine.png"
lab: "Sui Lab"
thumbPoster: "images/projects/hcc-network-poster.webp"
thumb: "images/projects/hcc-network.webp"
authors: "PI: [Prof. Meihua Sui](https://person.zju.edu.cn/suimeihua/745023.html)"
tags: ["multi-omics", "bioinformatics", "cancer biology"]
summary: "Separating sex-driven metabolic differences from the tumour burden that confounds them, across 174 samples of paired serum metabolomics and liver transcriptomics."
draft: false
---

## Background

Hepatocellular carcinoma is markedly more common in males, and the obvious way to look for
why is to compare metabolites between the sexes. The obvious way is also wrong: male mice
carry more tumour, so anything that merely tracks tumour burden will present itself as a
sex difference. Telling the two apart is the whole problem.

## Method

Paired **serum untargeted metabolomics and liver transcriptomics** from a DEN-induced mouse
model. The raw acquisition gives 9,082 spectral features, most of them noise, adducts or
fragments of the same compound; curation reduces that to a **468-metabolite matrix across
174 samples**.

On top of it sits a **sex × disease interaction model with tumour burden as a covariate**,
so a metabolite only scores if its behaviour differs by sex *beyond* what its tumour load
explains. Significance comes from **1,000 permutations** rather than a parametric
assumption the data does not support.

Tools: R (DESeq2, WGCNA), Python, untargeted metabolomics, transcriptomics.

## Results

The interaction test leaves roughly **190 candidates** — too many to chase, and most of
them will not survive contact with an orthogonal method. So the shortlist demands **four
independent lines of evidence** from each metabolite:

1. a significant sex × disease interaction,
2. independence from tumour burden,
3. reversal under intervention, and
4. a corroborating enzyme in the transcriptome.

**About 20 clear all four** (permutation *p* = 0.001), and **roughly 13 of those have not
been reported before** in the context of HCC sex dimorphism.

Together they outline an **estrogen (ERα)-driven metabolic reprogramming axis**, whose
direction was confirmed rather than assumed: the intervention arm pushes the system both
ways, and the markers move accordingly.

The panel is now queued for targeted MS/MS, which is the measurement that would turn these
from candidates into findings.

_The project is ongoing._
