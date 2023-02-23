import random
import torch
import dice_ml
from dice_ml import Dice
from sklearn.datasets import load_iris, fetch_california_housing
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import pandas as pd
import numpy as np
from dice_ml.utils import helpers 
from sklearn.model_selection import train_test_split


def CF_Generator(dataset,
                 target_name,
                 categorical_features=None,
                 continuous_features=None,
                 numeric_only=True):
  
  target = dataset[target_name] 
  outcome_name = target_name
  len_new_data=len(dataset[dataset[outcome_name]==0])
  target = dataset[outcome_name]



  numeric_transformer = Pipeline(steps=[
      ('scaler', StandardScaler())])

  categorical_transformer = Pipeline(steps=[
      ('onehot', OneHotEncoder(handle_unknown='ignore'))])



  if numeric_only:
    transformations = ColumnTransformer(
      transformers=[('num', numeric_transformer, continuous_features)])
  else:
    transformations = ColumnTransformer(
      transformers=[
          ('num', numeric_transformer, continuous_features),
          ('cat', categorical_transformer, categorical_features)])
  
  datasetX = dataset.drop(outcome_name, axis=1)

  x_train, x_test, y_train, y_test = train_test_split(datasetX,
                                                      target,
                                                      test_size=0.2,
                                                      random_state=0,
                                                      stratify=target)

  clf = Pipeline(steps=[('preprocessor', transformations),('classifier', RandomForestClassifier())])
  model = clf.fit(x_train, y_train)

  if numeric_only:

    d = dice_ml.Data(dataframe=dataset,
                        continuous_features=continuous_features, 
                          outcome_name=outcome_name)
  else:
    d = dice_ml.Data(dataframe=dataset,
                        continuous_features=continuous_features,
                        categorical_features=categorical_features,
                          outcome_name=outcome_name)
    
  m = dice_ml.Model(model=model, backend="sklearn", model_type='classifier')

  exp_genetic = Dice(d,m, method="genetic")
  return exp_genetic

def create_tabular_CF(dataset,
                      exp_genetic,
                      samples_limit,
                      max_CF,
                      outcome_name,
                      current_class,
                      output_path):
  
  queries = dataset[dataset[outcome_name]==current_class]
  queries.reset_index(inplace=True)
  queries = queries.drop([outcome_name, "index"], axis=1)
  len_new_data = len(dataset[dataset[outcome_name]==1])
  total = []
  for x in queries.T:
    query_instance = pd.DataFrame(queries.iloc[x]).T
    dice_exp = exp_genetic.generate_counterfactuals(query_instance, total_CFs=max_CF, desired_class="opposite")
    dice_exp.cf_examples_list[0].final_cfs_df.to_csv(path_or_buf='counterfactuals.csv', index=False)
    cfs = pd.read_csv(output_path)

    sample_dic = {}
    dic = {}
    for j in cfs.T:
      max = 0
      for i in query_instance.columns:
        if query_instance[i].item() != cfs.iloc[j][i]:
          max += 1
      dic[j] = max

    cf = cfs.iloc[np.argmin(dic)]
    feats = []
    for i in query_instance.columns:
      if query_instance[i].item() != cf[i]:
        feats.append(i)
    
    cf = pd.DataFrame(cf).T
    sample_dic["query"] = query_instance
    sample_dic["counter"] = cf
    sample_dic["diff"] = feats

    total.append(sample_dic)
    if x == samples_limit:
      break

  q=total[0]['query'].copy()
  q["qc"] = "q"
  q["index"] = 0

  c=total[0]['counter'].copy()
  c["qc"] = "c"
  c["index"] = 0

  frames = [q,c]
  dataset = pd.concat(frames)

  for i in range(1, len(total)):
    q=total[i]['query'].copy()
    q["qc"] = "q"
    q["index"] = i

    c=total[i]['counter'].copy()
    c["qc"] = "c"
    c["index"] = i

    frames.append(q)
    frames.append(c)

  dataset = pd.concat(frames)
  dataset.drop(outcome_name, inplace=True, axis=1)
  return dataset

def diff(valQ, valC):
    if type(valQ) != str:
        if int(valQ) > int(valC):
            return random.choice(["decrease", "lower", "reduce"])
        elif int(valQ) < int(valC):
            return random.choice(["increase", "raise"])
        else:
            return None
    else:
        if valQ != valC:
            return random.choice(["change", "exchange", "modify"])

def set_seed(seed):
  torch.manual_seed(seed)
  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

