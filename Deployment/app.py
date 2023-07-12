import pandas as pd
from flask import Flask, render_template, request,Markup

from models import pred

app = Flask(__name__,template_folder='templates')


@app.route('/')
def home():
	return render_template('home.html')


@app.route('/predict', methods=['GET','POST'])
def predict():

    Inputs = {}

    Inputs['InterestAndPenaltyBalance'] = request.form.get('InterestAndPenaltyBalance')
    Inputs['PrincipalPaymentsMade'] = request.form.get('PrincipalPaymentsMade')
    Inputs['PrincipalBalance'] = request.form.get('PrincipalBalance')
    Inputs['Interest'] = float(request.form.get('Interest')) / 100
    Inputs['MonthlyPayment'] = request.form.get('MonthlyPayment')
    Inputs['Amount'] = request.form.get('Amount')
    Inputs['AppliedAmount'] = request.form.get('AppliedAmount')
    Inputs['LanguageCode'] = request.form.get('LanguageCode')
    Inputs['Rating'] = request.form.get('Rating')
    Inputs['Country'] = request.form.get('Country')
    Inputs['Restructured'] = request.form.get('Restructured')
    Inputs['LoanDuration'] = request.form.get('LoanDuration')
    Inputs['MonthlyPaymentDay'] = request.form.get('MonthlyPaymentDay')
    Inputs['LiabilitiesTotal'] = request.form.get('LiabilitiesTotal')
    Inputs['IncomeTotal'] = request.form.get('IncomeTotal')
    Inputs['InterestAndPenaltyPaymentsMade'] = request.form.get('InterestAndPenaltyPaymentsMade')

    Inputs = pd.DataFrame.from_dict(Inputs, orient='index').T

    Outputs = pred(Inputs)

    Defaulted = Outputs['Defaulted'].values[0]
    EMI = Outputs['EMI'].values[0]
    ELA = Outputs['ELA'].values[0]
    ROI = Outputs['ROI'].values[0]


    Report = pd.concat([Inputs, Outputs], axis=1)

    Report.to_csv("Report.csv", index=False)

    

    if Defaulted == 1:
        return render_template('home.html', prediction_text=Markup(
            f"<br/>Defaulted:Yes<br/><br/> \
             EMI: {EMI:.2f} $ <br/><br/> \
             ROI: {ROI:.2f} % <br/><br/> \
             Eligible Loan Amount: {ELA:.2f} $")) 
    else:
        return render_template('home.html', prediction_text=Markup( 
            f"<br/>Defaulted: No <br/><br/>\
             EMI: {EMI:.2f} $ <br/><br/> \
             ROI: {ROI:.2f} % <br/><br/> \
             Eligible Loan Amount: {ELA:.2f} $")) 


if __name__=="__main__":
	app.run(debug=True)