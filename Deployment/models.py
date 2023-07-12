import pandas as pd
import pickle


def pred(df):
  
  cat_cols=['LanguageCode', 'Rating', 'Country']

  for col in cat_cols:
        df[col] = df[col].astype('object')
 
  df['Restructured'] = df['Restructured'].astype('bool')

  int_cols=['LoanDuration','MonthlyPaymentDay']

          
  for col in int_cols:
    df[col] = df[col].astype("int")


  float_cols=['InterestAndPenaltyPaymentsMade','PrincipalPaymentsMade','PrincipalBalance','Interest','MonthlyPayment','Amount','AppliedAmount',
              'LiabilitiesTotal','IncomeTotal','InterestAndPenaltyPaymentsMade']
          
  for col in float_cols:
    df[col] = df[col].astype("float")


  for colname in df.select_dtypes(["object"]):
      df[colname], _ = df[colname].factorize()


  Predictions = {} 

  # Classification Predictions
  clf = pickle.load(open('Models/pipeline_class.pkl', 'rb'))

  Predictions["Defaulted"] = clf.predict(df)
 
  # Regression Predictions
  reg = pickle.load(open('Models/pipeline_reg.pkl', 'rb'))

  predictions = reg.predict(df)

  Predictions['EMI'] = predictions[0][0]
  Predictions['ELA'] = predictions[0][1]
  Predictions['ROI'] = predictions[0][2]
  

  # Converting to DataFrame 
  Predictions = pd.DataFrame(Predictions)

  return pd.DataFrame(Predictions)