---
title: "texTENG: Fabricating Wearable Textile-Based Triboelectric Nanogenerators"
venue: To Appear in Proceedings of the 2025 ACM Augmented Humans (AH'25)
award: Best Paper Award
authors:
  - name: "Ritik Batra"
    affiliation: "Cornell University"
  - name: "Narjes Pourjafarian"
    affiliation: "Cornell University"
  - name: "Samantha Chang"
    affiliation: "Cornell University"
  - name: "Margaret Tsai"
    affiliation: "Cornell University"
  - name: "Jacob Revelo"
    affiliation: "Cornell University"
  - name: "Cindy Hsin-Liu Kao"
    affiliation: "Cornell University"
links:
  preprint: https://arxiv.org/abs/2503.12628
  video: null
  publication: null
  code: null
---

<figure>
  <src>assets/texteng/teaser.png</src>
  <alt>Figure 1</alt>
  <caption>
    _Figure 1:_ We introduce texTENG, a DIY-friendly framework for fabricating textile-based wearable devices capable of both sensing and power harvesting on the body. Compatible with diverse fabrication approaches and commercially available materials, our menu offers versatility and considerations for the design process. Our application examples demonstrate _(a)_ an interactive bracelet for sending emergency messages, _(b)_ a smart hair extension for activating voice assistants, _(c)_ a touch-sensitive drawstring for light control, _(d)_ a game controller utilizing a woven flex sensor, _(e)_ self-powered touch sensors for music player control, _(f)_ energy storage from smart garments to power a digital watch, _(g)_ energy harvesting from smart socks to power running lights, and_(h)_ wireless interaction enabled by a knit elbow patch.
  </caption>
</figure>

## Abstract

Recently, there has been a surge of interest in sustainable energy sources, particularly for wearable computing. Triboelectric nanogenerators (TENGs) have shown promise in converting human motion into electric power. Textile-based TENGs, valued for their flexibility and breathability, offer an ideal form factor for wearables. However, uptake in maker communities has been slow due to commercially unavailable materials, complex fabrication processes, and structures incompatible with human motion. This paper introduces texTENG, a textile-based framework simplifying the fabrication of power harvesting and self-powered sensing applications. By leveraging accessible materials and familiar tools, texTENG bridges the gap between advanced TENG research and wearable applications. We explore a design menu for creating multidimensional TENG structures using braiding, weaving, and knitting. Technical evaluations and example applications highlight the performance and feasibility of these designs, offering DIY-friendly pathways for fabricating textile-based TENGs and promoting sustainable prototyping practices within the HCI and maker communities.

## Background: Triboelectric Nanogenerators

texTENG operates based on triboelectric nanogenerators (TENGs), which convert mechanical energy into electricity for sensing and harvesting.

<figure>
  <src>assets/texteng/background.png</src>
  <alt>Figure 2</alt>
  <caption>
    _Figure 2:_ _(Left)_ Operational principle of TENGs;_(Center)_ Four fundamental operating modes of TENGs;_(Right)_ Different types of TENGs based on the bonding between electrodes and tribo layers.
  </caption>
</figure>

## Design Menu

For the fabrication of textile-based TENGs, we have distilled a design menu for user-friendly fabrication.

<figure>
  <src>assets/texteng/designMenu.png</src>
  <alt>Figure 3</alt>
  <caption>
    _Figure 3:_ Design Menu of texTENG includes_(a)_ commercially available triboelectric materials and textile structures for fabricating textile-based TENGs, including_(b)_ 1D yarn-level structure, _(c)_ 2D textile structures, and _(d)_ 2.5D textile structures. Materials are ordered based on our experiments and insights from Liu et al. (Since separating the electrode from the tribo layer does not enhance TENG performance, we opted not to incorporate single-electrode 2.5D structures in our implementation).
  </caption>
</figure>

## Fabrication Methods

Our exploration involved identifying user-friendly fabrication approaches suitable for texTENG.

<figure>
  <src>assets/texteng/1d.png</src>
  <alt>Figure 4</alt>
  <caption>
    _Figure 4._ DIY techniques for fabricating yarn-based TENGs (blue and yellow represent positive and negative tribo yarns, respectively, on the triboelectric series, gray represent conductive yarns, and purple represent non-functional yarn).
  </caption>
</figure>

<figure>
  <src>assets/texteng/fab.jpg</src>
  <alt>Figure 5</alt>
  <caption>
    _Figure 5._ Techniques for fabricating _(a)_ 1D yarn-based TENGs with a DIY braiding tool, _(b)_ 2D single-layer woven structures, _(c)_ 2D multilayer woven structures, _(d)_ 2D single-layer knit structures,_(e)_ 2D knit CS structures, _(f-h)_ 2.5D woven structures on the floor loom, and _(i-l)_ 2.5D Ottoman Stitch knit structures_(blue, yellow, purple, and gray represent positive, negative, non-functional, and insulated conductive yarns,respectively)_.
  </caption>
</figure>

## BibTex

```
@misc{batra2025texteng,
    title={texTENG: Fabricating Wearable Textile-Based Triboelectric Nanogenerators},
    author={Ritik Batra and Narjes Pourjafarian and Samantha Chang and Margaret Tsai and Jacob Revelo and Cindy Hsin-Liu Kao},
    year={2025},
    eprint={2503.12628},
    archivePrefix={arXiv},
    primaryClass={cs.HC},
    url={https://arxiv.org/abs/2503.12628}
}
```

## Acknowledgements

We would like to thank Heather Kim, Jingwen Zhu, and Pin-Sung Ku for their support and advising during the course of this project. We also would like to thank Melissa Conroy for teaching us the knitting fundamentals and Sam Xia Zeng for assisting us with evaluations.

This page was created using the open-source [Tufte Project Template](https://github.com/tansh-kwa/tufte-project-template).

## Contact

If you have questions about this work, contact Ritik Batra: `ritik at infosci dot cornell dot edu`.

