import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib

from config import example_1, example_2, example_3, example_4


def predict_single_record(single_row_data):
    """
    Предсказывает диагноз для одной строки данных

    Args:
        single_row_data: данные в формате словаря или pandas Series
                        с теми же признаками, что и в обучающих данных

    Returns:
        dict: словарь с результатами предсказания
    """

    model = tf.keras.models.load_model("modal/medical_epicrisis_cnn_lstm_model.keras")
    scaler = joblib.load("modal/scaler.pkl")
    label_encoder = joblib.load("modal/label_encoder.pkl")
    feature_columns = joblib.load("modal/feature_columns.pkl")


    if isinstance(single_row_data, dict):
        df_single = pd.DataFrame([single_row_data])
    else:
        df_single = pd.DataFrame([single_row_data])


    missing_columns = set(feature_columns) - set(df_single.columns)
    if missing_columns:
        raise ValueError(f"Отсутствуют необходимые признаки: {missing_columns}")

    df_single = df_single.fillna(0)

    X = df_single[feature_columns].values
    X_scaled = scaler.transform(X)
    X_reshaped = X_scaled.reshape(X_scaled.shape[0], X_scaled.shape[1], 1)


    y_pred = model.predict(X_reshaped, verbose=0)
    y_pred_class = np.argmax(y_pred, axis=1)[0]
    y_pred_prob = np.max(y_pred, axis=1)[0]


    predicted_diagnosis = label_encoder.inverse_transform([y_pred_class])[0]


    class_probabilities = {}
    for i, class_name in enumerate(label_encoder.classes_):
        class_probabilities[class_name] = float(y_pred[0][i])

    result = {
        "predicted_diagnosis": predicted_diagnosis,
        "confidence": float(y_pred_prob),
        "all_probabilities": class_probabilities,
        "predicted_class_index": int(y_pred_class),
    }

    return result


if __name__ == "__main__":
    example_data = example_2

    try:
        prediction = predict_single_record(example_data)
        print("Результат предсказания:")
        print(f"Диагноз: {prediction['predicted_diagnosis']}")
        print(f"Уверенность: {prediction['confidence']:.2%}")
        print("\nВероятности по всем классам:")
        for diagnosis, prob in prediction["all_probabilities"].items():
            print(f"  {diagnosis}: {prob:.2%}")

    except Exception as e:
        print(f"Ошибка при предсказании: {e}")
