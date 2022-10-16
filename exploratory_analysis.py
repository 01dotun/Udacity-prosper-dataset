#importing the required libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
#loading the load dataset as a pandas dataframe
loan=pd.read_csv(r"C:\Users\User\AppData\Roaming\JetBrains\PyCharmCE2021.3\scratches\datasets\prosperLoanData.csv")
#cleaning the dataset
#this are the columns that would be required for the analysis
col=["ListingCreationDate", "Term", "LoanStatus", "BorrowerAPR","BorrowerRate", "ListingCategory (numeric)","Occupation", "EmploymentStatus", "IncomeRange",
         "StatedMonthlyIncome", "IsBorrowerHomeowner", "EmploymentStatusDuration", "ProsperScore", "LoanOriginalAmount","LoanOriginationDate",
          "BorrowerState", "Investors", "Recommendations", "LenderYield", "ProsperRating (Alpha)", "CreditScoreRangeLower", "CreditScoreRangeUpper"]
#this checks for columns in the new dataframe if they are in the original dataframe so as there should not be an error
for i in col:
    if i in loan.columns:
        print("i in column")
    else:
       print("i not in column")
#creating a new dataframe based on existing values
loan_2=loan[col].copy()
#functions used to avoid repetition
def missing_value(df, column, newvalue):
    """
    this function fills the missing values in a column with the value given to it
    """
    for i in column:
        df[column]=df[column].fillna(newvalue)
def data_type(df,columns,newtype):
    """
       this function converts a column to the appropriate data type
    """
    for column in columns:
        df[columns]=df[columns].astype(newtype)
def date_change(df,column):
    """
       this function converts a column to a datetime object
    """
    df[column]=pd.to_datetime(df[column])
def rename_variable(df, column_name, *variables, new_variable="new_variable"):
    """
    This function has 4 arguments
    df: dataframe
    column_name: column of interest
    *variables: variables in the column
    new_variable: the new variable given to it
    this functions checks the column of interest for the variables that want to be created
    """
    for i in column_name:
        df[column_name].replace(variables, new_variable, inplace=True)

#working with missing values
missing_value(loan_2, "Occupation", "Other")
missing_value(loan_2, "EmploymentStatus", "not_given")
missing_value(loan_2, "BorrowerState", "No_state")
missing_value(loan_2, "ProsperScore", 0)
missing_value(loan_2, "BorrowerAPR", 0)
missing_value(loan_2, "EmploymentStatusDuration", 0)
#checking for duplicates
loan_2.duplicated().sum()
#incorrect datatype
#datetime
date_change(loan_2, "LoanOriginationDate")
date_change(loan_2, "ListingCreationDate")
#int64
data_type(loan_2, "ProsperScore", int)
#print(loan_2.info())
#new column for year
year=loan_2["LoanOriginationDate"].dt.year
loan_2["year"]=year
#Exploratory data analysis
#employment
employment_status=loan_2["EmploymentStatus"].value_counts()
rename_variable(loan_2, "EmploymentStatus", "Not available", "not_given", new_variable="Not_given")
rename_variable(loan_2, "EmploymentStatus", "Employed", "Self-employed", "Part-time", "Full-time", new_variable="Employed")
rename_variable(loan_2, "EmploymentStatus", "Not employed", new_variable="Unemployed")
employment_status=loan_2["EmploymentStatus"].value_counts()
print(employment_status)
sns.countplot(data=loan_2, y="EmploymentStatus", color="blue", order=employment_status.index)
plt.xlabel("Count of loan requests")
plt.ylabel("Employment status recorded")
plt.title("Employment status of Loan requests")
plt.show()

#Occupation and loan
occupation_order=loan_2["Occupation"].value_counts()
sns.countplot(data=loan_2, x="Occupation", color="blue", order=occupation_order.index)
plt.title("Occupation with the most amount of loan requested")
plt.ylabel("count")
plt.xlabel("Occupation")
plt.xticks(rotation=90)
plt.show()

print(occupation_order)
print(loan_2["Occupation"].unique())
rename_variable(loan_2,"Occupation","Nurse (LPN)","Pharmacist","Medical Technician", "Doctor","Chemist","Dentist","Nurse (RN)","Nurse's Aide", new_variable="Professional")
rename_variable(loan_2,"Occupation","Construction","Engineer - Mechanical","Engineer - Electrical","Engineer - Chemical", new_variable="Professional")
rename_variable(loan_2,"Occupation","Student - College Graduate Student","Student - College Senior","Student - College Sophomore", "Student - College Freshman",
               "Student - Community College","Student - Technical School","Student - College Junior",new_variable="Students")
