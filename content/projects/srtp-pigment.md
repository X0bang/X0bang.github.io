---
title: "A Sustainable Pigment Biosynthesis System"
date: 2025-03-01
year: "2025"
weight: 5
selected: true
venue: "ZJU"
venueLogo: "images/logos/zju.svg"
lab: "Chen Lab"
status: "Outstanding"
thumb: "images/projects/srtp-design.png"
authors: "Advised by [Prof. Ming Chen](https://person.zju.edu.cn/en/0005111)"
tags: ["metabolic engineering", "SRTP", "synthetic biology"]
links:
  - name: "Wiki"
    url: "https://2024.igem.wiki/zju-china/"
summary: "Engineering vioE activity and pathway flux for pigment yield, with light- and quorum-controlled circuits that make the output switchable."
draft: false
---

{{< figure src="images/projects/srtp-logo-neovio-dye.png" width="220px"
  alt="Neovio Dye" >}}

## Background

Microbial pigment production offers a route away from petrochemical dyes, but it has to
clear two bars at once: the pathway must be productive enough to be worth running, and the
output must be controllable rather than constitutive.

This Provincial SRTP grant project addressed both — enzyme and flux engineering for yield,
and genetic circuit design for control.

## Method

**Enzyme and metabolic engineering.** Semi-rational design combined with MD simulation was
used to improve the pathway enzyme **vioE**, while genome-scale metabolic modelling (GSMM)
identified knockout targets to redirect flux.

**Genetic circuit design.** I built dual orthogonal quorum-sensing circuits together with a
blue-light-inducible split-Cre system, so pigment output can be switched programmably and
reversibly.

Tools: GROMACS, LC-MS, SnapGene, GSMM, Python, R, optogenetics.

{{< figure src="images/projects/srtp-design.png"
  caption="System design: enzyme and flux engineering alongside the quorum-sensing and blue-light control circuits." >}}

{{< figure src="images/projects/srtp-cre-memory-system.png"
  caption="The Cre excision memory system." >}}

## Results

- A **vioE mutant with +32% activity**, identified through semi-rational design and MD
  simulation.
- **Two gene knockouts** from genome-scale metabolic modelling, giving **+48% and +23%**
  yield improvements.
- Working **programmable, reversible switching** of pigment output via the combined
  quorum-sensing and blue-light split-Cre circuits.

{{< figure src="images/projects/srtp-result.png"
  caption="Results across the engineered strains." >}}

{{< figure src="images/projects/srtp-metabolic-quorum-validation.png"
  caption="Validation of the metabolic engineering and the dual orthogonal quorum-sensing system." >}}

_Supported by a Provincial SRTP Research Grant (Zhejiang Provincial Department of Science
and Technology, 12,000 RMB), and rated Outstanding._
