import pandas as pd                 # pandas is a dataframe library
import matplotlib.pyplot as plt     # matplotlib.pyplot plots data
import numpy as np
from sklearn import cross_validation
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
from sklearn import tree
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
def preprocessing1():
	data = pd.read_csv(r"C:\TaskScheduler\stanovi_29032017.csv")

	print("\n")
	print("Task 1) Dropping all unnecessary columns\n")
	data = data.drop(['Alarm', 'Blindirana vrata', 'Cijena - Hitna prodaja [?]',
						'Datum objave', 'Dostava', 'Dostupnost', 'Garaža', 'Godina izgradnje', 
						'Hitno', 'Internet', 'Iznajmljeno', 'Kablovska TV', 'Kanalizacija', 'Klima', 'Kvadratura balkona',
						'Namješten', 'Način plaćanja','Nedavno adaptiran', 'Obnovljen', 'Ostava/špajz', 'Parking',
						'Plaćam do', 'Povrat novca', 'Primarna orjentacija', 'Stanje', 'Struja', 'Telefonski priključak', 
						'Uključen trošak režija', 'Uknjiženo / ZK', 'Video nadzor','Voda',
						 'Vrsta poda', 'Za studente'], axis=1)

	print("Task 2) Firstly dropping renting rows and then dropping 'Vrste oglasa '\n")
	data = data[data['Vrsta oglasa'] == "Prodaja"]
	data = data.drop('Vrsta oglasa', axis=1)

	print("Task 3) Dropping NaN values from 'Cijena' and 'Kvadrata'\n")
	data = data.dropna(subset=['Cijena'])
	data = data.dropna(subset=['Kvadrata'])
	
	print("Task 4) Dropping 'Po dogovoru' prices and making 'Cijena' usable\n")
	data = data[data.Cijena != 'Po dogovoru']
	data.Cijena = data.Cijena.str.replace("KM", "").str.replace(",", "").str.replace(".","").astype(float)

	print("Task 5) Cleaning 'Kvadrata'\n")
	data = data[data.Kvadrata.str.contains("-") == False]
	data = data[data.Kvadrata.str.contains("/") == False]
	data = data[data.Kvadrata.str.contains("od ") == False]
	data.Kvadrata = data.Kvadrata.str.extract('(\d+)', expand=False)
		
	print("Task 6) Enumerating 'Broj soba'\n")
	broj_soba_map = {'Garsonjera': 0.5, 'Jednosoban (1)': 1, 'Jednoiposoban (1.5)': 1.5,'Dvosoban (2)': 2,
					 'Trosoban (3)': 3, 'Četverosoban (4)': 4, 'Petosoban i više': 5}
	data['Broj soba'] = data['Broj soba'].map(broj_soba_map)

	print("Task 7) Enumerating 'Lokacija'\n")
	location_map = {'Sarajevo - Centar': 1, 'Novo Sarajevo': 2, 'Ilidža': 3, 'Stari Grad': 4, 
					'Sarajevo, Novi Grad': 5, 'Hadžići': 6, 'Vogošća': 7, 'Ilijaš': 8}
	data ['Lokacija'] = data['Lokacija'].map(location_map)

	print("Task 8) Enumerating 'Grijanje'\n")
	grijanje_map = {'Centralno (Plin)': 1, 'Centralno (Kotlovnica)': 2, 'Plin': 3, 'Centralno (gradsko)': 4,
					 'Struja': 5, 'Ostalo': 6}
	data ['Vrsta grijanja'] = data['Vrsta grijanja'].map(grijanje_map)
	grijanje = data['Vrsta grijanja']

	print("Task 9) Cleaning 'Sprat'\n")
	data['Sprat']= data['Sprat'].replace(['Visoko prizemlje', 'Prizemlje', 'Suteren'], [0.9, 0.5, 0])
	data['Sprat'] = data['Sprat'].str.extract('(\d+)', expand=False)

	print("Task 10) Assuming that user did not fill in some value if it is 'NaN', than \
		i will just replace it with zeros (If there is that value it is 1)\n")
	data = data.fillna(value=0)

	print("Task 11) Arranging columns as i want\n")
	cols = data.columns.tolist()
	data = data[['OLX ID','Adresa','Broj pregleda','Kvadrata','Broj soba','Lokacija', 'Sprat','Balkon',
					 'Lift', 'Novogradnja', 'Plin', 'Podrum/Tavan', 'Vrsta grijanja', 'Latitude', 'Longitude', 'Cijena']]

	print("Task 12) Converting 'Da', 'Ne' and 'marked' into numbers from 'Balkon', 'Lift', 'Novogradnja', 'Plin' and 'Podrum/Tavan'\n")
	data['Balkon']= data['Balkon'].replace(['Da', 'Ne', 'marked'], [1, 0, 1])
	data['Lift']= data['Lift'].replace(['Da', 'Ne', 'marked'], [1, 0, 1])
	data['Novogradnja']= data['Novogradnja'].replace(['Da', 'Ne', 'marked'], [1, 0, 1])
	data['Plin']= data['Plin'].replace(['Da', 'Ne', 'marked'], [1, 0, 1])
	data['Podrum/Tavan']= data['Podrum/Tavan'].replace(['Da', 'Ne', 'marked'], [1, 0, 1])

	print("Task 13) Dropping all 'Cijena' where price < 10000\n")
	data['Cijena'] = data['Cijena'].drop(data['Cijena'][data.Cijena < 30000].index)
	data['Cijena'] = data['Cijena'].drop(data['Cijena'][data.Cijena > 500000].index)
	data = data.dropna(subset=['Cijena'])


	print("Task 14) Saving into csv file call 'sarajevo_stanovi.csv'\n")
	data.to_csv('sarajevski_stanovi.csv', header=True)
	print(data.head())
