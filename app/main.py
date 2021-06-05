import pickle

from flask import Flask, render_template, request

app = Flask(
    __name__, template_folder='../templates',
    static_folder='../static'
    )
# открываем подготовленную модель
with open('model/rf.pkl', 'rb') as pkl_file:
    clf = pickle.load(pkl_file)


# главная страница
@app.route('/', methods=['post', 'get'])
def login():
    # вывод начальной формы
    if request.method == 'GET':
        return render_template(
            'start.html',
            message='Pass parameters to model through the form below:'
            )
    # получение данных формы
    if request.method == 'POST':
        data = dict(request.form)
        for key, value in data.items():
            if data[key] == '':
                data[key] = 0
            try:
                data[key] = float(data[key])
            except ValueError:
                return render_template(
                    'start.html', message='Wrong inputs, try again'
                    )
        x = [data['petal-length'],
             data['petal-width'],
             data['sepal-length'],
             data['sepal-width']
             ]
        y_pred = int(clf.predict([x]))
        classes = ['setosa', 'versicolor', 'virginica']
        return render_template(
            'result.html',
            result_msg=f'Your iris is {classes[y_pred]}',
            iris_image=f'{classes[y_pred]}.jpg'
            )


if __name__ == '__main__':
    app.run()
