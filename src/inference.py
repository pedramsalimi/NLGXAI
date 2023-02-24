from dataset import create_dataset
import config

def inference(
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
    max_CF,
    current_class,
    numeric_only,
    dataset_name,
    pre_starting,
    starting,
    ending,
):
  exp_genetic = CF_Generator(dataset,
                              target_name,
                              categorical_features=cat_feats,
                              continuous_features=con_feats,
                              numeric_only=numeric_only)

  dataset = create_tabular_CF(dataset,
                              exp_genetic,
                              samples_limit=0, # 1000
                              max_CF=max_CF,
                              outcome_name=target_name,
                              current_class=current_class,
                              output_path=output_path)

  generations = construct_generations(dataset,
                                      pre_starting,
                                      starting,
                                      ending,
                                      feature_categories,
                                      undesired_class,
                                      desired_class,
                                      undesired_statement,
                                      desired_statement)


  generations = pd.DataFrame.from_dict(generations, orient="index")
  generations.rename(columns={0:"text"}, inplace=True)
  df = final_dataset(dataset, generations)
  df.to_csv(f"{dataset_name}.csv", index=False)
  data = pd.read_csv("/content/DiCE/my_sample.csv")
  print("\n",
        "*"*9,
        "COUNTERFACTUAL EXPLANATION",
        "*"*9,
        "\n")
  print(data.target_text.iloc[0])

if __name__ == "__main__":
  dataset_file_path = config.input_file
  dataset = pd.read_csv(dataset_file_path)
  dataset = dataset.dropna()
  categorical_sex = {1:"Male", 0:"Female"}
  dataset=dataset.replace({"sex": categorical_sex})
  sample = dataset.iloc[1020]

  target_name = "target"
  undesired_class = config.undesired_class
  desired_class = config.desired_class
  con_feats = config.con_feats
  cat_feats = config.cat_feats
  feature_categories = config.feature_categories
  undesired_statement = config.undesired_statement
  desired_statement = config.desired_statement
  output_path= config.output_path
  samples_limit= config.samples_limit
  max_CF= config.max_CF
  current_class=config.current_class
  numeric_only=config.numeric_only

  dataset_name = config.dataset_name
  pre_starting = config.pre_starting
  starting = config.starting
  ending = config.ending

  inference(
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
      max_CF,
      current_class,
      numeric_only,
      dataset_name,
      pre_starting,
      starting,
      ending,
  )
    
"""
Output Example:

100%|██████████| 1/1 [00:01<00:00,  1.09s/it]
 ********* COUNTERFACTUAL EXPLANATION ********* 

In order to prevent you from heart problems you would need to change 5 attributes.
You would not have heart disease if you, 
1), take steps to reduce trestbps to 94.0 and, 
2), increase chol from 248 to 471.0. 
3), raise thalach from 122 to 132.0. 
4), increase oldpeak from 1.0 to 2.0. 
5), raise ca from 0 to 1.0. 
Furthermore, Your age has a contribution to have a heart problem. 
Moreover, sex Male has a higher chance to  have a healthy heart compared to sex Female and, stay safe!
"""


