input_file = "/content/heart.csv"
target_name = "target"
undesired_class = "have a heart problem."
desired_class = "healthy heart."
con_feats = ['age',
             'cp',
             'trestbps',
             'chol',
             'fbs',
             'restecg',
             'thalach',
             'exang',
             'oldpeak',
             'slope',
             'ca',
             'thal']

cat_feats = ['sex']
feature_categories = {'age':"restricted",
                      'sex':"regular",
                      'cp':"direct",
                      'trestbps':"indirect",
                      'chol':"direct",
                      'fbs':"direct",
                      'restecg':"direct",
                      'thalach':"direct",
                      'exang':"direct",
                      'oldpeak':"direct",
                      'slope':"direct",
                      'ca':"direct",
                      'thal':"direct"}

undesired_statement="have a heart problem"
desired_statement="have a healthy heart"
output_path="/data/counterfactuals.csv"
samples_limit=0
max_CF=4
current_class=1
numeric_only=True

dataset_name = "my_sample"

pre_starting = ["In order to prevent having a heart disease you need to change ",
                "In order to prevent you from heart problems you would need to change "]

starting = ["You would not have heart disease if you, ",
            "You would not get heart problem if you, ",
            "You won't have heart disease if you, "]

ending = ["Take care!", "stay healthy!",
          "I hope all is well.",
          "stay safe!",
          "Wishing you well."]
