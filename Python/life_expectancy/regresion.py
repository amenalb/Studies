# -*- coding: utf-8 -*-
"""Nalborczyk_Paskowski_Regresja

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14PyullvVzfH1xaQYpFjkE2XJGvIzSvRJ

# Projekt praktyczny (regresja)

## Zbiór danych *Life Expectancy Data.csv* następujące kolumny:
- Country - państwo\
- Status - kraj rozwijający się / rozwinięty\
- Life expectancy - oczekiwana długość życia w latach\
- Adult Mortality - śmiertelność wśród dorosłych, prawdopodobieństwo śmierci w wieku między 15 a 60 lat na 1000 osób\
- infant deaths - śmiertelnośc noworodków w przeliczeniu na 1000 urodzeń\
- Alcohol - konsumpcja alkoholu wśród osób 15+ [w litrach]\
- percentage expenditure - udział wydatków na sektor zdrowia w PKB per capita\
- Hepatitis B - udział zaszczepionych dzieci do 1 roku życia na WZW typu B\
- Measles - liczba odnotowanych przypadków zachorowań na odrę na 1000 mieszkańców\
- BMI\
- under-five deaths - liczba śmierci na 1000 dzieci poniżej 5 roku życia\
- Polio - udział zaszczepionych dzieci do 1 roku życia na Polio\
- Total expenditure - udział wydatków na sektor zdrowia w całości wydatków rządowych\
- Diphtheria - udział zaszczepionych dzieci do 1 roku życia na błonicę i krztusiec\
- HIV/AIDS - śmierci dzieci poniżej 5 roku życia na 1 000 żywych urodzeń spowodowane HIV/AIDS\
- GDP - PKB per capita\
- Population - liczba mieszkańców\
- thinness 1-19 years - rozpowszechnienie chudości w wieku 1 -19 lat\
- thinness 5-9 years - rozpowszechnienie chudości w wieku 5 - 9 lat\
- Income composition of resources - Wskaźnik rozwoju społecznego HDI Human Development Index\
- Schooling - liczba lat nauczania szkolnego\

# Celem projektu jest:
1. przygotowanie i analiza dostarczonych danych
2. budowa i analiza jakości modeli do prognozy oczekiwanej długości życia w latach
3. ocena opracowanych modeli

## Zaimportuj biblioteki
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""## Wczytaj plik *Life Expectancy Data.csv* oraz wyświetl kilka pierwszych wierszy


"""

file_path = 'Life Expectancy Data.csv'
df = pd.read_csv('Life Expectancy Data.csv', delimiter=';')

df.head()

"""Czyszczenie zbioru"""

# Sprawdzenie typów danych
print(df.dtypes)

"""# Preprocessing
- wyświetl rozmiar zbioru
- sprawdź ilość NaN-ów
- jesli występują kolumny z dużą lością NaN-ów usuń je
- sprawdź statystyki NaN-ów dla wierszy (m.in. jaka jest mininalna, maxymalna, srednia liczba nanów w wierszu). Jeśli są wiersze, dla których jest >=5 braki usuń je i zresetuj indexy
- wyświetl wiersze od 170 do 175
- pozostałe NaN-y uzupełnij średnią
- oblicz statystyki opisowe
"""

# wyświetlanie ogólnych informacji o zbiorze
df.info()
print("Rozmiar zbioru danych:", df.shape)
print("Ilość NaN-ów w zbiorze danych:", df.isna().sum().sum())

# Usuwanie kolumn z dużą ilością NaN-ów (więcej niż 50% braków)
threshold = 0.5
df = df.loc[:, df.isna().mean() < threshold]

# Statystyki NaN-ów dla wierszy
nan_stats = df.isna().sum(axis=1)
print("Minimalna liczba NaN-ów w wierszu:", nan_stats.min())
print("Maksymalna liczba NaN-ów w wierszu:", nan_stats.max())
print("Średnia liczba NaN-ów w wierszu:", nan_stats.mean())

