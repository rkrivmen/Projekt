from flask import Flask, render_template,redirect, url_for, request, session,jsonify
app = Flask(__name__)
app.secret_key = 'see on stx salajane ja mitte keegi ei saa sisse'
# Route for the home page
@app.route('/', methods=['GET', 'POST'])

def home():
    f=open("paroolid.txt","r",encoding="utf-8")
    nimi={}
    for i in f:
        i=i.strip("\n").split(";")
        nimi[i[0]]=i[1]
    f.close()
    error = None
    if request.method == 'POST':
        a= request.form['username']
        b=request.form['password']
        if a in nimi and b ==nimi[a] :
            session["user"]=a
            return redirect(url_for('tabel'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('log.html', error=error)

@app.route("/tabel")
def tabel():
    f=open("paevad.txt","r",encoding="utf-8")
    ajad={}
    for i in f:
        i=i.strip("\n").split(";")
        ajad[i[0]]=i[1]
    if session["user"] in ajad:
        aeg=ajad[session["user"]].split(":")
    print(session["user"])
    return render_template("main.html")
@app.route('/send-date', methods=['POST'])
def send_date():
    if request.method == 'POST':
        data = request.get_json()
        session["year"] = data.get('year')
        session["month"] = data.get('month')
        session["day"] = data.get('day')
        return redirect(url_for('paev'))



# Endpoint to fetch highlighted days for a specific year and month
@app.route('/highlighted-days/<int:year>/<int:month>', methods=['GET'])
def get_highlighted_days(year, month):
    year = str(year)
    month = str(month)
    f=open("tegevus.txt","r",encoding="UTF-8")
    ajad={}
    highlighted_days={}
    for i in f:
        i=i.strip("\n").split(":")
        if i[0] in ajad:
            osa=ajad[i[0]]
            osa.append(i[1::])
            ajad[i[0]]=osa
        else:
            ajad[i[0]]=[i[1::]]
    f.close()
    aeg=ajad["artur"]
    for i in aeg:
        if i[0] in highlighted_days:
            osa=highlighted_days[str(i[0])]
            osa.append([str(i[1]),int(i[2])])
            highlighted_days[str(i[0])]=osa
        else:
            highlighted_days[str(i[0])]=[[str(i[1]),int(i[2])]]
    if year in highlighted_days:
        highlighted_for_year = highlighted_days[year]
        
        highlighted_for_month = [day[1] for day in highlighted_for_year if day[0] == month]
        return jsonify(highlighted_for_month)
    
    return jsonify([])

@app.route("/paev",methods=['GET', 'POST'])
def paev():
    if request.method == 'POST':
        b=[]
        c=0
        a= request.form['tegevus']
        f=open("tegevus.txt","r",encoding="utf-8")
        for i in f:
            b.append(i)
        f.close()
        f=open("tegevus.txt","w",encoding="utf-8")
        for i in b:
            g=i.strip("\n").split(":")
            if g[0]==session["user"] and g[1]==str(session["year"]) and g[2]==str(session["month"]) and g[3]==str(session["day"]):
                f.write(i.strip("\n")+" "+a+"\n")
                print(i)
                c=1
            else:
                f.write(i)
        if c!=1:
            f.write("\n"+session["user"]+":"+str(session["year"])+":"+str(session["month"])+":"+str(session["day"])+":"+a)

        file=open("paevad.txt","r",encoding="utf-8")
        f.close()

    f=open("tegevus.txt","r",encoding="utf-8")
        
    for i in f:
        i=i.strip("\n").split(":")
        if i[0]==session["user"] and i[1]==str(session["year"]) and i[2]==str(session["month"]) and i[3]==str(session["day"]):
            f.close()
            return render_template('paev.html', year=session["year"], month=session["month"], day=session["day"], txt=i[4])
    f.close()
    return render_template('paev.html', year=session["year"], month=session["month"], day=session["day"],txt="puudub")


if __name__ == '__main__':
    app.run(debug=True)


