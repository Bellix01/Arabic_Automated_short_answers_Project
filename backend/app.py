from flask import Flask, request, jsonify
from keras.preprocessing.sequence import pad_sequences
import random
from keras.preprocessing.text import Tokenizer
from flask_cors import CORS
from keras.models import load_model
from keras.utils import custom_object_scope
from keras import backend as K
import numpy as np
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)


questions_data = [
    {"id": 1, "title": "كم عدد أولي العزم من الرسل؟", "description": ""},
    {"id": 2, "title": "من هو النبي الذي آمن به كل قومه؟", "description": ""},
    {"id": 3, "title": "ما هو اسم العبد الصالح الذي رافقه نبي الله موسى عليه السلام؟", "description": ""},
    {"id": 4, "title": "من هو حبيب الله؟", "description": ""},
    {"id": 5, "title": "من هو النبي الذي سمي: ” نبي الله”؟", "description": ""},
    {"id": 6, "title": "من هو النبي الذي دعا ربه: ” أني مسني الضر وأنت أرحم الراحمين”؟", "description": ""},
    {"id": 7, "title": "من هو النبي الملقب بروح الله؟", "description": ""},
    {"id": 8, "title": "من هو النبي الذي كاد به إخوته ورموه في البئر وهو صغيرًا؟", "description": ""},
    {"id": 9, "title": "من هم الأسباط؟", "description": ""},
    {"id": 10, "title": "من هو صفي الله؟", "description": ""},
    {"id": 11, "title": "من هو النبي الذي قال لابنه: ” يَا بُنَيَّ ارْكَب مَّعَنَا وَلَا تَكُن مَّعَ الْكَافِرِينَ”، كما ورد في القرآن الكريم؟", "description": ""},
    {"id": 12, "title": "من هو النبي الذي قال لابنه: ” يا بني لا تقصص رؤياك على إخوتك فيكيدوا لك كيدًا “، ومن كان ابنه؟", "description": ""},
    {"id": 13, "title": "كم سورة في القرآن الكريم سميت باسم نبي وما هي؟", "description": ""},
    {"id": 14, "title": "من هو أول البشر؟", "description": ""},
    {"id": 15, "title": "من هو خاتم الأنبياء والمرسلين؟", "description": ""},
    {"id": 16, "title": "من هو النبي الذي أيده الله تعالى بمعجزة إحياء الموتى؟", "description": ""},
    {"id": 17, "title": "من هو النبي الذي الذي انشق له البحر؟", "description": ""},
    {"id": 18, "title": "ما هي النبتة التي وضع سيدنا يونس أوراقها على جسده بعد أن خرج من فم الحوت؟", "description": ""},
    {"id": 19, "title": "ما هي مهنة نبي الله موسى عليه السلام؟", "description": ""},
    {"id": 20, "title": "ما هي مهنة نبي الله عيسى عليه السلام؟", "description": ""},
    {"id": 21, "title": "من هو النبي الكريم الذي أُرسل إلى قوم عاد؟", "description": ""},
    {"id": 22, "title": "ما هي قصة قوم عاد؟", "description": ""},
]


def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

with custom_object_scope({'recall_m': recall_m, 'precision_m': precision_m, 'f1_m': f1_m}):
    print("Before loading the model")
    model = load_model("transformer.h5")
    print("After loading the model")



reponse = pd.read_csv('C:/Users/DELL/Documents/MBD/S3/Deep Learning MBD 2023/Project/reponse.csv', encoding='utf-8')
reponse = reponse.dropna()
reponse['reponse'] = reponse['reponse'].astype(str)
tokenizer = Tokenizer(filters=''''!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ''''' )
tokenizer.fit_on_texts(reponse['reponse'])


@app.route('/questions', methods=['GET'])
def get_questions():
    # Shuffle the questions and return the first 10
    random.shuffle(questions_data)
    selected_questions = questions_data[:10]
    return jsonify(selected_questions)

@app.route('/submit-all-answers', methods=['POST'])
def submit_all_answers():
    try:
        data = request.get_json()
        answers = data.get('answers', [])
        predictions_list = []

        for answer_data in answers:
            answer_text = answer_data.get('answer')
            sequence = tokenizer.texts_to_sequences([answer_text])
            padded_sequence = pad_sequences(sequence, maxlen=30)
            predictions = model.predict(padded_sequence)
            predicted_class = int(np.argmax(predictions))
            predictions_list.append(predicted_class)

        response = {
            'predictions': predictions_list
        }

        return jsonify(response)


    except Exception as e:
        app.logger.error(f"Error processing answers: {str(e)}")
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