rename_variable(loan_2,"Occupation","Computer Programmer","Executive","Teacher", "Analyst","Accountant/CPA","Retail Management","Judge","Professor",
                "Pilot - Private/Commercial","Architect","Principal","Biologist","Sales - Retail","Sales - Commission","Flight Attendant","Scientist",
                "Scientist","Realtor","Attorney","Psychologist",new_variable="Professional")
rename_variable(loan_2,"Occupation","Skilled Labor","Truck Driver","Laborer", "Fireman","Tradesman - Mechanic","Bus Driver","Landscaping","Waiter/Waitress",
                "Tradesman - Plumber","Tradesman - Carpenter","Homemaker","Postal Service","Tradesman - Electrician","Clerical","Teacher's Aide"
                "Social Worker","Teacher's Aide","Administrative Assistant","Social Worker",new_variable="Semi-skilled")
rename_variable(loan_2, "Occupation", "Military Officer","Civil Service", "Police Officer/Correction Officer","Military Enlisted",new_variable="Government Officials")
rename_variable(loan_2, "Occupation","Car Dealer", "Food Service Management","Food Service","Investor","Clergy", "Religious","Other",new_variable="Others")
print(loan_2["Occupation"].unique())
print(loan_2["Occupation"].value_counts())
occupation_order=loan_2["Occupation"].value_counts()
sns.countplot(data=loan_2, y="Occupation", color="blue", order=occupation_order.index)
plt.title("Occupation with the most amount of loan requested")
plt.xlabel("count")
plt.xticks(rotation=90)
plt.show()
loan_2["Occupation"]=loan_2["Occupation"].replace({}, inplace=True)

#Homeowner and loan
print(loan_2.info())
home_owner=loan_2["IsBorrowerHomeowner"].value_counts()
home_owner_percentage=[((home_owner[0]/113937)*100),((home_owner[1]/113937)*100)]
legend=["False:Borrower is not a home owner", "True:Borrower is a homeowner"]
#print(home_owner)
plt.pie(home_owner_percentage, autopct="%.1f%%")
plt.legend(legend, loc="best")
plt.title("Loan requests and whether the customer is a homeowner or not")
plt.show()
print(loan_2["Term"].value_counts())
orders=loan_2.groupby("Term").size().sort_values().index
plt.figure(figsize=[24,10])
sns.countplot(data=loan_2, x="Term", color="blue")
plt.title("The frequency of Length of Loans in months")
plt.xlabel("Months")
plt.ylabel("Frequency")
plt.show()


print(loan_2["ListingCategory (numeric)"].value_counts())
#loanstatus
loan_status_order=loan_2["LoanStatus"].value_counts().index
sns.countplot(data=loan_2, y="LoanStatus", color="blue", order=loan_status_order)
plt.title("Status of Loan")
plt.xlabel("Status")
plt.ylabel("Count")
plt.show()
rename_variable(loan_2, "ListingCategory (numeric)", 0, new_variable="Not Available")
rename_variable(loan_2, "ListingCategory (numeric)", 1, new_variable="Debt Consolidation")
rename_variable(loan_2, "ListingCategory (numeric)", 2, new_variable="Home Improvement")
rename_variable(loan_2, "ListingCategory (numeric)", 3, new_variable="Business")
rename_variable(loan_2, "ListingCategory (numeric)", 4, new_variable="Personal Loan")
rename_variable(loan_2, "ListingCategory (numeric)", 5, new_variable="Student Use")
rename_variable(loan_2, "ListingCategory (numeric)", 6, new_variable="Auto")
rename_variable(loan_2, "ListingCategory (numeric)", 7, new_variable="Others")
rename_variable(loan_2, "ListingCategory (numeric)", 8, new_variable="Baby&Adoption")
rename_variable(loan_2, "ListingCategory (numeric)", 9, new_variable="Boat")
rename_variable(loan_2, "ListingCategory (numeric)", 10, new_variable="Cosmetic Procedure")
rename_variable(loan_2, "ListingCategory (numeric)", 11, new_variable="Engagement Ring")
rename_variable(loan_2, "ListingCategory (numeric)", 12, new_variable="Green Loans")
rename_variable(loan_2, "ListingCategory (numeric)", 13, new_variable="Household Expenses")
rename_variable(loan_2, "ListingCategory (numeric)", 14, new_variable="Large purchases")
rename_variable(loan_2, "ListingCategory (numeric)", 15, new_variable="Medical/Dental")
rename_variable(loan_2, "ListingCategory (numeric)", 16, new_variable="Motorcycle")
rename_variable(loan_2, "ListingCategory (numeric)", 17, new_variable="RV")
rename_variable(loan_2, "ListingCategory (numeric)", 18, new_variable="Taxes")
rename_variable(loan_2, "ListingCategory (numeric)", 19, new_variable="Vacation")
rename_variable(loan_2, "ListingCategory (numeric)", 20, new_variable="Wedding Loans")
percentage_of_listing_category=loan_2["ListingCategory (numeric)"].value_counts()
for i in range(percentage_of_listing_category.shape[0]):
    count=percentage_of_listing_category[i]
    percentage_string="{:0.1f}".format(100*count/(percentage_of_listing_category.sum()))
    plt.text(count+1,i, percentage_string +"%", va="center")
