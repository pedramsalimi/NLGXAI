# Towards feasible counterfactual explanations: a taxonomy guided template-based NLG method
# Overview
This repository contains the implementation and resources for our research on counterfactual explanations in Explainable AI. Our work introduces a  Natural Language Generation (NLG) method tailored for generating sentence-level counterfactual explanations using Feature Actionability Taxonomy (FAT). This project is part of the iSee initiative and has been accepted for presentation at ECAI 2023.

# Main Contributions
our main contribution lies in introducing a template-based natural language generation method tailored for sentence-level counterfactual explanations. By integrating a taxonomy with feature attribution weights, we've enabled the selection of NLG templates compatible with explainers like DICE, NICE, and DisCERN.​

📄 Paper: https://rgu-repository.worktribe.com/output/2015280
🎥 Video Presentation: [Watch on YouTube](https://youtu.be/7Ti2354ohkk)

# Citation:
@inproceedings { ,
	title = {Towards feasible counterfactual explanations: a taxonomy guided template-based NLG method.},
	abstract = {Counterfactual Explanations (cf-XAI) describe the smallest changes in feature values necessary to change an outcome from one class to another. However, presently many cf-XAI methods neglect the feasibility of those changes. In this paper, we introduce a novel approach for presenting cf-XAI in natural language (Natural-XAI), giving careful consideration to actionable and comprehensible aspects while remaining cognizant of immutability and ethical concerns. We present three contributions to this endeavor. Firstly, through a user study, we identify two types of themes present in cf-XAI composed by humans: content-related, focusing on how features and their values are included from both the counterfactual and the query perspectives; and structure-related, focusing on the structure and terminology used for describing necessary value changes. Secondly, we introduce a feature actionability taxonomy with four clearly defined categories, each accompanied by an example, to streamline the explanation presentation process. Using insights from the user study and our taxonomy, we created a generalisable template-based natural language generation (NLG) method compatible with existing explainers like DICE, NICE, and Dis-CERN, to produce counterfactuals that address the aforementioned limitations of existing approaches. Finally, we conducted a second user study to assess the performance of our taxonomy-guided NLG templates on three domains. Our findings show that the taxonomyguided Natural-XAI approach (n-XAIT ) received higher user ratings across all dimensions, with significantly improved results in the majority of the domains assessed for articulation, acceptability, feasibility, and sensitivity dimensions.},
	conference = {26th European conference on artificial intelligence 2023 (ECAI-2023)},
	note = {INFO INCOMPLETE (Info of acceptance from contact 19/7/2023 LM)
PERMISSION GRANTED (version = AAM; embargo = none; licence = BY-NC; POLICY =  https://www.iospress.com/article-sharing-policy 20/7/2023 LM)
DOCUMENT READY (AAM rec'd 19/7/2023 LM)
ADDITIONAL INFO - Contact: Pedram Salimi; Nirmalie Wiratunga; David Corsar; Anjana Wijekoon

Set Statement:  (© [name of author, year]. The definitive, peer reviewed and edited version of this Article  is published in [book title, editor(s), print ISBN or online ISBN, pages, year, and DOI or URL]. These details can be found on https://ebooks.iospress.nl.)},
	publicationstatus = {Accepted},
	publisher = {IOS Press},
	url = {https://rgu-repository.worktribe.com/output/2015280},
	keyword = {Counterfactual explanation, Natural-XAI method, Feature actionability taxonomy (FAT), Actionability knowledge;},
	author = {Salimi, Pedram and Wiratunga, Nirmalie and Corsar, David and Wijekoon, Anjana}
}