def tpl_Q_C(pre_starting,
            starting,
            feat_changes,
            feature_categories,
            undesired_class,
            desired_class,
            undesired_statement,
            desired_statement):
  
  im_restricted = []
  im_regular = []
  m_direct = []
  m_indirect = [] 
  restricted = []
  regular = []

  for i in feature_categories.keys(): 
    if feature_categories[i] == "restricted":
      im_restricted.append(i)
    elif feature_categories[i] == "regular":
      im_regular.append(i)
    elif feature_categories[i] == "direct":
      m_direct.append(i)
    elif feature_categories[i] == "indirect":
      m_indirect.append(i)

  seed = random.randint(0, 50)
  set_seed(seed)

  start = random.choice(starting)
  feat_changes = feat_changes
  c = 0
  for feat in feat_changes.keys():

   #Directly Mutable Features 
   if feat in m_direct:
    if c+1 == len(feat_changes):
      properties = feat_changes[feat]
      temp = f"{properties[0]} {feat} from {properties[1]} to {properties[2]} "
      start += temp
      c += 1
    else:
      properties = feat_changes[feat]
      temp = f"{properties[0]} {feat} from {properties[1]} to {properties[2]} and, "
      start += temp
      c += 1

   #Indirectly Mutable Features
   elif feat in m_indirect:
    if c+1 == len(feat_changes):
      properties = feat_changes[feat]
      temp = f"take steps to {properties[0]} {feat} from {properties[1]} to {properties[2]} "
      start += temp
      c += 1
    else:
      properties = feat_changes[feat]
      temp = f"take steps to {properties[0]} {feat} from {properties[1]} to {properties[2]} and, "
      start += temp
      c += 1

   # Restricted Immutable features
   elif feat in im_regular:
     regular.append(feat)

   elif feat in im_restricted:
     restricted.append(feat)

  immutable_reg = ""
  x = 0
  for f in regular:
    properties = feat_changes[f]
    if x == 0:
      temp = f"Moreover, {f} {properties[2]} has a higher chance to  {desired_statement} compared to {f} {properties[1]} and, "
      immutable_reg += temp
      x += 1
    else:
      temp = f", {f} {properties[2]} has a higher chance to  {desired_statement} compared to {f} {properties[1]}. "
      immutable_reg += temp
      x += 1

  immutable_res = ""
  x = 0
  for f in restricted:
    if x == 0:
      temp = f"Furthermore, Your {f} has a contribution to {undesired_class} "
      immutable_res += temp
      x += 1
    else:
      temp = f", Your {f} has a contribution to {undesired_class}. "
      immutable_res += temp
      x += 1
  # number of actionable features:
  total_immutable_features = len(regular) + len(restricted)
  total_actionable = len(feat_changes) - total_immutable_features

  pre_start = random.choice(pre_starting)
  pre_start = pre_start + str(total_actionable) + " attributes.\n"

  return pre_start+start+immutable_res+immutable_reg

def tpl_C(pre_starting,
          starting,
          feat_changes,
          feature_categories,
          undesired_class,
          desired_class,
          undesired_statement,
          desired_statement):

  im_restricted = []
  im_regular = []
  m_direct = []
  m_indirect = [] 
  restricted = []
  regular = []

  for i in feature_categories.keys(): 
    if feature_categories[i] == "restricted":
      im_restricted.append(i)
    elif feature_categories[i] == "regular":
      im_regular.append(i)
    elif feature_categories[i] == "direct":
      m_direct.append(i)
    elif feature_categories[i] == "indirect":
      m_indirect.append(i)

  seed = random.randint(0, 50)
  set_seed(seed)

  start = random.choice(starting)
  feat_changes = feat_changes
  c = 0
  for feat in feat_changes.keys():

   #Directly Mutable Features 
   if feat in m_direct:
    if c+1 == len(feat_changes):
      properties = feat_changes[feat]
      temp = f"{properties[0]} {feat} to {properties[2]} "
      start += temp
      c += 1
    else:
      properties = feat_changes[feat]
      temp = f"{properties[0]} {feat} to {properties[2]} and, "
      start += temp
      c += 1

   #Indirectly Mutable Features
   elif feat in m_indirect:
    if c+1 == len(feat_changes):
      properties = feat_changes[feat]
      temp = f"take steps to {properties[0]} {feat} to {properties[2]} "
      start += temp
      c += 1
    else:
      properties = feat_changes[feat]
      temp = f"take steps to {properties[0]} {feat} to {properties[2]} and, "
      start += temp
      c += 1

   # Restricted Immutable features
   elif feat in im_regular:
     regular.append(feat)

   elif feat in im_restricted:
     restricted.append(feat)


  immutable_reg = ""
  x = 0
  for f in regular:
    properties = feat_changes[f]
    if x == 0:
      temp = f"Moreover, {f} {properties[2]} has a higher chance to  {desired_statement} compared to {f} {properties[1]} and, "
      immutable_reg += temp
      x += 1
    else:
      temp = f", {f} {properties[2]} has a higher chance to  {desired_statement} compared to {f} {properties[1]}. "
      immutable_reg += temp
      x += 1

  immutable_res = ""
  x = 0
  for f in restricted:
    if x == 0:
      temp = f"Furthermore, Your {f} has a contribution to {undesired_class} "
      immutable_res += temp
      x += 1
    else:
      temp = f", Your {f} has a contribution to {undesired_class}. "
      immutable_res += temp
      x += 1

  # number of actionable features:
  total_immutable_features = len(regular) + len(restricted)
  total_actionable = len(feat_changes) - total_immutable_features

  pre_start = random.choice(pre_starting)
  pre_start = pre_start + str(total_actionable) + " attributes.\n"

  return pre_start+start+immutable_res+immutable_reg


