# Taxonomy of Feature Actionability
This repository contains a taxonomy of counterfactual categories and information about the associated templates. The taxonomy classifies features into two broad categories: Immutable and Mutable, based on their actionability in a counterfactual scenario. Mutable features are further divided into two subcategories: Mutable directly and Mutable indirectly, depending on whether or not the user can directly change the feature. Immutable features are also classified into two subcategories: Sensitive Immutable and Immutable regular. Sensitive Immutable features are those that cannot be suggested for change, as they may be offensive or sensitive, such as race. Immutable regular features refer to other regular immutable features, such as the number of accounts a user has opened in the previous year.

This taxonomy provides a comprehensive classification of features that can be used as a guideline for creating counterfactuals. In addition to the taxonomy, this repository also contains templates for generating natural language explanations based on the counterfactual categories. These templates provide a structured approach for generating coherent and understandable explanations, making it easier for users to understand the counterfactual scenarios. This information can be used as a reference by contributors who wish to add their own datasets to the repository, ensuring that the information is structured and consistent with the taxonomy and templates provided.
```
Feature Actionability Taxonomy
- Immutable
  Definition: Incapable of being changed or modified
  - Immutable Sensitive (I.S.)
     Definition: A feature whose value cannot be modified,
                 and should (normally) not be suggested as changeable
                 as this may cause offense to the recipient
     Example: race/ethnicity in Student dataset
  - Immutable Non-sensitive (I.NS.)
     Definition: A feature whose value cannot be modified
                 by any action the recipient can take
     Example: age band in OULAD dataset
- Mutable
   Definition: A feature whose value can be changed or al-
   tered, either directly or through specific steps
   - Mutable Directly (M.D.)
     Definition: A feature whose value recipient can mod-
     ify directly by the recipient through their actions with
     certainty and without any constraints
     Example: loan amount in Loan Approval dataset
   - Mutable Indirectly (M.I.)
     Definition: A feature whose value changes as a conse-
     quence of one or more actions taken by the recipient
     but cannot be directly modified itself
     Example: Blood Pressure in Diabetes dataset
```


# Template-based Text Generation
 To ensure well-structured templates for counterfactual explanations, a user study was conducted to analyze the key ideas in generating natural language counterfactual explanations. Based on the findings of user study and feature actionability taxonomy we constructed our template-based NLG system. The creation of our templates involved three stages: sentence planning, surface realisation and discourse planning.  

An output example:

*In order to prevent you from heart problems you would need to change 5 attributes.  
You would not get heart problem if you,  
1), increase cp to 2.0.  
2), take steps to lower trestbps to 108.0 and,  
3), lower chol to 243.0.  
4), lower thalach to 152.0.  
5), decrease oldpeak to 0.0.  
Furthermore, Your age has a contribution to have a heart problem.  
Moreover, sex Male has a higher chance to  have a healthy heart compared to sex Female and, Take care!*  
  
We hope that this information will be helpful for users who wish to contribute datasets and work with our code.