# Usunięcie wierszy z >= 5 brakami i zresetowanie indeksów
df = df[nan_stats < 5].reset_index(drop=True)

# Wyświetlenie wierszy od 170 do 175
print("Wiersze od 170 do 175:")
print(df.iloc[170:176])

# Uzupełnienie pozostałych NaN-y średnią z kolumny
df = df.fillna(df.mean(numeric_only=True))

# statystyki opisowe
df.describe()

# Obliczenie statystyk opisowych
print("Statystyki opisowe zbioru danych:")
print(df.describe())

# Wyświetlenie wierszy od 170 do 175
print("Wiersze od 170 do 175:")
df.iloc[170:176]

"""# Wizualizacja

Wykonaj wykresy rozkładu (histogram i ramka-wąsy) zmiennej *Life expectancy* skategoryzowane w zalezności od statusu kraju. Zinterpretuj wyniki.
"""

plt.figure(figsize=(14, 6))

# Histogram
plt.subplot(1, 2, 1)
sns.histplot(data=df, x='Life expectancy', hue='Status', multiple='stack', kde=True)
plt.title('Histogram oczekiwanej długości życia według statusu kraju')
plt.xlabel('Oczekiwana długość życia')
plt.ylabel('Liczba przypadków')

# Ramka-wąsy
plt.subplot(1, 2, 2)
sns.boxplot(data=df, x='Status', y='Life expectancy')
plt.title('Ramka-wąsy oczekiwanej długości życia według statusu kraju')
plt.xlabel('Status kraju')
plt.ylabel('Oczekiwana długość życia')

plt.tight_layout()
plt.show()

"""## Interpretacja Histogramu oczekiwanej długości życia według statusu kraju
### Kraje rozwijające się (Developing)
W większość krajów rozwijających się ma oczekiwaną długość życia w okolicy 75 lat.
Dla krajów rozwijąjących się oczekiwany wiek życia jest bardzo rozproszony, zawiera się pomiędzy 50-85 lat.
Kształt rozkładu: Lewoskośny (asymetryczny)
### Kraje rozwinięte (Developed)
Histogram ma szczyt w okolicach 80 lat, co oznacza, że większość krajów rozwiniętych ma oczekiwaną długość życia w tym przedziale.
Dane są bardziej skoncentrowane wokół wyższych wartości oczekiwanej długości życia (od 75 do 85 lat)
Kształt rozkładu: Lewoskośny (asymetryczny)

Wykres ipokazuje wyraźne różnice w oczekiwanej długości życia pomiędzy krajami rozwiniętymi i rozwijającymi się. Kraje rozwinięte mają wyższą oczekiwaną długość życia w porównaniu do krajów rozwijających się. W krajach rozwiniętych oczekiwana długość życia jest bardziej jednolita, podczas gdy w krajach rozwijających się jest bardziej zróżnicowana.

# Korelacja
Wykonaj macierz korelacji dla zmiennych ilościowych. Z którymi zmiennymi skorelowana jest zmienna *Life expectancy*. Zinterpretuj te korelacje.
"""

df.head()

# Wybierz tylko zmienne numeryczne
numeric_df = df.select_dtypes(include=['float64', 'int64'])

# Obliczamy macierz korelacji
correlation_matrix = numeric_df.corr()

# Wyświetlamy macierz korelacji
print("Macierz korelacji:")
print(correlation_matrix)

# Wykres macierzy korelacji
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
plt.title('Macierz korelacji zmiennych ilościowych')
plt.show()

