This repository contains a taxonomy of counterfactual categories and information about the associated templates. The taxonomy classifies features into two broad categories: Immutable and Mutable, based on their actionability in a counterfactual scenario. Mutable features are further divided into two subcategories: Mutable directly and Mutable indirectly, depending on whether or not the user can directly change the feature. Immutable features are also classified into two subcategories: Restricted Immutable and Immutable regular. Restricted Immutable features are those that cannot be suggested for change, as they may be offensive or sensitive, such as race. Immutable regular features refer to other regular immutable features, such as the number of accounts a user has opened in the previous year.

This taxonomy provides a comprehensive classification of features that can be used as a guideline for creating counterfactuals. In addition to the taxonomy, this repository also contains templates for generating natural language explanations based on the counterfactual categories. These templates provide a structured approach for generating coherent and understandable explanations, making it easier for users to understand the counterfactual scenarios. This information can be used as a reference by contributors who wish to add their own datasets to the repository, ensuring that the information is structured and consistent with the taxonomy and templates provided.

Features
|-- Immutable
|   |-- Restricted Immutable
|   |   |-- Race
|   |   |-- Ethnicity
|   |   `-- ...
|   `-- Immutable regular
|       |-- Age
|       |-- Education level
|       |-- Number of accounts opened in the previous year
|       `-- ...
`-- Mutable
    |-- Mutable directly
    |   |-- Loan amount
    |   |-- Interest rate
    |   `-- ...
    `-- Mutable indirectly
        |-- Credit score
        |-- Working hours per week
        `-- ...

To ensure well-structured templates for counterfactual explanations, a user study was conducted to analyze the key ideas in generating natural language counterfactual explanations. Four categories of information were extracted from the study, including the use of both previous and counterfactual feature values in the explanation, only mentioning counterfactual values, using a wide variety of changing words, and the use of ordinal adverbs or bullet-pointing for ease of understanding. Based on these four categories, four templates were created that can incorporate any of the aforementioned characteristics.

The templates can be categorized into two that use paragraph-like explanations and two that use ordinal adverbs. Each of the templates is able to handle the taxonomy of actionable and immutable features, as well as using a diverse range of words for increasing variability in the explanation. Additionally, each template starts with an initial sentence (prologue) that mentions the number of actionable features that the user can change, and ends with a domain-specific epilogue. For instance, in the health domain, the template might end with "Stay healthy!" while in the financial domain, the template might conclude with "Good luck with your loan!".

So now details about templates:
1. paragraph-based explanations:
	1. mutable directly:
		both previous and counterfactual values: {CHANGING_TERM} {FEATURE} from {PREVIOUS_VALUE} to {COUNTERFACTUAL_VALUE}
		only counterfactual values: {CHANGING_TERM} {FEATURE} to {COUNTERFACTUAL_VALUE}
	2. mutable indirectly: 
		both previous and counterfactual values: take steps to {CHANGING_TERM} {FEATURE} from {PREVIOUS_VALUE} to {COUNTERFACTUAL_VALUE}
		only counterfactual values: take steps to {CHANGING_TERM} {FEATURE} to {COUNTERFACTUAL_VALUE}
	3. Immutable restricted:
		{FEATURE} {COUNTERFACTUAL_VALUE} has a higher chance to  {DESIRED_STATEMENT} compared to {FEATURE} {PREVIOUS_VALUE} 
	4. Immutable regular:
		Your {FEATURE} has a contribution to {UNDESIRED_CLASS}

Paragraph-based explanations
├── Mutable directly
│   ├── Both previous and counterfactual values
│   │   ├── {CHANGING_TERM} + {FEATURE} + from {PREVIOUS_VALUE} value to {COUNTERFACTUAL_VALUE}
│   │   └── {CHANGING_TERM} + {FEATURE} + to counterfactual value
│   └── Only counterfactual values
│       ├── {CHANGING_TERM} + {FEATURE} + from {PREVIOUS_VALUE} value to {COUNTERFACTUAL_VALUE}
│       └── {CHANGING_TERM} + {FEATURE} + to counterfactual value
├── Mutable indirectly
│   ├── Both previous and counterfactual values
│   │   ├── Take steps to {CHANGING_TERM} + {FEATURE} + from {PREVIOUS_VALUE} value to {COUNTERFACTUAL_VALUE}
│   │   └── Take steps to {CHANGING_TERM} + {FEATURE} + to counterfactual value
│   └── Only counterfactual values
│       ├── Take steps to {CHANGING_TERM} + {FEATURE} + from {PREVIOUS_VALUE} value to {COUNTERFACTUAL_VALUE}
│       └── Take steps to {CHANGING_TERM} + {FEATURE} + to {COUNTERFACTUAL_VALUE}
├── Immutable restricted
│   └── {FEATURE} + {COUNTERFACTUAL_VALUE} + has a higher chance to desired statement compared to {FEATURE} {PREVIOUS_VALUE}
└── Immutable regular
    └── Your {FEATURE} has a contribution to {UNDESIRED_CLASS}

Ordinal-based explanations
├── Mutable directly
│   ├── Both previous and counterfactual values
│   │   ├── \n{INDEX}), {CHANGING_TERM} + {FEATURE} + from {PREVIOUS_VALUE} value to {COUNTERFACTUAL_VALUE}
│   │   └── \n{INDEX}), {CHANGING_TERM} + {FEATURE} + to counterfactual value
│   └── Only counterfactual values
│       ├── \n{INDEX}), {CHANGING_TERM} + {FEATURE} + from {PREVIOUS_VALUE} value to {COUNTERFACTUAL_VALUE}
│       └── \n{INDEX}), {CHANGING_TERM} + {FEATURE} + to counterfactual value
├── Mutable indirectly
│   ├── Both previous and counterfactual values
│   │   ├── \n{INDEX}), Take steps to {CHANGING_TERM} + {FEATURE} + from {PREVIOUS_VALUE} value to {COUNTERFACTUAL_VALUE}
│   │   └── \n{INDEX}), Take steps to {CHANGING_TERM} + {FEATURE} + to counterfactual value
│   └── Only counterfactual values
│       ├── \n{INDEX}), Take steps to {CHANGING_TERM} + {FEATURE} + from {PREVIOUS_VALUE} value to {COUNTERFACTUAL_VALUE}
│       └── \n{INDEX}), Take steps to {CHANGING_TERM} + {FEATURE} + to {COUNTERFACTUAL_VALUE}
├── Immutable restricted
│   └── \nMoreover, {FEATURE} + {COUNTERFACTUAL_VALUE} + has a higher chance to desired statement compared to {FEATURE} {PREVIOUS_VALUE}
└── Immutable regular
    └── \nFurthermore, Your {FEATURE} has a contribution to {UNDESIRED_CLASS}
For each dataset, we provide the following information to ensure well-structured templates:

Prologue: A list of strings that introduces the explanation and provides information about the number of features that are actionable and can be changed by the user.

Starting point: A list of strings that presents the initial state and conditions of the dataset. For example, in a loan application dataset, this could be a sentence such as "Your loan would be approved if...".

Epilogue: A list of strings that concludes the explanation with domain-specific statements. For instance, in a health domain dataset related to heart disease, the epilogue could be "Stay healthy!".

Target class: A string that represents the class that the user wants to achieve or reach with their actions. In a loan application dataset, this could be "Approved".

Undesired class: A string that represents the class that the user wants to avoid or prevent. For example, in a loan application dataset, this could be 'Rejected'.

Desired class: A string that represents the desired outcome of the user's actions. For instance, in a heart disease dataset, this could be 'Having a healthy heart'.

Con_feats: A list of strings that represents the continuous features in the dataset that are actionable and can be changed by the user.

Cat_feats: A list of strings that represents the categorical features in the dataset that are actionable and can be changed by the user.

Feature_categories: A dictionary that maps each feature to its category in the actionable taxonomy (direct, indirect, restricted, or regular).

Undesired statement: A string that represents the undesirable state that the user wants to avoid. In a heart disease dataset, this could be "Having a heart problem".

Desired statement: A string that represents the desirable state that the user wants to achieve. For example, in a heart disease dataset, this could be "Having a healthy heart".

The templates are categorized as paragraph-based or ordinal-adverb-based explanations. For paragraph-based explanations, we have four templates that cover all possible combinations of previous and counterfactual values for mutable features, as well as the two categories of immutable features. For ordinal-adverb-based explanations, we also have four templates that can handle the same feature taxonomy and changing word diversity.

An output example:

In order to prevent you from heart problems you would need to change 5 attributes.
You would not get heart problem if you, 
1), increase cp to 2.0. 
2), take steps to lower trestbps to 108.0 and, 
3), lower chol to 243.0. 
4), lower thalach to 152.0. 
5), decrease oldpeak to 0.0. 
Furthermore, Your age has a contribution to have a heart problem. 
Moreover, sex Male has a higher chance to  have a healthy heart compared to sex Female and, Take care!

We hope that this information will be helpful for users who wish to contribute datasets and work with our code.
