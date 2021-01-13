from flask import Flask, render_template
import mysql.connector

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="",
	database="projekat"
)
app = Flask(__name__)

def convertTuple(tup): 
    strData =  ''.join(tup) 
    return strData

@app.route("/raspored")
def raspored():
	raspored = mydb.cursor()
	raspored.execute("SELECT * FROM raspored")
	resRaspored = raspored.fetchall()

	nastavnici = mydb.cursor()
	nastavnici.execute("SELECT DISTINCT nastavnik FROM raspored")
	resNastavnici = nastavnici.fetchall()

	vreme = mydb.cursor()
	vreme.execute("SELECT DISTINCT vreme FROM raspored")
	resVreme = vreme.fetchall()
	
	# u bazi je bio jedan podakat koji je nije imao \n na kraju i query nije prepoznao da se
	# ponavlja vrednost, iz tog razloga je odradjen ovaj kod ispod, kako bi se dobili
	# jedinstveni podaci za kolonu vreme (u bazi stoji Raf11 umesto Raf11\n)
	finallVreme = []
	for i in resVreme:
		convertData = convertTuple(i)
		finallVreme.append(convertData.rstrip())
	
	uniqueListVreme = []
	for n in finallVreme:
		if n not in uniqueListVreme:
			uniqueListVreme.append(n)
	
	return render_template("raspored.html", raspored=resRaspored, nastavnici=resNastavnici, vreme=uniqueListVreme)

if __name__ == '__main__':
	app.run(debug=True)