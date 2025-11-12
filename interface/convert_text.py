import re

class MedicalFeatureExtractor:
    """Извлечение признаков из медицинского текста"""
    
    def __init__(self):
        self.symptom_patterns = self._load_symptom_patterns()
        self.medical_terms = self._load_medical_terms()
        
    def _load_symptom_patterns(self):
        """Паттерны для поиска симптомов"""
        return {
            'кашель': {
                'keywords': ['кашель', 'кашля', 'кашле', 'откашливан'],
                'intensity': {
                    'легкий': ['покашливан', 'легкий кашель', 'незначительный кашель'],
                    'средний': ['кашель', 'малопродуктивный', 'постоянный кашель'],
                    'сильный': ['сильный кашель', 'надсадный', 'мучительный', 'приступ кашля']
                }
            },
            'температура': {
                'keywords': ['температур', 'лихорадк', 'жар', 'озноб', 'гипертерми', 'субфебрильн', 'фебрильн'],
                'intensity': {
                    'легкая': ['субфебрильн', '37.', '37,'],
                    'средняя': ['температур', '38.', '38,', 'фебрильн'],
                    'высокая': ['высокая температур', '39.', '39,', '40.', '40,', 'гипертерми']
                }
            },
            'одышка': {
                'keywords': ['одышк', 'затруднен', 'дыхан', 'нехватк', 'воздух', 'удушь', 'диспноэ'],
                'intensity': {
                    'легкая': ['одышка при нагрузк', 'незначительная одышка'],
                    'средняя': ['одышк', 'затруднен', 'дыхан'],
                    'тяжелая': ['одышка в покое', 'сильная одышка', 'удушь']
                }
            },
            'слабость': {
                'keywords': ['слабост', 'усталост', 'недомогание', 'разбитост', 'астени', 'утомляемост'],
                'intensity': {
                    'легкая': ['слабост', 'недомогание'],
                    'средняя': ['выраженная слабост', 'сильная слабост'],
                    'тяжелая': ['резкая слабост', 'обездвиженност']
                }
            },
            'головная_боль': {
                'keywords': ['головная боль', 'головные боли', 'головной боль', 'цефалги', 'мигрен', 'болит голова'],
                'intensity': {
                    'легкая': ['головная боль', 'незначительная головная боль'],
                    'средняя': ['сильная головная боль', 'выраженная головная боль'],
                    'тяжелая': ['нестерпимая головная боль', 'мучительная головная боль']
                }
            },
            'рвота': {
                'keywords': ['рвот', 'тошнот', 'тошнит'],
                'intensity': {
                    'легкая': ['тошнот', 'подташниван'],
                    'средняя': ['рвот', 'однократн'],
                    'тяжелая': ['многократн', 'неукротим']
                }
            },
            'насморк': {
                'keywords': ['насморк', 'заложенност', 'нос', 'ринит', 'выделен', 'носа'],
                'intensity': {
                    'легкая': ['насморк', 'заложенност носа'],
                    'средняя': ['сильный насморк', 'обильные выделен'],
                    'тяжелая': ['постоянный насморк', 'непроходимост']
                }
            },
            'боль_в_груди': {
                'keywords': ['боль в груд', 'боли в груд', 'кардиалги', 'болит груд', 'боль за грудин'],
                'intensity': {
                    'легкая': ['незначительная боль', 'дискомфорт в груд'],
                    'средняя': ['боль в груд', 'боли в груд'],
                    'тяжелая': ['сильная боль', 'острая боль', 'нестерпимая боль']
                }
            }
        }
    
    def _load_medical_terms(self):
        """Медицинские термины для поиска"""
        return {
            'аускультация': ['аускультац', 'хрип', 'дыхан', 'жесткое дыхан', 'ослаблен'],
            'перкуссия': ['перкусс', 'перкуторн'],
            'пальпация': ['пальпац', 'пальпирует'],
            'отеки': ['отек', 'пастозност', 'отечност'],
            'цианоз': ['цианоз', 'синюшност', 'акроцианоз'],
            'тахикардия': ['тахикарди', 'учащен', 'сердцебиен', 'чсс'],
            'сатурация': ['сатурац', 'spo2', 'насыщен', 'кислород'],
            'артериальное_давление': ['артериальн', 'давлен', 'ад'],
            'анализ_крови': ['анализ кров', 'лейкоцит', 'гемоглобин', 'соэ', 'с-реактивн']
        }
    
    def find_symptom_intensity(self, text, symptom_name):
        """Находит интенсивность симптома в тексте"""
        if not text or not isinstance(text, str):
            return 0
            
        text_lower = text.lower()
        symptom_data = self.symptom_patterns.get(symptom_name)
        
        if not symptom_data:
            return 0

        found_keywords = [kw for kw in symptom_data['keywords'] if kw in text_lower]
        if not found_keywords:
            return 0

        intensity = 1 
        
        intensity_levels = symptom_data.get('intensity', {})
        

        if 'тяжелая' in intensity_levels:
            for pattern in intensity_levels['тяжелая']:
                if pattern in text_lower:
                    return 3

        if 'средняя' in intensity_levels:
            for pattern in intensity_levels['средняя']:
                if pattern in text_lower:
                    intensity = max(intensity, 2)
        
        return intensity
    
    def find_medical_term(self, text, term_name):
        """Проверяет наличие медицинского термина"""
        if not text or not isinstance(text, str):
            return 0
            
        text_lower = text.lower()
        keywords = self.medical_terms.get(term_name, [])
        
        return 1 if any(kw in text_lower for kw in keywords) else 0
    
    def extract_numeric_values(self, text):
        """Извлекает числовые значения из текста"""
        features = {}
        

        temp_match = re.search(r'температур[а-я]*\s*(\d+[.,]\d+)', text.lower())
        features['vital_temp_body'] = float(temp_match.group(1).replace(',', '.')) if temp_match else 0.0

        bp_match = re.search(r'давлен[а-я]*\s*(\d+)[/\s]?(\d+)', text.lower())
        features['vital_bp_systolic'] = float(bp_match.group(1)) if bp_match else 0.0
        features['vital_bp_diastolic'] = float(bp_match.group(2)) if bp_match else 0.0
        

        heart_match = re.search(r'(чсс|пульс|сердцебиен[а-я]*)\s*(\d+)', text.lower())
        heart_rate = float(heart_match.group(2)) if heart_match else 0.0
        features['vital_heart_rate'] = heart_rate
        features['vital_pulse'] = heart_rate

        sat_match = re.search(r'(сатурац[а-я]*|spo2)\s*(\d+)', text.lower())
        features['vital_saturation'] = float(sat_match.group(2)) if sat_match else 0.0

        resp_match = re.search(r'(дыхан[а-я]*|чд)\s*(\d+)', text.lower())
        features['vital_resp_rate'] = float(resp_match.group(2)) if resp_match else 0.0

        features['lab_wbc'] = 0.0
        features['lab_crp'] = 0
        features['lab_glucose'] = 0.0
        features['lab_total_protein'] = 0.0
        
        return features
    
    def extract_features_from_text(self, text):
        """Извлекает все признаки из текста"""
        features = {}
        
        try:

            numeric_features = self.extract_numeric_values(text)
            features.update(numeric_features)
            
  
            for symptom_name in self.symptom_patterns.keys():
                intensity = self.find_symptom_intensity(text, symptom_name)
                features[f'has_{symptom_name}'] = 1 if intensity > 0 else 0
                features[f'intensity_{symptom_name}'] = intensity
            
            for term_name in self.medical_terms.keys():
                has_term = self.find_medical_term(text, term_name)
                features[f'has_{term_name}'] = has_term
            

            features['text_length_complaints'] = len(text)
            features['text_length_history'] = len(text)
            features['text_length_examination'] = len(text)

            symptom_names = list(self.symptom_patterns.keys())
            total_symptoms = sum(features.get(f'has_{symptom}', 0) for symptom in symptom_names)
            total_intensity = sum(features.get(f'intensity_{symptom}', 0) for symptom in symptom_names)
            
            features['total_symptoms_count'] = total_symptoms
            features['total_symptoms_intensity'] = total_intensity
            features['symptoms_diversity'] = total_symptoms / len(symptom_names) if symptom_names else 0
            
        except Exception as e:
            print(f"Ошибка при извлечении признаков: {e}")
        
        return features

def process_medical_text(text):
    """
    Обрабатывает медицинский текст и возвращает признаки в нужном формате
    
    Args:
        text (str): Медицинский текст
        
    Returns:
        dict: Словарь с признаками в формате example_1
    """
    extractor = MedicalFeatureExtractor()
    features = extractor.extract_features_from_text(text)
    return features

# Пример использования
if __name__ == "__main__":
    medical_text = """
    Пациент жалуется на сильный кашель, температуру 38.5, одышку при нагрузке, 
    слабость. При аускультации выслушиваются хрипы. Артериальное давление 130/70, 
    ЧСС 96, сатурация 83%.
    """
    result = process_medical_text(medical_text)  
    print("example_1 = {")
    for key, value in result.items():
        if isinstance(value, float):
            print(f"    '{key}': {value},")
        else:
            print(f"    '{key}': {value},")
    print("}")
    
    example_1 = result
    print(f"\nИзвлечено {len(example_1)} признаков")