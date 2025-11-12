from convert_text import process_medical_text
from predict import predict_single_record

medical_text = """
    Пациент жалуется на сильный кашель, температуру 38.5, одышку при нагрузке, 
    слабость. При аускультации выслушиваются хрипы. Артериальное давление 130/70, 
    ЧСС 96, сатурация 83%.
    """

example_1 =  process_medical_text(medical_text)  
prediction = predict_single_record(example_1)
print("Результат предсказания:")
print(f"Диагноз: {prediction['predicted_diagnosis']}")
print(f"Уверенность: {prediction['confidence']:.2%}")
print("\nВероятности по всем классам:")
for diagnosis, prob in prediction["all_probabilities"].items():
    print(f"  {diagnosis}: {prob:.2%}")

