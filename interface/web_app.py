import streamlit as st
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

# Настройка страницы
st.set_page_config(
    page_title="Определитель заболевания лёгких",
    page_icon="🫁",
    layout="wide"
)

# Заголовок приложения
st.title("🫁 Определитель заболевания лёгких")

# Описание
st.markdown("Введите текст медицинского заключения для анализа:")

# Поле ввода текста
input_text = st.text_area(
    "Текст медицинского заключения:",
    height=200,
    placeholder="Введите текст медицинского заключения здесь..."
)

# Кнопки в колонках
col1, col2 = st.columns(2)

with col1:
    process_clicked = st.button("🔍 Обработать текст", type="primary", use_container_width=True)

with col2:
    clear_clicked = st.button("🧹 Очистить все", use_container_width=True)

# Обработка очистки
if clear_clicked:
    st.rerun()

# Обработка текста
if process_clicked and input_text.strip():
    with st.spinner("Обрабатываю текст..."):
        try:
            # Ваша существующая логика
            processed_input = process_medical_text(input_text) 
            prediction = predict_single_record(processed_input)
            diagnosis_code = prediction['predicted_diagnosis']
            diagnosis_name = DIAGNOSIS_NAMES.get(diagnosis_code, "неизвестный диагноз")
            
            # Отображение результатов
            st.success("Обработка завершена!")
            
            # Красивое отображение результата
            st.markdown("### 📊 Результаты анализа:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    label="Диагноз",
                    value=f"{diagnosis_code}",
                    delta=diagnosis_name
                )
            
            with col2:
                st.metric(
                    label="Уверенность предсказания",
                    value=f"{prediction['confidence']:.2%}"
                )
            
            # Дополнительная информация
            with st.expander("📋 Детали результата"):
                st.write(f"**Код диагноза:** {diagnosis_code}")
                st.write(f"**Наименование:** {diagnosis_name}")
                st.write(f"**Уверенность:** {prediction['confidence']:.2%}")
                st.write("\nВероятности по всем классам:")
                for diagnosis, prob in prediction["all_probabilities"].items():
                    st.write(f"  {diagnosis}: {prob:.2%}")
                
        except Exception as e:
            st.error(f"Произошла ошибка при обработке: {str(e)}")

elif process_clicked and not input_text.strip():
    st.warning("⚠️ Пожалуйста, введите текст для анализа")

# Инструкция в сайдбаре
with st.sidebar:
    st.header("ℹ️ Инструкция")
    st.markdown("""
    1. Введите текст медицинского заключения в поле выше
    2. Нажмите кнопку **'Обработать текст'**
    3. Получите результат анализа
    
    **Поддерживаемые диагнозы:**
    - C34-C35: Онкологические заболевания
    - J44-J45: Хронические болезни дыхательных путей
    - A15-A16: Туберкулез
    - J45-J46: Астма
    - D14-D15: Доброкачественные образования
    - U07-U8: COVID-19
    - J15-J16: Бактериальная пневмония
    """)

# Футер
st.markdown("---")
st.markdown("*Система автоматического анализа медицинских заключений*")