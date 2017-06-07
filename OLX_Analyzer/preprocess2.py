import pandas as pd
import numpy as np
from  sklearn import cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

#reading from a file
flat_data = pd.read_csv(r"C:\Users\emirh\PycharmProjects\OLX_Scraper\podaci\stanovi_13032017.csv")
print("START: " + str(len(flat_data)))
#drop row if column 'Vrsta oglasa' is different than 'Prodaja'
flat_data = flat_data[flat_data['Vrsta oglasa'] == "Prodaja"]

flat_data = flat_data[['Kvadrata','Cijena','Broj soba']]

#drop row if column Kvadrata contains "-"
flat_data = flat_data[flat_data.Kvadrata.str.contains("-") == False]
#drop row if column Kvadrata contains "/"
flat_data = flat_data[flat_data.Kvadrata.str.contains("/") == False]
#drop row if column Kvadrata contains "od "
flat_data = flat_data[flat_data.Kvadrata.str.contains("od ") == False]

#replace certain strings, with some other
flat_data.Cijena = flat_data.Cijena.str.replace("KM", "").str.replace(",", "").str.replace(".","").str.replace("Po dogovoru", "NaN").str.strip()
flat_data['Broj soba'] = flat_data['Broj soba'].str.replace("(", "").str.replace(")", "").str[-3:].str.replace("n", "").str.replace("era","0").str.strip().str.replace("iše", "5.5")
#if there is non-digit value after digits, delete everything after digits (http://stackoverflow.com/a/42781927/3357517)
flat_data.Kvadrata = flat_data.Kvadrata.str.extract('(\d+)', expand=False)

print("Before short-long cleaning: " + str(len(flat_data)))
flat_data = flat_data[flat_data.Kvadrata.str.len() < 4]
flat_data = flat_data[flat_data.Cijena.str.len() < 7]

print("Before NaN cleaning: " + str(len(flat_data)))
#clearing rows with NaN in an old-fashioned way
flat_data = flat_data[flat_data.Kvadrata != "NaN"]
flat_data = flat_data[flat_data.Cijena != 'NaN']
flat_data = flat_data[flat_data['Broj soba'] != 'NaN']

print("Before blank cleaning: " + str(len(flat_data)))
#clearing rows with blanks in an old-fashioned way
flat_data = flat_data[flat_data.Kvadrata != ""]
flat_data = flat_data[flat_data.Cijena != ""]
flat_data = flat_data[flat_data['Broj soba'] != ""]
flat_data = flat_data[flat_data.Kvadrata != " "]
flat_data = flat_data[flat_data.Cijena != " "]
flat_data = flat_data[flat_data['Broj soba'] != " "]


print("END: " + str(len(flat_data)))

flat_data.to_csv('flat_data.csv',header=True)

X = np.array(flat_data['Kvadrata'])
y = np.array(flat_data['Cijena'])

X = np.array([X]).T
y = np.array([y]).T

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size=0.2)

clf = LinearRegression()
clf.fit(X_train,y_train.ravel())
accuracy = clf.score(X_test, y_test)
print("Linear regression: ", accuracy)

flat_data = flat_data.astype(np.float64)
flat_data = flat_data[np.isfinite(flat_data)]
flat_data = flat_data[~np.isnan(flat_data.Kvadrata)]

print("END END: " + str(len(flat_data)))
plt.scatter(flat_data.Cijena, flat_data.Kvadrata, s=1)
plt.xlabel("Price")
plt.ylabel("m2")
plt.show()