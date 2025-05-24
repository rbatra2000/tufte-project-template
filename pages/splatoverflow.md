---
title: "SplatOverflow: Asynchronous Hardware Troubleshooting"
venue: To Appear in Proceedings of the 2025 ACM Computer-Human Interaction Conference (CHI’25)
award: Honorable Mention for Best Paper
authors:
  - name: "Amritansh Kwatra"
    affiliation: "Cornell Tech"
  - name: "Tobias Weinberg"
    affiliation: "Cornell Tech"
  - name: "Ilan Mandel"
    affiliation: "Cornell Tech"
  - name: "Ritik Batra"
    affiliation: "Cornell Tech"
  - name: "Peter He"
    affiliation: "Cornell University"
  - name: "Francois Guimbretiere"
    affiliation: "Cornell University"
  - name: "Thijs Roumen"
    affiliation: "Cornell Tech"
links:
  preprint: https://arxiv.org/abs/2411.02332
  video: https://youtu.be/rdtaUo2Lo38
  presentation: https://www.youtube.com/watch?v=-LABTmOn7mU
  publication: https://dl.acm.org/doi/10.1145/3706598.3714129
  code: null
---

<figure>
  <src>../imgs/figone.png</src>
  <alt>Figure 1</alt>
  <caption>
    _Figure 1._ _(a)_ A SplatOverflow scene, comprising a 3D Gaussian Splat aligned and registered onto a digital CAD model, acting as a boundary object to facilitate asynchronous troubleshooting tasks for hardware. A local end-user can query technical documentation and past issues associated with the hardware by simply clicking on the parts in the SplatOverflow scene. If no solution is found, they can use SplatOverflow to request and receive help asynchronously from a remote maintainer. _(b)_ A remote maintainer uses SplatOverflow to explore a local end-user's hardware and author instructions for them to follow. _(c)_ A local end-user views the maintainer's instructions rendered as an overlay onto their hardware in their workspace and executes the specified action.
  </caption>
</figure>

## Abstract

Compared to the plethora of software tools that support _designing_ hardware, there are relatively few tools that support _troubleshooting_ and _maintaining_ hardware. As a result, providing technical support for hardware is often ad-hoc and challenging to scale. Inspired by software troubleshooting workflows like StackOverflow, we propose a workflow for asynchronous hardware troubleshooting: SplatOverflow. SplatOverflow creates a novel boundary object that scaffolds asynchronous communication about hardware between multiple users. A SplatOverflow scene comprises a <sidenote><text>3D Gaussian Splat</text><note>[3D Gaussian Splatting [Kerbl et al. 2023]](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/) is a view-interpolation and rasterization technique that renders a 3D scene as a collection of Gaussian distributions.</note></sidenote> of the end-user's hardware registered onto the hardware's CAD model. These two elements enable multiple users to remotely and independently inspect a hardware instance, easily compare the hardware instance to it's design or associated documentation, and communicate actions or instructions the end-user must carry out. SplatOverflow links these comments, instructions and discussions to the CAD parts they reference and stores them for future users to easily query and access. Similar to StackOverflow, this allows communities of users to build pools of shared technical knowledge about the hardware they are all using. In the paper accompanying this project, we describe the design of SplatOverflow, detail the workflows it enables, and explain its utility to different kinds of users. We also validate that non-experts can use SplatOverflow to troubleshoot common problems with a 3D printer in a user study.

<!-- As tools for designing and manufacturing hardware become more accessible, smaller producers can develop and distribute novel hardware. However, there aren't established tools to support end-user hardware troubleshooting or routine maintenance. As a result, technical support for hardware remains ad-hoc and challenging to scale. Inspired by software troubleshooting workflows like StackOverflow, we propose a workflow for asynchronous hardware troubleshooting: SplatOverflow. SplatOverflow creates a novel boundary object, the SplatOverflow scene, that users reference to communicate about hardware. The scene comprises a <sidenote><text>3D Gaussian Splat</text><note>[3D Gaussian Splatting [Kerbl et al. 2023]](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/) is a view-interpolation and rasterization technique that renders a 3D scene as a collection of Gaussian distributions.</note></sidenote> of the user's hardware registered onto the hardware's CAD model.  With SplatOverflow, maintainers can directly address issues and author instructions in the user's workspace. The instructions define workflows that can easily be shared between users and recontextualized in new environments. In this paper, we describe the design of SplatOverflow, detail the workflows it enables, and illustrate its utility to different kinds of users. We also validate that non-experts can use SplatOverflow to troubleshoot common problems with a 3D printer in a user study. -->

## Demonstrative Examples

We demonstrate SplatOverflow with a variety of hardware examples, including a pick-and-place machine (the [LumenPnP v3, by Opulo](https://docs.opulo.io/semi-assembly/)), a 3D printer (the [Prusa MK3S+](https://help.prusa3d.com/manual/original-prusa-i3-mk3s-kit-assembly_1128)), and an open-source e-reader ([The Open Book, by Oddly Specific Objects](https://www.oddlyspecificobjects.com/projects/openbook/)).

<figure>
  <src>../video/opulo-orbit.mp4</src>
  <alt>Figure 2</alt>
  <caption>
    _Figure 2._ A SplatOverflow scene of a pick-and-place machine, the Opulo Lumen V3 registered onto it's CAD model rendered as a yellow wireframe. For a detailed example of troubleshooting a problem on this pick-and-place using SplatOverflow, please see our video or read the Walkthrough section of our paper.
  </caption>
</figure>

<figure>
  <src>../video/prusa-orbit.mp4</src>
  <alt>Figure 3</alt>
  <caption>
    _Figure 3._ A SplatOverflow scene of a 3D printer, the Prusa MK3S+ registered onto it's CAD model rendered as a yellow wireframe. Our evaluation examined whether non-experts could use SplatOverflow to troubleshoot common problems with this printer. For more details, please read the Evaluation section of our paper.
  </caption>
</figure>

<figure>
  <src>../imgs/openbook-traces-and-pads.png</src>
  <alt>Figure 4</alt>
  <caption>
    _Figure 4._ A still of a SplatOverflow scene depicting the PCB for an open-source e-reader, the Open Book registered onto it's CAD model. In _(a)_ electrical traces from the PCB layout are overlaid onto the board as a yellow wireframe. In _(b)_ electrical pads are highlighted.
  </caption>
</figure>


## Source Code & Documentation

The source code and accompanying technical documentation of our implementation will be available shortly under a `CC BY-SA` license. If you'd like access before the public release, please reach out using the email address below.

## BibTex

```
@inproceedings{kwatra2024splatoverflow,
author = {Kwatra, Amritansh and Weinberg, Tobias M and Mandel, Ilan and Batra, Ritik and He, Peter and Guimbretiere, Francois and Roumen, Thijs},
title = {SplatOverflow: Asynchronous Hardware Troubleshooting},
year = {2025},
isbn = {9798400713941},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3706598.3714129},
doi = {10.1145/3706598.3714129},
booktitle = {Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems},
articleno = {450},
numpages = {16},
keywords = {Hardware Maintenance, Repair, Troubleshooting},
series = {CHI '25}
}
```

## Acknowledgements

We would like to thank the [Digital Life Initiative](https://dli.tech.cornell.edu/) at Cornell Tech for supporting this work through a doctoral fellowship. We would also like to thank Joey Castillo, Frank Bu and Stephen Hawes for taking part in preliminary discussions that helped motivate this work.

This page was created using the open-source [Tufte Project Pages](https://github.com/tansh-kwa/tufte-project-template) template.

## Contact

If you have questions about this work, contact Amrit Kwatra: `ak2244 at cornell dot edu`.
