# SPUTA
Readme to be updated

## Important Notes
* Read Line 17 and Line 57 of views.py in companyDashboard
* Performance Graph and Next 30 Day Prediction Graph for each company have to be updated per month seperately and added to the their ticker folder in companyDashboard/static/companyDashboard/images/ with the naming convention TICKERNAME'no_space'2_digit_monthnumber.png<br>example: MSFT01.png

## Drawbacks
1. The UI / Web Design is not responsive 
2. The prediction is entirely based on past 100 days closing price, however it does not take into consideration sudden rises and falls in the company portfolio as stock market could be highly unpredictable sometimes.