"""Widać zależność midzy oczekiwanym wiekiem życia, a
Wskaźnik rozwoju społecznego HDI.

Natomiast udział wydatków na sektor zdrowia w PKB kraju nie ma wpływu na oczekiwany wiek życia.

# Regresja linowa jednej zmiennej
- Zbuduj model regresji liniowej prostej (jednej zmiennej) umozliwijący przewidywanie długości życia. Odpowiednio przygotuj X (zmienna objaśniająca) i y (zmienna objasniana).
- Wykonaj predykcję dla zbioru treningowego i testowego
- Oblicz metryki (R2, MAE, MSE, RMSE). Oceń jakość modelu (dobrze dopasowany, przetrenowany, niedotrenowany).
"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# Przygotowanie zmiennych objaśniającej (X) i zmiennej objaśnianej (y)
X = df[['GDP']].dropna()
y = df.loc[X.index, 'Life expectancy'].dropna()

# Upewnij się, że X i y mają te same indeksy po usunięciu brakujących wartości
X = X.loc[y.index]

# Podział na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Stworzenie i trenowanie modelu regresji liniowej
model = LinearRegression()
model.fit(X_train, y_train)

# Predykcja dla zbioru treningowego i testowego
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Obliczenie metryk
r2_train = r2_score(y_train, y_train_pred)
r2_test = r2_score(y_test, y_test_pred)

mae_train = mean_absolute_error(y_train, y_train_pred)
mae_test = mean_absolute_error(y_test, y_test_pred)

mse_train = mean_squared_error(y_train, y_train_pred)
mse_test = mean_squared_error(y_test, y_test_pred)

rmse_train = np.sqrt(mse_train)
rmse_test = np.sqrt(mse_test)

# Ocena jakości modelu
train_size = X_train.shape[0]
test_size = X_test.shape[0]

results = {
    "R2 Train": r2_train,
    "R2 Test": r2_test,
    "MAE Train": mae_train,
    "MAE Test": mae_test,
    "MSE Train": mse_train,
    "MSE Test": mse_test,
    "RMSE Train": rmse_train,
    "RMSE Test": rmse_test,
    "Train Size": train_size,
    "Test Size": test_size
}

results

"""# Interpretacja wyników

* Porównanie wartości R² dla zbioru treningowego i testowego pomoże ocenić, jak dobrze model radzi sobie z dopasowaniem do danych treningowych oraz jego ogólność na danych.
  * Są stosunkowo niskie. Wartość R² bliska 0 sugeruje, że model nie wyjaśnia dobrze zmienności długości życia na podstawie PKB per capita.
  * R² dla zbioru testowego jest jeszcze niższe niż dla zbioru treningowego, co sugeruje, że model może nie generalizować dobrze na nowych danych.
* MAE, MSE, RMSE - metryki błędu pozwalają zrozumieć przeciętny błąd przewidywania (MAE), kwadratowy błąd przewidywania (MSE) oraz pierwiastek z MSE (RMSE) dla obu zbiorów danych.
  * MAE (średni absolutny błąd) dla zbioru treningowego i testowego są zbliżone (ok. 5.92 i 6.01), co oznacza, że model przeciętnie myli się o około 6 lat w przewidywaniu długości życia.
  * MSE (średni kwadratowy błąd) i RMSE (pierwiastek z MSE) są również zbliżone między zbiorem treningowym a testowym, co sugeruje, że błędy są w podobnym zakresie dla obu zbiorów.
* Train Size i Test Size - informacje o wielkości zbiorów treningowego i testowego.

Ocena modelu:
* Niedotrenowanie: Niskie wartości R² i stosunkowo wysokie wartości MAE i RMSE wskazują, że model może być niedotrenowany, co oznacza, że nie wyjaśnia dostatecznie dobrze zależności między zmiennymi.
* Dane treningowe i testowe: Podobne wartości metryk dla danych treningowych i testowych sugerują, że model nie jest przetrenowany. Przetrenowanie występuje wtedy, gdy model bardzo dobrze dopasowuje się do danych treningowych, ale słabo radzi sobie z danymi testowymi. W tym przypadku tak nie jest.

