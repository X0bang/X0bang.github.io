---
title: "LumaManta — Programmable Biosensing for Water Monitoring"
date: 2024-08-01
year: "2025"
weight: 3
selected: true
venue: "iGEM 2025"
venueLogo: "images/logos/igem.svg"
lab: "Bioinformatics Group"
status: "Silver Medal"
thumbPoster: "images/projects/lumamanta-detection-poster.webp"
thumb: "images/projects/lumamanta-detection.webp"
authors: "Technical Lead, ZJU-China · PIs: [Prof. Ming Chen](https://person.zju.edu.cn/en/0005111) & Prof. Fan Yang"
tags: ["iGEM", "synthetic biology", "optogenetics"]
links:
  - name: "Wiki"
    url: "https://2025.igem.wiki/zju-china/"
  - name: "Code"
    url: "https://gitlab.igem.org/2025/zju-china"
summary: "Converting two light inputs into four sensor proteins on demand with CRISPR logic gates, packaged as an all-in-one device for water pollutant and eDNA monitoring."
draft: false
---

## Background

Monitoring water for pollutants and environmental DNA (eDNA) usually means collecting
samples and sending them to a lab. An all-in-one device that senses in real time has to
solve a harder problem than any single biosensor does: one platform needs to report on
several different targets without carrying a separate genetic circuit for each.

## Method

As **Technical Lead** I coordinated a 14-member interdisciplinary team spanning wet lab,
dry lab, hardware, and software.

The core of the design is **BiChromaLogic**, a light-controlled genetic circuit built on
CRISPR-based logic gates. It takes **2 light inputs** and converts them into **4 distinct
sensor proteins on demand** — so the device can be reprogrammed for a target by changing
illumination rather than by rebuilding the biology.

Tools and techniques: CRISPR-i/a, optogenetics, confocal microscopy, Python, R, GROMACS,
AlphaFold3.

### Genetic circuit

{{< figure src="images/projects/igem/igem-07-optogenetic-logic-circuit.png"
  caption="Optogenetic logic circuit design." >}}

### Wet lab

{{< figure src="images/projects/igem/igem-01-wetlab-design.png"
  caption="Wet lab design." >}}

### Modelling

{{< figure src="images/projects/igem/igem-02-model-design.png"
  caption="Model design." >}}

{{< figure src="images/projects/igem/igem-03-molecular-design-kinetics.png"
  caption="Molecular design and kinetic modelling." >}}

{{< figure src="images/projects/igem/igem-05-strand-replacement-simulation.png"
  caption="Dispersion and device-level simulation of the strand-replacing reaction." >}}

{{< figure src="images/projects/igem/igem-06-environment-system-behavior.png"
  caption="Environment and system behaviour." >}}

### Detection module

{{< figure src="images/projects/igem/igem-08-dna-immobilization.png"
  caption="DNA immobilisation." >}}

### Hardware

{{< figure src="images/projects/igem/igem-10-hardware-1.png"
  caption="Device hardware." >}}

{{< figure src="images/projects/igem/igem-11-hardware-2.png"
  caption="Device hardware, continued." >}}

## Results

- **Circuit performance:** 169% activation and 92% repression efficiency across the logic
  gates.
- **Competition outcome:** Silver Medal at iGEM 2025 as ZJU-China.
- The work also became the basis of an eDNA-based aquatic pathogen detection entry that
  took a Gold Medal at Zhejiang University's 18th "Dandelion" Undergraduate Innovation
  Competition.

{{< figure src="images/projects/igem/igem-04-atf-reprogramming.png"
  caption="Progress on aTF reprogramming." >}}

{{< figure src="images/projects/igem/igem-09-detection-model-result.png"
  caption="Detection model results." >}}