def tpl_bullet_Q_C(pre_starting,
                   starting,
                   feat_changes,
                   feature_categories,
                   undesired_class,
                   desired_class,
                   undesired_statement,
                   desired_statement):

  im_restricted = []
  im_regular = []
  m_direct = []
  m_indirect = [] 
  restricted = []
  regular = []

  for i in feature_categories.keys(): 
    if feature_categories[i] == "restricted":
      im_restricted.append(i)
    elif feature_categories[i] == "regular":
      im_regular.append(i)
    elif feature_categories[i] == "direct":
      m_direct.append(i)
    elif feature_categories[i] == "indirect":
      m_indirect.append(i)

  seed = random.randint(0, 50)
  set_seed(seed)

  start = random.choice(starting)
  feat_changes = feat_changes
  c = 0
  for feat in feat_changes.keys():

   #Directly Mutable Features 
   if feat in m_direct:
    if c+1 == len(feat_changes):
      properties = feat_changes[feat]
      temp = f"\n{c+1}), and, {properties[0]} {feat} from {properties[1]} to {properties[2]}. "
      start += temp
      c += 1
    else:
      properties = feat_changes[feat]
      temp = f"\n{c+1}), {properties[0]} {feat} from {properties[1]} to {properties[2]}. "
      start += temp
      c += 1

   #Indirectly Mutable Features
   elif feat in m_indirect:
    if c+1 == len(feat_changes):
      properties = feat_changes[feat]
      temp = f"\n{c+1}), take steps to {properties[0]} {feat} to {properties[2]} "
      start += temp
      c += 1
    else:
      properties = feat_changes[feat]
      temp = f"\n{c+1}), take steps to {properties[0]} {feat} to {properties[2]} and, "
      start += temp
      c += 1

   # Restricted Immutable features
   elif feat in im_regular:
     regular.append(feat)

   elif feat in im_restricted:
     restricted.append(feat)


  immutable_reg = ""
  x = 0
  for f in regular:
    properties = feat_changes[f]
    if x == 0:
      temp = f"\nMoreover, {f} {properties[2]} has a higher chance to  {desired_statement} compared to {f} {properties[1]} and, "
      immutable_reg += temp
      x += 1
    else:
      temp = f", {f} {properties[2]} has a higher chance to  {desired_statement} compared to {f} {properties[1]}. "
      immutable_reg += temp
      x += 1

  immutable_res = ""
  x = 0
  for f in restricted:
    if x == 0:
      temp = f"\nFurthermore, Your {f} has a contribution to {undesired_class} "
      immutable_res += temp
      x += 1
    else:
      temp = f", Your {f} has a contribution to {undesired_class}. "
      immutable_res += temp
      x += 1

  # number of actionable features:
  total_immutable_features = len(regular) + len(restricted)
  total_actionable = len(feat_changes) - total_immutable_features

  pre_start = random.choice(pre_starting)
  pre_start = pre_start + str(total_actionable) + " attributes.\n"

  return pre_start+start+immutable_res+immutable_reg


