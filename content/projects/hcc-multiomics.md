---
title: "Sex Dimorphism in DEN/TCPOBOP-Induced Hepatocellular Carcinoma"
date: 2026-03-01
year: "2026"
weight: 4
selected: true
venue: "Sui Lab, ZJU Medicine"
status: "Ongoing"
authors: "Advised by Dr. Wenbin Zhou · Prof. Meihua Sui's Lab, School of Medicine, Zhejiang University"
tags: ["multi-omics", "bioinformatics", "cancer biology"]
summary: "Transcriptomic and metabolomic analysis across 174 mice, tracing sex-biased metabolites through hepatitis, cirrhosis, and HCC — and testing whether hormone supplementation reverses them."
draft: false
---

## Background

Hepatocellular carcinoma (HCC) is markedly more common in males, but the mechanism behind
that sex bias is not well resolved — particularly which molecular differences appear at
which stage of disease progression, and whether they are causes or consequences.

## Method

Using a DEN/TCPOBOP-induced mouse model, I analysed paired **transcriptomic and metabolomic
data across 174 mice**, spanning three stages of progression: hepatitis, cirrhosis, and HCC.

The analysis had three parts:

1. **Multi-omics profiling** to identify metabolites that differ by sex across stages.
2. **A hormone rescue arm**, testing whether estrogen supplementation moves those markers.
3. **Network integration**, linking WGCNA and PPI hub genes back to the metabolomic
   findings.

Tools: R (DESeq2, WGCNA), Python, transcriptomics, metabolomics.

## Results

- **12 core sex-biased metabolites** were identified, concentrated in the bile acid,
  tryptophan, and acylcarnitine pathways.
- **Estrogen supplementation reversed the bile acid marker TUDCA (+97%)** and rescued
  roughly half of the male–female gap in a composite disease score.
- **155 links** between hub genes and metabolomic findings emerged from network
  integration, pointing to candidate drivers of sex-biased liver disease progression.

The project is ongoing.
