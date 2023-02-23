from dataset_utils import CF_Generator
from dataset_utils import create_tabular_CF
from dataset_utils import construct_generations
from dataset_utils import final_dataset
import pandas as pd

def create_dataset(
    dataset,
    target_name,
    undesired_class,
    desired_class,
    con_feats,
    cat_feats,
    feature_categories,
    undesired_statement,
    desired_statement,
    output_path,
    samples_limit,
    max_CF,
    current_class,
    numeric_only,
    categorical_sex,
    dataset_name,
    pre_starting,
    starting,
    ending,
):

  print("Start generating Counterfactuals...")
  exp_genetic = CF_Generator(dataset,
                              target_name,
                              categorical_features=cat_feats,
                              continuous_features=con_feats,
                              numeric_only=numeric_only)
  print("Counterfactual generation just finished...")

  print("Start generating tabular CF dataset...")
  dataset = create_tabular_CF(dataset,
                              exp_genetic,
                              samples_limit=samples_limit, # 1000
                              max_CF=max_CF,
                              outcome_name=target_name,
                              current_class=current_class,
                              output_path=output_path)
  print("Tabular CF dataset generation just finished...")
  print("Start generating textual explanations...")
  generations = construct_generations(dataset,
                                      pre_starting,
                                      starting,
                                      ending,
                                      feature_categories,
                                      undesired_class,
                                      desired_class,
                                      undesired_statement,
                                      desired_statement)
  print("textual explanations generation just finished...")

  generations = pd.DataFrame.from_dict(generations, orient="index")
  generations.rename(columns={0:"text"}, inplace=True)
  df = final_dataset(dataset, generations)
  df.to_csv(f"{dataset_name}.csv", index=False)