sns.countplot(data=loan_2, y="ListingCategory (numeric)", color="blue", order=percentage_of_listing_category.index)
plt.ylabel("Reason")
plt.title("Reasons for collecting loan")
plt.show()
sns.countplot(data=loan_2, x="ProsperScore", color="blue")
plt.title("Prosper score")
plt.show()

#Borrowers APR
#Distribution
#print(loan_2.info())
plt.subplot(1,2,1)
borrower_rate_bins=np.arange(loan_2["BorrowerRate"].min(), loan_2["BorrowerRate"].max()+0.01,0.01)
plt.hist(data=loan_2, x="BorrowerRate", color="blue", bins=borrower_rate_bins)
plt.title("A histogram showing distribution of Borrower's rate")
plt.xlabel("Borrower's Rate")
plt.ylabel("Frequency")
plt.subplot(1,2,2)
borrower_apr_bins=np.arange(loan_2["BorrowerAPR"].min(), loan_2["BorrowerAPR"].max()+0.01,0.01)
plt.hist(data=loan_2, x="BorrowerAPR", color="blue", bins=borrower_apr_bins)
plt.title("A histogram showing distribution of Borrower's Annual percentage rate (APR)")
plt.xlabel("Borrower's Annual percentage rate (APR)")
plt.ylabel("Frequency")
plt.show()
numerical_variables=loan_2.select_dtypes(include="number").columns
plt.figure(figsize=[10,6])
sns.heatmap(loan_2[numerical_variables].corr(), annot=True, fmt=".3f")
plt.title("A heatmap showing correlation between numerical variables.")
plt.xticks(rotation=9)
plt.show()
#scatterplot of loan amount and lenders yield
sns.regplot(data=loan_2, x="LoanOriginalAmount", y="LenderYield")
plt.show()
#creating a sample of the dataset to reduce overlapping
sample=loan_2.sample(1000)
xdatasample, ydatasample=sample["LoanOriginalAmount"], sample["LenderYield"]
sns.regplot(data=loan_2, x=xdatasample, y=ydatasample)
plt.title("A scatterplot showing lenders yield and original loan amount")
plt.show()
#box plot of loan status and loan original amount
plt.figure(figsize=[24,10])
orders=loan_2.groupby("LoanStatus")["LoanOriginalAmount"].sum().sort_values(ascending=True)
print(orders)
sns.boxplot(data=loan_2, x="LoanStatus", y="LoanOriginalAmount", order=orders.index, color="blue")
plt.title("A boxplot showing the relationship between loan status and loan original amount")
plt.xlabel("Loan Status")
plt.ylabel("Loan Original Amount")
plt.xticks(rotation=12)
plt.show()
#violin plot for term in relation to APR, BorrowerRate
plt.subplot(1,2,1)
sns.violinplot(data = loan_2, x = 'Term', y = 'BorrowerAPR', color = "blue")
plt.title("A violin plot showing term and APR")
plt.subplot(1,2,2)
sns.violinplot(data = loan_2, x = 'Term', y = 'BorrowerRate',color = "blue")
plt.title("A violin plot showing term and Borrower Rate")
plt.show()
sns.lineplot(data=loan_2, x="year", y="BorrowerRate", hue="EmploymentStatus")
plt.title("Yearly Borrower's rate by employment status")
plt.show()
sns.barplot(data=loan_2, x="year", y="BorrowerRate", hue="IsBorrowerHomeowner")
plt.title("A plot showing the borrower's rate by homeowner")
plt.show()

plt.subplot(1,2,1)
prosper_orders=loan_2.groupby("ProsperRating (Alpha)").size().sort_values(ascending=True)

sns.pointplot(data = loan_2, x = 'ProsperRating (Alpha)', y = 'StatedMonthlyIncome',order=prosper_orders.index, hue = 'Term', linestyles="")
plt.title("A point plot showing term in relation to \n prosper rating and loan original amount")
plt.xlabel("Prosper Rating (Alpha)")
plt.ylabel("Stated Monthly Income")
plt.subplot(1,2,2)
sns.pointplot(data = loan_2, x = 'ProsperRating (Alpha)', y = 'LoanOriginalAmount',order=prosper_orders.index, hue = 'Term',linestyles="")
plt.title("A point plot showing term in relation to \n prosper rating and loan original amount")
plt.xlabel("ProsperRating (Alpha)")
plt.ylabel("Loan Original Amount")
plt.show()
#saving for file for explanatory analysis
#loan_2.to_csv('loan_2.csv', index = False)

