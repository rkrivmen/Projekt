from flask import Flask, render_template,redirect, url_for, request, session

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

@app.route("/paev")
def paev():
    return render_template('paev.html', year=session["year"], month=session["month"], day=session["day"])


if __name__ == '__main__':
    app.run(debug=True)


