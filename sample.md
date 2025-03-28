---
title: "SplatOverflow: Asynchronous Hardware Troubleshooting"
venue: to appear at ACM CHI 2025
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
preprint: https://arxiv.org/abs/2411.02332
video: https://youtu.be/rdtaUo2Lo38
publication: null
code: null 
---

<figure>
  <src>assets/figone.png</src>
  <alt>Figure 1</alt>
  <caption>
    _Figure 1._ _(a)_ A SplatOverflow scene, comprising a 3D Gaussian Splat aligned and registered onto a digital CAD model, acting as a boundary object to facilitate asynchronous troubleshooting tasks for hardware. _(b)_ A remote maintainer using SplatOverflow to explore a local user's hardware and author instructions for them to follow. _(c)_ A local user viewing the maintainer's instructions rendered as an overlay onto their hardware in their workspace and performing the specified action.
  </caption>
</figure>

## Abstract

As tools for designing and manufacturing hardware become more accessible, smaller producers can develop and distribute novel hardware. However, there aren't established tools to support end-user hardware troubleshooting or routine maintenance. As a result, technical support for hardware remains ad-hoc and challenging to scale. Inspired by software troubleshooting workflows like StackOverflow, we propose a workflow for asynchronous hardware troubleshooting: SplatOverflow. SplatOverflow creates a novel boundary object, the SplatOverflow scene, that users reference to communicate about hardware. The scene comprises a <sidenote><text>3D Gaussian Splat</text><note>[3D Gaussian Splatting [Kerbl et al. 2023]](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/) is a view-interpolation and rasterization technique that renders a 3D scene as a collection of Gaussian distributions.</note></sidenote> of the user's hardware registered onto the hardware's CAD model. The splat captures the current state of the hardware, and the registered CAD model acts as a referential anchor for troubleshooting instructions. With SplatOverflow, maintainers can directly address issues and author instructions in the user's workspace. The instructions define workflows that can easily be shared between users and recontextualized in new environments. In this paper, we describe the design of SplatOverflow, detail the workflows it enables, and illustrate its utility to different kinds of users. We also validate that non-experts can use SplatOverflow to troubleshoot common problems with a 3D printer in a user study.

## Demonstrative Examples

We demonstrate SplatOverflow with a variety of hardware examples, including a pick-and-place machine, a 3D printer, and an open-source e-reader.

<figure>
  <src>assets/opulo-orbit.mp4</src>
  <alt>Figure 2</alt>
  <caption>
    _Figure 2._ A SplatOverflow scene of a pick-and-place machine, the Opulo Lumen V3 registered onto it's CAD model rendered as a yellow wireframe. For a detailed example of troubleshooting a problem on this pick-and-place using SplatOverflow, please see our video or read the Walkthrough section of our paper.
  </caption>
</figure>

<figure>
  <src>assets/prusa-orbit.mp4</src>
  <alt>Figure 3</alt>
  <caption>
    _Figure 3._ A SplatOverflow scene of a 3D printer, the Prusa MK3S+ registered onto it's CAD model rendered as a yellow wireframe. Our evaluation examined whether non-experts could use SplatOverflow to troubleshoot common problems with this printer. For more details, please read the Evaluation section of our paper.
  </caption>
</figure>

<figure>
  <src>assets/openbook-traces-and-pads.png</src>
  <alt>Figure 4</alt>
  <caption>
    _Figure 4._ A still of a SplatOverflow scene depicting the PCB for an open-source e-reader, the Open Book registered onto it's CAD model. In _(a)_ electrical traces from the PCB layout are overlaid onto the board as a yellow wireframe. In _(b)_ electrical pads are highlighted.
  </caption>
</figure>

## Source Code & Documentation

The source code and accompanying technical documentation of our implementation will be available shortly under a `CC BY-SA` license. If you'd like access before the public release, please reach out using the email address below.

## BibTex

```
@misc{kwatra2024splatoverflowasynchronoushardwaretroubleshooting,
    title={SplatOverflow: Asynchronous Hardware Troubleshooting}, 
    author={Amritansh Kwatra and Tobias Wienberg and Ilan Mandel and Ritik Batra 
            and Peter He and Francois Guimbretiere and Thijs Roumen},
    year={2024},
    eprint={2411.02332},
    archivePrefix={arXiv},
    primaryClass={cs.HC},
    url={https://arxiv.org/abs/2411.02332}, 
}
```

## Acknowledgements

We would like to thank the [Digital Life Initiative](https://dli.tech.cornell.edu/) at Cornell Tech for supporting this work through a doctoral fellowship. We would also like to thank Joey Castillo, Frank Bu and Stephen Hawes for taking part in preliminary discussions that helped motivate this work.

## Contact

If you have questions about this work, contact Amrit Kwatra: `ak2244 at cornell dot edu`.





