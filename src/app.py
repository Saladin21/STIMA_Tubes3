from flask import Flask, render_template, url_for, request, redirect
import command as c
import database as db

app = Flask(__name__)
riwayat = {}
i = 0

@app.route('/', methods=['POST','GET'])
def index():
	global i
	if request.method == 'POST':
		chat_content = request.form['content']
		hasil = c.executeCommand(chat_content)
		hasil = hasil.replace('\n', '<br>')
		i+=1
		riwayat[i] = chat_content
		i+=1
		riwayat[i] = hasil
		return redirect(url_for('index'))
	else:
		return render_template('index.html', chats=riwayat)



if __name__ == '__main__':
	db.CreateTable()
	app.run(debug=True)