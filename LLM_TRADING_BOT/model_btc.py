import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Input
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from project import get_btc_price
from datetime import datetime
import time
import matplotlib.pyplot as plt
current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Désactivation des optimisations oneDNN

chemin_du_modele = 'modele_lstm_btc.h5'
sequence_length = 60
prix_btc_list = []
diff_list = []


while True:
    # Charger les données
    df = pd.read_csv('BTC-USD.csv')
    df.ffill(inplace=True)
    df.sort_values('Date', inplace=True)
    # Obtenir le dernier prix du Bitcoin et l'ajouter au DataFrame
    last_btc_price = get_btc_price()
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Supposons que votre DataFrame ait au moins les colonnes 'Date' et 'Close'
    new_row = {'Date': current_date, 'Close': last_btc_price}
    df = df._append(new_row, ignore_index=True)
    df.to_csv('BTC-USD.csv', index=False)

    # Sélectionner les colonnes nécessaires et préparer les données
    data = df['Close'].values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    # Créer des séquences
    def create_sequences(data, sequence_length):
        xs, ys = [], []
        for i in range(len(data) - sequence_length):
            x = data[i:(i + sequence_length)]
            y = data[i + sequence_length]
            xs.append(x)
            ys.append(y)
        return np.array(xs), np.array(ys)

    X, y = create_sequences(scaled_data, sequence_length)

    # Diviser en données d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Charger ou construire le modèle
    # if os.path.exists(chemin_du_modele):
    #     model = load_model(chemin_du_modele)
    #     # Recréer l'optimiseur
    #     model.compile(optimizer=Adam(), loss='mean_squared_error')
    # else:
    model = Sequential()
    model.add(Input(shape=(sequence_length, 1)))  # Spécifiez la forme d'entrée ici
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    model.compile(optimizer=Adam(), loss='mean_squared_error')

    # Entraîner le modèle avec les nouvelles données
    model.fit(X_train, y_train, epochs=40, batch_size=32, verbose=0)

    # Sauvegarder le modèle après chaque entraînement
    model.save(chemin_du_modele)
    last_sequence = scaled_data[-sequence_length:]
    last_sequence = last_sequence.reshape((1, sequence_length, 1))

    # Faire la prédiction
    predicted_price_scaled = model.predict(last_sequence)

    # Dénormaliser la prédiction
    predicted_price = scaler.inverse_transform(predicted_price_scaled)

    # Optionnel : Une pause peut être ajoutée ici pour espacer les itérations
    time.sleep(1)
    prix_predit = predicted_price[0][0]
    prix_btc = get_btc_price()
    diff = float(prix_predit) - float(prix_btc)
    prix_btc_list.append(prix_btc)
    diff_list.append(diff)

    # Afficher les valeurs
    print("Prix BTC actuel:", prix_btc)
    print("Différence:", prix_predit)

    # Vérifier si 200 valeurs ont été collectées
    if len(prix_btc_list) >= 2000:
        # Afficher le graphique
        plt.figure(figsize=(12, 6))

        # Créer une plage d'indices pour l'axe x
        x_axis = range(len(prix_btc_list))

        plt.plot(x_axis, prix_btc_list, label='Prix BTC', color='blue')
        plt.plot(x_axis, diff_list, label='Prix Prédit', color='red')

        plt.title('Comparaison du Prix BTC et des Prix Prédits sur 200 points')
        plt.xlabel('Point')
        plt.ylabel('Valeur')
        plt.legend()
        plt.show()
        break # Arrêter la boucle

    # Pause entre les itérations
