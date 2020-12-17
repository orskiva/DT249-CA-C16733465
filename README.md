# Income predictor - Iva Oreskovic

Using a dataset ( the "Adult Data Set") from the UCI Machine-Learning Repository we can predict based on a number of factors whether or not someone's income will be greater than $50,000.

## Building the classifier
Data is imported directly from the web as a CSV. Having selected for the apppropriate, ''clean'' dataset (not utilising any lines with missing info/categories), the data is split into greater than (g) and less than/equal (l) 50k income. Dataset is then split into 75/25, to be used as training and test data. The average values of l and g for the test data are calculated. These two results ar ethen averaged for each attribute to compute a midpoint or 'class separation value'.
For each record, each attribute is tested against the midpoint values of l/g datasets. The overall result is the greater count of the individual results (<=50K, >50K).




## The data

The data is presented in the form of a comma-delimited text file (CSV) which has the following structure:

Listing of attributes:

1. Age: Number.
2. Workclass: Can be one of -- Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked.
3. fnlwgt: number. This is NOT NEEDED for our study.
4. Education: Can be one of -- Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool. This is NOT NEEDED for our study.
5. Education-number: Number -- indicates level of education.
6. Marital-status: Can be one of -- Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse.
7. Occupation: Can be one of -- Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces.
8. Relationship: Can be one of -- Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried.
9. Race: Can be one of -- White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black.
10. Sex: Either Female or Male.
11. Capital-gain: Number.
12. Capital-loss: Number.
13. Hours-per-week: Number.
14. Native-country: United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands. This is NOT NEEDED for our study.
15. Outcome for this record: Can be >50K or <=50K.

Data is available from http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data. This application downloads and reads this CSV directly from the web. 

Fields that have 'discrete' attributes such as 'Relationship' are given a numeric weight by counting the number of occurrences as a fraction of the total number of positive records (outcome > 50K) and negative records (outcome <= 50K).
'''

## Running the project
Project was developed in a python3 environment
1. Install request module: `pip3 install requests`
2. Run classifier.py through IDE or command line: `python classifier.py`
