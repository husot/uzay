from flask import Flask,render_template,request
import requests
from datetime import datetime


payload = {}
headers= {
  "apikey": "VE3bah46ie3zgKBH7FFdLRS3M8KJIYndIikpgm61"
}
        
birinci_tarih="2015-09-07"
ikinci_tarih="2015-09-08"
api_key="VE3bah46ie3zgKBH7FFdLRS3M8KJIYndIikpgm61"


app = Flask(__name__)
@app.route("/",methods = ["GET","POST"])

def index():
    if request.method == "POST":
        start_date = request.form.get("start_date") 
        print(start_date)
        end_date = request.form.get("end_date")
        #start_date = datetime.strptime(start_date, '%Y-%m-%d')
        #end_date = datetime.strptime(end_date, '%Y-%m-%d')
       

        url ="https://api.nasa.gov/neo/rest/v1/feed?start_date="+start_date+"&end_date="+end_date+"&api_key="+api_key
        response = requests.request("GET", url, headers=headers, data = payload)
        app.logger.info(response)
            
        infos =  response.json()
        deneme=infos["near_earth_objects"]
            
        ######### KMLER
        closest_points=[]
        for listeler in deneme:
            for item in deneme[listeler]:
                mesafeler=item["close_approach_data"]
                closest_points.append(mesafeler)

        kms=[]            
        for i in closest_points:
            miss_dict=i[0]
            miss_mesafe=miss_dict["miss_distance"]
            miss_kms=miss_mesafe["kilometers"]
            kms.append(miss_kms)

        float_kms=[]
        for i in kms:
            float_kms.append(float(i))

        ######## İSİMLER
        closest_names=[]
        for listeler in deneme:
            for item in deneme[listeler]:
                isimler=item["name"]
                closest_names.append(isimler)


        ######################
        isim_km=list(zip(closest_names,float_kms))
            # float_kms.sort()
            # top_10=float_kms[:10]
        sorted_list = sorted(isim_km, key=lambda x: x[1])
        sorted_list=sorted_list[:10]

        return render_template("index2.html", events = sorted_list)
    return render_template('index2.html')
if __name__ == "__main__":
    app.run(debug=True)
