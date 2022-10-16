#explanatory stage
#importing the selected modules
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
#loading the load dataset as a pandas dataframe
loan_2=pd.read_csv(r"C:\Users\User\AppData\Roaming\JetBrains\PyCharmCE2021.3\scratches\loan_2.csv")
#1 home owner and income range
new_order=loan_2["IncomeRange"].value_counts().sort_values(ascending=False)
print(new_order)
sns.countplot(data=loan_2,y="IsBorrowerHomeowner", hue="IncomeRange", hue_order=new_order.index)
plt.title("A bar chart showing  income range and if \n a borrower is a home owner")
plt.xlabel("Count")
plt.ylabel("Home Owner")
plt.show()
#2 home owner and employment status
sns.countplot(data=loan_2,y="EmploymentStatus", hue="IsBorrowerHomeowner")
plt.title("A bar chart showing a borrowers employment status \n and home owner")
plt.xlabel("Count")
plt.ylabel("Employment Status")
plt.tight_layout()
plt.show()

#3 credit score and borrower's apr
plt.subplot(1,2,1)
sns.lineplot(data=loan_2, x="year", y="BorrowerRate")
plt.title("A line plot showing borrower's rate over time")
plt.ylabel("Borrower's Rate")
plt.xlabel("Year")
plt.subplot(1,2,2)
sns.lineplot(data=loan_2, x="year", y="BorrowerAPR")
plt.title("A line plot showing borrower's Annual percentage rate over time")
plt.ylabel("Borrower's Annual percentage rate (APR)")
plt.xlabel("Year")
plt.show()

#4 to get the average credit score
loan_2['average_credit_score'] = (loan_2['CreditScoreRangeLower'] + loan_2['CreditScoreRangeUpper'])/2
#taking a sample of the dataset
new_sample=loan_2.sample(100)
apr, rate, credit_score=new_sample["BorrowerAPR"],new_sample["BorrowerRate"], new_sample["average_credit_score"]
#crdit score and Apr
plt.subplot(1,2,1)
sns.regplot(data = loan_2, x = apr, y = credit_score, line_kws={'color':'blue'})
plt.title("A Scatter plot for showing \n Borrower's APR and average_credit_score")
plt.xlabel("Borrower's APR")
plt.ylabel("Average Credit Score")
#credit score and borrower's rate
plt.subplot(1, 2, 2)
sns.regplot(data = loan_2, x = rate, y = credit_score,  line_kws={'color':'blue'})
plt.title("A Scatter plot for showing \n Borrower's Rate and average_credit_score")
plt.xlabel("Borrower's Rate")
plt.ylabel("Average Credit Score")
#plt.show()