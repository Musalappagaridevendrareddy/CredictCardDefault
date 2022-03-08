from flask import Flask, request, render_template, send_file
from flask import Response
import os
from flask_cors import CORS, cross_origin
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
# import flask_monitoringdashboard as dashboard
from predictFromModel import prediction

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
# dashboard.bind(app)
CORS(app)
upload_folder = 'Prediction_Output_File/'
# app.config['UPLOAD_FOLDER'] = upload_folder


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/predict", methods=['GET', 'POST'])
@cross_origin()
def predictRouteClient():
    try:
        if os.path.exists('Prediction_Output_File'):
            files = os.listdir('Prediction_Output_File')
            filtered = [file for file in files if file.endswith('.csv')]
            for file in filtered:
                p = os.path.join('Prediction_Output_File', file)
                os.remove(p)
        if request.method == 'POST' and request.form.get('action1') == 'Custom File Predict':
            f = request.files['csvfile']
            if os.path.exists('upload_data'):
                files = os.listdir('upload_data')
                filtered = [file for file in files if file.endswith('.csv')]
                for file in filtered:
                    p = os.path.join('upload_data', file)
                    os.remove(p)

            f.save('upload_data/' + f.filename)
            path = 'upload_data'
            pred_val = pred_validation(path)  # object initialization

            pred_val.prediction_validation()  # calling the prediction_validation function

            pred = prediction(path)  # object initialization

            # predicting for dataset present in database
            path = pred.predictionFromModel('Custom')
            return render_template('index.html', path="Prediction File created at %s!!!" % path, filename1='Custom_Predictions.csv')
        elif request.method == 'POST' and request.form.get('action2') == 'Default File Predict':
            path = 'Prediction_Batch_files'
            pred_val = pred_validation(path)  # object initialization

            pred_val.prediction_validation()  # calling the prediction_validation function

            pred = prediction(path)  # object initialization

            # predicting for dataset present in database
            path = pred.predictionFromModel('Default')
            return render_template('index.html', path="Prediction File created at %s!!!" % path, filename2='Default_Predictions.csv')

    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")


@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():
    try:
        if request.json['filepath'] is not None:
            path = request.json['filepath']
            train_valObj = train_validation(path)  # object initialization

            train_valObj.train_validation()  # calling the training_validation function

            trainModelObj = trainModel()  # object initialization
            trainModelObj.trainingModel()  # training the model for the files in the table


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")


@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = upload_folder + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

