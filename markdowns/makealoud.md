---
title: "MakeAloud: Think-Aloud to Bridge Design-Fabrication Workflows"
authors:
  - name: "Ritik Batra"
    affiliation: ["Autodesk Research", "Cornell Tech"]
  - name: "Kendra Wannamaker"
    affiliation: "Autodesk Research"
  - name: "George Fitzmaurice"
    affiliation: "Autodesk Research"
  - name: "Justin Matejka"
    affiliation: "Autodesk Research"
venue: To Appear in Proceedings of Designing Interactive Systems Conference (DIS’26)
award: Honorable Mention for Best Paper
links:
  # preprint: https://arxiv.org/abs/2506.10891
  publication: null
  video: https://youtu.be/bSumxAIxTPw
  # presentation: https://youtu.be/ufHH9f9QcOA?si=6qkRVySBlI4hxEjw
---

## Abstract

Translating Computer-Aided Design (CAD) models into physical objects requires expertise and adjustments to navigate fabrication constraints. Makers develop this tacit knowledge by understanding materials, techniques, and practical requirements. Adjustments are typically shared with designer collaborators through sketches and text. However, this documentation lacks situated knowledge gained during fabrication and remains disconnected from the model.

To explore how computational tools could address these limitations, we developed _MakeAloud_, a design probe leveraging AI to capture makers' in-situ knowledge with hand-tracking hardware and think-aloud computing and then generate design insights within collaborators' CAD tools. Through a study with woodworkers and designers, we identify three design considerations for designer-maker collaboration tools: surfacing fabrication constraints in CAD to preserve designer intent, supporting asymmetrical domain expertise through AI-mediated communication, and building collective fabrication knowledge archives. This work contributes empirical insights into how AI can bridge design and fabrication workflows, offering pathways for cross-disciplinary collaboration.

<figure>
  <src>assets/makealoud/teaser.png</src>
  <alt>This teaser figure shows that in subfigure A, a woodworker capture their workflows by talking out loud ("The designer did not add joints"). The mobile device on an auto-tracking stand then interrupts them ("What joint do you suggest"). The woodworker then responds with "Dovetail joints." Some other examples of captured knowledge by the maker talking out loud are "My hand router is not working" and "Wooden designs need tolerances." In subfigure B, the designer can access this information within Autodesk Fusion (CAD tool) by asking "What joints did they suggest" and then the tool would respond with "Dovetail joints. Here is how to add them to the model" while referencing a specific part of the model.</alt>
  <caption>
    Workflow illustrating how designers and makers can collaborate using _MakeAloud_ (orange). (a) During the fabrication workflow, the maker (blue) captures their situated knowledge with _MakeAloud_ video recording them and their think-aloud utterances. (b) The designer (green) can then use _MakeAloud_ in Autodesk Fusion to generate insights from the captured fabrication workflow and receive guidance on how to adjust the CAD model based on the maker's fabrication constraints.
  </caption>
</figure>

## BibTex

```
@inproceedings{batra2026makealoud,
  title={MakeAloud: Think-Aloud to Bridge Design-Fabrication Workflows},
  author={Batra, Ritik and Wannamaker, Kendra and Fitzmaurice, George and Matejka, Justin},
  booktitle={Proceedings of the 2026 ACM Designing Interactive Systems Conference},
  year={2026}
}
```

## Acknowledgements

We would like to thank the 12 maker and designer participants for sharing their expertise and insights with us. We also thank John Thompson, Jo Vermeulen, Frederic Gmeiner, Kathy Cheng, Evgeny Stemasov, Sebastian Bidegain, Niti Parikh, and Amritansh Kwatra for brainstorming with us, helping with pilot studies, and providing feedback on the paper.

This page was created using the open-source [Tufte Project Template](https://github.com/tansh-kwa/tufte-project-template).

## Contact

If you have questions about this work, contact Ritik Batra: `ritik at infosci dot cornell dot edu`

