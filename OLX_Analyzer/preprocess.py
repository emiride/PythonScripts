import pandas as pd
import numpy as np
from  sklearn import cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

#reading from a file
flat_data = pd.read_csv(r"C:\Users\emirh\PycharmProjects\OLX_Scraper\podaci\stanovi_13032017.csv")
#drop row if column Kvadrata contains "-"
flat_data = flat_data[flat_data.Kvadrata.str.contains("-") == False]
print(len(flat_data))
flat_data = flat_data[flat_data['Vrsta oglasa'] != "Potražnja"]
flat_data = flat_data[flat_data['Vrsta oglasa'] != "Izdavanje"]
flat_data = flat_data[flat_data.Kvadrata.str.len() < 4]
flat_data = flat_data[flat_data.Cijena.str.len() > 6]


print(len(flat_data))
flat_data.Cijena = flat_data.Cijena.str.replace("KM", "").str.replace(",", "").str.replace(".","").str.replace("Po dogovoru", "NaN").str.strip()
flat_data['Broj soba'] = flat_data['Broj soba'].str.replace("(", "").str.replace(")", "").str[-3:].str.replace("n", "").str.replace("era","0").str.strip().str.replace("iše", "5.5")
flat_data.Kvadrata = flat_data.Kvadrata.str.extract('(\d+)', expand=False)

flat_data = flat_data[['Kvadrata','Cijena']]
flat_data = flat_data.replace([np.inf, -np.inf], np.nan).dropna(how="all")
flat_data = flat_data.astype(np.float64)
flat_data = flat_data[np.isfinite(flat_data)]
print(len(flat_data))
flat_data.to_csv('flat_data.csv',header=True)

X = np.array(flat_data['Kvadrata'])
y = np.array(flat_data['Cijena'])

X = np.array([X]).T
y = np.array([y]).T

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size=0.2)

X_train[np.isnan(X_train)] = np.median(X_train[~np.isnan(X_train)])
y_train[np.isnan(y_train)] = np.median(y_train[~np.isnan(y_train)])
X_test[np.isnan(X_test)] = np.median(X_test[~np.isnan(X_test)])
y_test[np.isnan(y_test)] = np.median(y_test[~np.isnan(y_test)])

clf = svm.LinearSVR()
clf.fit(X_train,y_train)
accuracy = clf.score(X_test, y_test)
print("Linear regression: ", accuracy)

plt.scatter(flat_data.Cijena, flat_data.Kvadrata, s=1)
#flat_data.Cijena.plot()
#flat_data.Kvadrata.plot()

plt.xlabel("Price")
plt.ylabel("m2")
plt.show()