# Podziel zbiór danych na zbiór treningowy i testowy w stodunku 80% do 20%.
"""

# Podział na zbiór treningowy i testowy w stosunku 80% do 20%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Sprawdzenie rozmiaru zbiorów treningowego i testowego
train_size = X_train.shape[0]
test_size = X_test.shape[0]

train_size, test_size

"""# Regresja linowa wielu zmiennych
- Zbuduj model regresji liniowej wielu zmiennych umozliwijący przewidywanie długości życia. Odpowiednio przygotuj X (zmienne objaśniające) i y (zmienna objasniana).
- Wykonaj predykcję dla zbioru treningowego i testowego
- Oblicz metryki (R2, MAE, MSE, RMSE). Oceń jakość modelu (dobrze dopasowany, przetrenowany, niedotrenowany).
"""

# Przygotowanie zmiennych objaśniających (X) i zmiennej objaśnianej (y)
# Wybór wszystkich dostępnych zmiennych objaśniających
X = df.drop(columns=['Life expectancy', 'Country', 'Status'])
y = df['Life expectancy']

# Usunięcie wierszy z brakującymi wartościami
X = X.dropna()
y = y.loc[X.index]

# Podział na zbiór treningowy i testowy w stosunku 80% do 20%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Stworzenie i trenowanie modelu regresji liniowej wielu zmiennych
model_multiple = LinearRegression()
model_multiple.fit(X_train, y_train)

# Predykcja dla zbioru treningowego i testowego
y_train_pred_multiple = model_multiple.predict(X_train)
y_test_pred_multiple = model_multiple.predict(X_test)

# Obliczenie metryk
r2_train_multiple = r2_score(y_train, y_train_pred_multiple)
r2_test_multiple = r2_score(y_test, y_test_pred_multiple)

mae_train_multiple = mean_absolute_error(y_train, y_train_pred_multiple)
mae_test_multiple = mean_absolute_error(y_test, y_test_pred_multiple)

mse_train_multiple = mean_squared_error(y_train, y_train_pred_multiple)
mse_test_multiple = mean_squared_error(y_test, y_test_pred_multiple)

rmse_train_multiple = np.sqrt(mse_train_multiple)
rmse_test_multiple = np.sqrt(mse_test_multiple)

results_multiple = {
    "R2 Train Multiple": r2_train_multiple,
    "R2 Test Multiple": r2_test_multiple,
    "MAE Train Multiple": mae_train_multiple,
    "MAE Test Multiple": mae_test_multiple,
    "MSE Train Multiple": mse_train_multiple,
    "MSE Test Multiple": mse_test_multiple,
    "RMSE Train Multiple": rmse_train_multiple,
    "RMSE Test Multiple": rmse_test_multiple
}

results_multiple

"""# R2 (Coefficient of Determination):

* Wynik R2 dla zbioru treningowego wynosi około 0.877, co oznacza, że model wyjaśnia około 87.7% wariancji danych treningowych.
* Wynik R2 dla zbioru testowego wynosi około 0.819, co oznacza, że model wyjaśnia około 81.9% wariancji danych testowych.
* Wartości R2 są zbliżone dla zbioru treningowego i testowego, co sugeruje, że model jest dobrze dopasowany i nie ma zbyt dużego przeuczenia ani niedouczenia.

# MAE (Mean Absolute Error):

* Średni błąd bezwzględny dla zbioru treningowego wynosi około 2.083, a dla zbioru testowego około 2.848.
* MAE jest miarą średniej wartości bezwzględnej różnicy między prognozowanymi a rzeczywistymi wartościami. Im niższa wartość MAE, tym lepiej.
# MSE (Mean Squared Error):

* Średni błąd kwadratowy dla zbioru treningowego wynosi około 7.725, a dla zbioru testowego około 13.857.
* MSE jest miarą średniej kwadratowej różnicy między prognozowanymi a rzeczywistymi wartościami. Im niższa wartość MSE, tym lepiej.
# RMSE (Root Mean Squared Error):

* Pierwiastek błędu średniokwadratowego dla zbioru treningowego wynosi około 2.779, a dla zbioru testowego około 3.722.
* RMSE jest miarą pierwiastka kwadratowego średniego błędu kwadratowego. Im niższa wartość RMSE, tym lepiej.


"""