def tpl_bullet_C(pre_starting,
                 starting,
                 feat_changes,
                 feature_categories,
                 undesired_class,
                 desired_class,
                 undesired_statement,
                 desired_statement):
  
  im_restricted = []
  im_regular = []
  m_direct = []
  m_indirect = [] 
  restricted = []
  regular = []

  for i in feature_categories.keys(): 
    if feature_categories[i] == "restricted":
      im_restricted.append(i)
    elif feature_categories[i] == "regular":
      im_regular.append(i)
    elif feature_categories[i] == "direct":
      m_direct.append(i)
    elif feature_categories[i] == "indirect":
      m_indirect.append(i)

  seed = random.randint(0, 50)
  set_seed(seed)

  start = random.choice(starting)
  feat_changes = feat_changes
  c = 0
  for feat in feat_changes.keys():

   #Directly Mutable Features 
   if feat in m_direct:
    if c+1 == len(feat_changes):
      properties = feat_changes[feat]
      temp = f"\n{c+1}), and, {properties[0]} {feat} to {properties[2]}. "
      start += temp
      c += 1
    else:
      properties = feat_changes[feat]
      temp = f"\n{c+1}), {properties[0]} {feat} to {properties[2]}. "
      start += temp
      c += 1

   #Indirectly Mutable Features
   elif feat in m_indirect:
    if c+1 == len(feat_changes):
      properties = feat_changes[feat]
      temp = f"\n{c+1}), take steps to {properties[0]} {feat} to {properties[2]} "
      start += temp
      c += 1
    else:
      properties = feat_changes[feat]
      temp = f"\n{c+1}), take steps to {properties[0]} {feat} to {properties[2]} and, "
      start += temp
      c += 1

   # Restricted Immutable features
   elif feat in im_regular:
     regular.append(feat)

   elif feat in im_restricted:
     restricted.append(feat)


  immutable_reg = ""
  x = 0
  for f in regular:
    properties = feat_changes[f]
    if x == 0:
      temp = f"\nMoreover, {f} {properties[2]} has a higher chance to  {desired_statement} compared to {f} {properties[1]} and, "
      immutable_reg += temp
      x += 1
    else:
      temp = f", {f} {properties[2]} has a higher chance to  {desired_statement} compared to {f} {properties[1]}. "
      immutable_reg += temp
      x += 1

  immutable_res = ""
  x = 0
  for f in restricted:
    if x == 0:
      temp = f"\nFurthermore, Your {f} has a contribution to {undesired_class} "
      immutable_res += temp
      x += 1
    else:
      temp = f", Your {f} has a contribution to {undesired_class}. "
      immutable_res += temp
      x += 1

  # number of actionable features:
  total_immutable_features = len(regular) + len(restricted)
  total_actionable = len(feat_changes) - total_immutable_features

  pre_start = random.choice(pre_starting)
  pre_start = pre_start + str(total_actionable) + " attributes.\n"

  return pre_start+start+immutable_res+immutable_reg

def construct_generations(dataset,
                          pre_starting,
                          starting,
                          ending,
                          feature_categories,
                          undesired_class,
                          desired_class,
                          undesired_statement,
                          desired_statement):

  t = dataset.copy()
  t.reset_index(inplace=True)
  t.drop("level_0", inplace=True, axis=1)

  generations = {}

  for i in range(len(t)):
    seed = random.randint(0, 50)
    set_seed(seed)
    if i%2==0:
      feat_changes = {}
      for j in t:
        l = []
        if j != "qc" and j != "index":
          dif= diff(valQ=t[t['qc']=="q"][j][i], # i
                    valC=t[t['qc']=="c"][j][i+1]) # i+1
        else:
          continue
        if dif != None:
          l.append(dif)  
          l.append(t[t['qc']=="q"][j][i])
          l.append(t[t['qc']=="c"][j][i+1])
        else:
          continue
        
        feat_changes[j] = l
        """
        feat_changes example: {'age': ['lower', 58.0, 29.0]}
        """

      start = random.choice([tpl_Q_C,tpl_C,tpl_bullet_Q_C,tpl_bullet_C])(pre_starting,
                                                                         starting,
                                                                         feat_changes,
                                                                         feature_categories,
                                                                         undesired_class,
                                                                         desired_class,
                                                                         undesired_statement,
                                                                         desired_statement) 

      end = random.choice(ending)
      generations[t['index'][i]] = start + end
  return generations


# generations = generations.to_dict()
def final_dataset(dataset, generations):
  generations = generations
  t = dataset.copy()
  t.reset_index(inplace=True)
  t.drop("level_0", inplace=True, axis=1)
  input_list = {}
  for x in range(len(t)):
    if x%2==0:
      q = pd.DataFrame(t.iloc[x]).T
      c = pd.DataFrame(t.iloc[x+1]).T

      query = ""
      for i in q.columns:
        if i != "index" and i != "qc":
          col = i + " && Query | " + str(q[i].item())
          query += col
          query += " "

      counter = ""
      for i in c.columns:
        if i != "index" and i != "qc":
          col = i + " && Counter | " + str(c[i].item())
          counter += col
          counter += " "
      total = query + " " + counter
      input_list[q["index"].item()] = total
  data = {}
  prefix = []
  for i in input_list.keys():
    prefix.append("ConterfactualExplanation")
    input = input_list[i]
    target = generations.text[i]
    data[i] = [input,target]
  df = pd.DataFrame.from_dict(data).T.rename(columns = {0:'input_text', 1:'target_text'})
  df["prefix"] = prefix
  return df
