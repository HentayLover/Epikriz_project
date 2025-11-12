import tkinter as tk
from tkinter import scrolledtext

from convert_text import process_medical_text
from predict import predict_single_record


DIAGNOSIS_NAMES = {
    "C34-C35": "онкологические заболевания органов дыхания",
    "J44-J45": "хронические болезни нижних дыхательных путей", 
    "A15-A16": "туберкулез органов дыхания",
    "J45-J46": "астма и астматический статус",
    "D14-D15": "доброкачественные образования органов дыхания",
    "U07-U8": "COVID-19",
    "J15-J16": "бактериальная пневмония"
}

def process_text():
    """Функция для обработки текста из поля ввода"""
    input_text = text_input.get("1.0", tk.END).strip()  # Считываем текст из поля ввода
    
    procesed_input =  process_medical_text(input_text) 
    prediction = predict_single_record(procesed_input)
    diagnosis_code = prediction['predicted_diagnosis']
    diagnosis_name = DIAGNOSIS_NAMES.get(diagnosis_code, "неизвестный диагноз")
    # Проверяем, не пустой ли текст
    if not input_text:
        return
    
    res_string = f"Предсказания \n Получен диагноз: {prediction['predicted_diagnosis']} - {diagnosis_name} \n при уверенности {prediction['confidence']:.2%}"

    processed_text = res_string  

    text_output.config(state="normal")

    text_output.delete("1.0", tk.END)  
    text_output.insert("1.0", processed_text)  

    text_output.config(state="disabled")

def clear_all():
    """Функция для очистки всех полей"""
    text_input.delete("1.0", tk.END)  

    text_output.config(state="normal")
    text_output.delete("1.0", tk.END)  
    text_output.config(state="disabled")


root = tk.Tk()
root.title("Определитель заболевания лёгких")
root.geometry("600x400")


label_input = tk.Label(root, text="Введите текст:")
label_input.pack(pady=5)


text_input = scrolledtext.ScrolledText(root, height=8, width=70)
text_input.pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)


process_button = tk.Button(button_frame, text="Обработать текст", command=process_text)
process_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Очистить все", command=clear_all)
clear_button.pack(side=tk.LEFT, padx=5)


label_output = tk.Label(root, text="Результат:")
label_output.pack(pady=5)


text_output = scrolledtext.ScrolledText(root, height=8, width=70, state="disabled")
text_output.pack(pady=5)

root.mainloop()