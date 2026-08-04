---
title: "Trimeric Redesign of a CAR-T Costimulatory Transmembrane Domain"
date: 2026-06-01
year: "2026"
weight: 1
selected: true
venue: "UniMelb, WEHI"
venueLogo: "images/logos/unimelb.png, images/logos/wehi.png"
status: "Ongoing"
thumbPoster: "images/projects/procar3-poster.jpg"
thumb: "images/projects/procar3-trimer.mp4"
authors: "Supervised by Dr. Emma Petley · PIs: [Prof. Matt Call](https://www.wehi.edu.au/researcher/matt-call/) & [A/Prof. Melissa Call](https://www.wehi.edu.au/researcher/melissa-call/)"
tags: ["protein engineering", "structural biology", "molecular dynamics"]
links:
  - name: "Program"
    url: "https://www.wehi.edu.au/education/undergraduate/inspire/"
summary: "Redesigning a CAR-T costimulatory transmembrane domain back into its native trimeric form, screened by all-atom and coarse-grained MD with free-energy calculations, and validated by flow cytometry and degranulation assays."
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

**Dry lab — computational screening.** Four candidate designs went through four
complementary routes: 500 ns all-atom trimer simulations to test whether each assembly
holds, umbrella sampling for the free energy of lateral assembly, coarse-grained runs
started from separated helices to see whether they find each other unaided, and a separate
insertion free energy for the single helix. GROMACS throughout, with Rosetta and ESM2
guiding and scoring the designs.

**Wet lab — functional validation.** Collaborating with the team, I helped optimise 4 TMD
variants, then ran flow cytometry and degranulation assays against 2 tumour cell lines,
confirming surface expression before measuring function.

Techniques: flow cytometry, degranulation assay, HEK293T culture, GROMACS, ΔG prediction,
Rosetta, ESM2.

## Computational strategy

A single simulation cannot separate "the trimer never forms" from "it forms but the protein
never reaches the surface", so the question is split across four routes that answer
different halves of it — assembly on one side, membrane insertion on the other.

{{< figure src="images/projects/wehi/strategy-overview.png"
  caption="Four routes from one question. All-atom MD tests whether each design holds together; the other three attack the free energy of assembly and of insertion separately." >}}

Each variant is built as a full membrane system — trimer, bilayer, water and ions — in
CHARMM-GUI, then equilibrated in stages before production.

{{< figure src="images/projects/wehi/system-setup.png"
  caption="The four candidate designs, each embedded in an explicit lipid bilayer with water and counter-ions." >}}

For the assembly free energy, one chain is pulled away from the other two in the plane of
the membrane and the path is sampled with a series of umbrella windows.

{{< figure src="images/projects/wehi/umbrella-strategy.png"
  caption="Steered dynamics pulls chain A from the B+C dimer in-plane; 29 umbrella windows are placed along that path." >}}

A coarse-grained model runs the complementary experiment: start the three helices apart and
see whether they find each other on their own.

{{< figure src="images/projects/wehi/cg-method.png"
  caption="Coarse-grained self-assembly — three separated helices, free to diffuse in the bilayer over 10 µs." >}}

## Results

The designed trimers are real. All four all-atom trajectories converge and stay converged,
and the interfaces hold rather than drifting apart over the run.

{{< figure src="images/projects/wehi/md-convergence.png"
  caption="Backbone RMSD, radius of gyration, helix crossing angle and buried interface area across the four designs — all four converge and remain stable." >}}

Contact between neighbouring chains is maintained at a high level throughout, and stays
that way from the early window to the late one.

{{< figure src="images/projects/wehi/contact-occupancy.png"
  caption="Contact occupancy per design, early window against late, with the per-chain symmetry of each interface." >}}

Together with the wet-lab result — **73–74% surface expression** and T cell activation in
the degranulation assay — this says the redesigned TMD both assembles and reaches the
surface in working form.

The project is ongoing. The current focus is a functional comparison against the
conventional 4-1BBζ architecture, and the free-energy work above is still being refined.

_Fully funded through the InSPIRE program at the Walter and Eliza Hall Institute, the
Department of Medical Biology of the University of Melbourne._