preprocessing1()
#
#
# def plot_corr(df, size=15):
# 	    corr = df.corr()    # data frame correlation function
# 	    fig, ax = plt.subplots(figsize=(size, size))
# 	    ax.matshow(corr)   # color code the rectangles by correlation value
# 	    plt.xticks(range(len(corr.columns)), corr.columns)  # draw x tick marks
# 	    plt.yticks(range(len(corr.columns)), corr.columns)  # draw y tick marks
# 	    plt.show()
#
# data = pd.read_csv('sarajevo_stanovi.csv')
#
# corr = data.corr()
#
#
# data = data.drop('Vrsta grijanja', axis=1)
# data = data.drop('Plin', axis=1)
# data = data.drop('Novogradnja', axis=1)
# data = data.drop('Podrum/Tavan', axis=1)
# data = data.drop('Balkon', axis=1)
# '''
#
#
# #v1 = data.drop('Lokacija', axis=1)
# #v2= data['Lokacija']
#
# '''
# X = data.drop('Cijena', axis=1).as_matrix()
# Y = data['Cijena'].as_matrix()
#
#
# min_max_scaler =  MinMaxScaler(feature_range=(0, 1))
# X = min_max_scaler.fit_transform(X)
# Y = min_max_scaler.fit_transform(Y)
# X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,Y,test_size=0.3)
# #print(data.corr())
#
#
# DTree = tree.DecisionTreeRegressor()
# DTree = DTree.fit(X_train, y_train)
# accuracy = DTree.score(X_train, y_train)
# accuracy1 = DTree.score(X_test, y_test)
# print("Decision Tree Regressor training: ", accuracy)
# print("Decision Tree Regressor testing: ", accuracy1)
#
#
# Lregression = LinearRegression()
# Lregression.fit(X_train,y_train)
# accuracy2 = Lregression.score(X_train, y_train)
# accuracy3 = Lregression.score(X_test, y_test)
# print("Linear regression training: ", accuracy2)
# print("Linear regression testing: ", accuracy3)
#
# SVR_Regressor = svm.SVR()
# SVR_Regressor.fit(X_train,y_train)
# accuracy2 = SVR_Regressor.score(X_train, y_train)
# accuracy3 = SVR_Regressor.score(X_test, y_test)
# print("SVR_Regressor training: ", accuracy2)
# print("SVR_Regressor testing: ", accuracy3)
#
#
# preds = SVR_Regressor.predict(X = X_test)
#
#
# data1 = {'predicted': [preds], 'true': [y_test]}
# df = pd.DataFrame(data1, columns = ['predicted', 'true'])
# df.to_csv('example.csv',  sep=',', header=True)
#
# plt.figure(figsize = (14,8))
# plt.plot(preds[:50])
# plt.plot(y_test[:50])
# plt.show()



'''
colormap = np.array(['red', 'lime', 'black', 'yellow', 'green', 'blue', 'pink', 'magenta'])
plt.figure(figsize=(15, 8))
plt.scatter(data.Plin, data.Lokacija, s = 40)
plt.title('Cijena')
plt.show()
'''


'''
colormap = np.array(['red', 'lime', 'black', 'yellow', 'green', 'blue', 'pink', 'magenta'])
#X_tsne = TSNE(learning_rate=100).fit_transform(v1)
pca = PCA(n_components=2)
X_pca = pca.fit(v1).transform(v1)

plt.figure(figsize=(15, 8))
#plt.subplot(1,2,1)
#plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=colormap[v2])
#plt.subplot(1,2,2)
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=colormap[v2])
plt.show()
'''

'''
print(data.isnull().values.any())
#plot_corr(data)
data['Cijena'].plot()
plt.show()
print(data['Cijena'].max())
print(data['Cijena'].min())
print(len(data))
	'''

