from application_logging.logger import App_Logger
from sklearn.preprocessing import MinMaxScaler
from flask import Flask, request, render_template
from flask_cors import cross_origin
import pickle
import math


logger = App_Logger('logFiles/App.log')

app = Flask(__name__)

logger.info("INFO", 'Loading Pickle File For The Heating & Cooling Load')
model = pickle.load(open('Energy_Efficiency_RF_Heatingg.pkl', 'rb'))
model2 = pickle.load(open('Energy_Efficiency_RF_Coolingg.pkl', 'rb'))
logger.info("INFO", 'Pickle File Load For Heating & Cooling models')


@app.route("/", methods=['GET', 'POST'])
@cross_origin()
def home():
    """
    :Method Name : home
    :DESC : This Will Return The Home Page
    :return : render_template (index.html) page
    """
    try:
        logger.info('INFO', 'The Home Page Is Displayed')
        return render_template('index.html')

    except Exception as e:
        raise Exception(f"(home) - Could not find index.html Page \n" + str(e))


@app.route("/report", methods=['GET', 'POST'])
@cross_origin()
def report():
    """
    :Method Name : report
    :DESC : This Will Return The Feature Analysis Page
    :return : render_template (Report.html) page
    """
    try:
        logger.info('INFO', 'The Report Method Is Calling For Showing The Report')
        return render_template('Report.html')

    except Exception as e:
        raise Exception(f"(report) - Could not find report.html Page \n" + str(e))


@app.route("/predict", methods=['POST'])
@cross_origin()
def predict():
    """
        :Method Name : predict
        :DESC : This Will Return The Prediction of User Input
        :return : render_template (index.html) page With result
    """
    if request.method == 'POST':
        logger.info("INFO", 'Request Method : POST')

        try:
            relative_compactness = float(request.form['relative_compactness'])

            surface_area = float(request.form['surface_area'])

            wall_area = float(request.form['wall_area'])

            roof_area = float(request.form['roof_area'])

            overall_height = float(request.form['overall_height'])

            orientation = request.form['orientation']

            glazing_area = float(request.form['glazing_area'])

            glazing_area_distribution = float(request.form['glazing_area_distribution'])

            logger.info("INFO", 'All The Feature Is Selected By Value')


            logger.info('INFO', 'Predicting The Final Outputs')
            prediction_heating = round(math.exp(model.predict([[relative_compactness, surface_area, wall_area, roof_area,
                                                  overall_height, orientation, glazing_area, glazing_area_distribution]]
                                                )),2)
            prediction_cooling = round(math.exp(model2.predict([[relative_compactness, surface_area, wall_area, roof_area,
                                                  overall_height, orientation, glazing_area, glazing_area_distribution]]
                                                )),2)

            return render_template('index.html', prediction_text="The Heating Load & Cooling Load Is {} {}".format(
                prediction_heating, prediction_cooling))

        except Exception as e:
            raise Exception(f"(predict) - Their Is Something Wrong About Predict \n" + str(e))

    else:
        logger.info('INFO', 'Post Method Is Not Selected')
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
