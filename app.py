from flask import Flask,render_template,request
import os
from utils import pipeline_model_cnn
from utils import pipeline_model_rnn
from utils import pipeline_model_mlp

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("main.html")


@app.route('/breed')
def breed():
    return render_template("breed.html")

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method=='POST':
        img = request.files['image']
        filename = img.filename
        path = os.path.join('static/uploads',filename)
        img.save(path)
        print(filename)
        predictions = pipeline_model_cnn(path)

        predictionscnn = pipeline_model_cnn(path)
        predictionsrnn = pipeline_model_rnn(path)
        predictionsmlp = pipeline_model_mlp(path)
        prediction=[]
        print(predictionscnn,end= "********")
        for i in range(len(predictionscnn)):
            temp = predictionscnn[i]
            if predictionscnn[i][1]<predictionsrnn[i][1]:
                if predictionsmlp[i][1]<predictionsrnn[i][1]:
                    temp=predictionsrnn[i]
                else:
                    temp=predictionsmlp[i]
            else:
                if predictionsmlp[i][1]<predictionscnn[i][1]:
                    temp=predictionscnn[i]
                else:
                    temp=predictionsmlp[i]
            prediction.append(temp)
        return render_template("predict.html",p="uploads/{}".format(filename),pred=prediction)
    return render_template("predict.html",p="images/dog.jpg",pred="")


if __name__ == '__main__':
    app.run(port=8000,debug=True)