from flask import Flask, render_template, url_for, request, redirect, send_from_directory, session
import os, datetime


app = Flask(__name__)
app.static_folder = 'templates\static'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# reminder the comment the hell out of this

def write_logs(name='',password='', ip_address='', time=''):
    with open('logs.txt', 'a') as file:
        file.write('{ip_address}\t\t{time}\t\t{name}:::{password}\n'.format(
                            name=name,
                            password=password,
                            ip_address=ip_address,
                            time=time
                        ))

@app.route('/', methods=["POST", "GET"])
def index():

    # save logs
    with open('logs.txt', 'a') as file:
        write_logs(
            ip_address=request.remote_addr,
            time=datetime.datetime.now()
        )

    session['connected'] = ''

    if request.method == 'POST':
        input_name = request.form['name']
        input_password = request.form['password']
        try:
            with open(os.path.join(os.getcwd(), 'users', input_name, 'dont_remove.conf'), 'r') as file:
                password = file.read().split('\n')[0]
            if password == input_password:
                # correctly connected

                # save logs
                with open('logs.txt', 'a') as file:
                    write_logs(
                        name=input_name,
                        password=input_password,
                        ip_address=request.remote_addr,
                        time=datetime.datetime.now()
                    )

                # write name in session
                session['connected'] = input_name

                return redirect('/account/'+input_name)

            else:
                with open('logs.txt', 'a') as file:
                    write_logs(
                        name=input_name,
                        password=input_password,
                        ip_address=request.remote_addr,
                        time=datetime.datetime.now()
                    )

        except Exception as exc:
            with open('logs.txt', 'a') as file:
                    write_logs(
                        name=input_name,
                        password=input_password,
                        ip_address=request.remote_addr,
                        time=datetime.datetime.now()
                    )

    
    return render_template('index.html')



@app.route('/account/<name>', methods=["POST", "GET"])
def account(name):
    if request.method == 'GET':
        if session['connected'] != '':
            with open(os.path.join(os.getcwd(), 'users', name, 'dont_remove.conf'), 'r') as file:
                settings = file.read().split('\n')
            return render_template('account.html', name=name, files=os.listdir(os.path.join(os.getcwd(), 'users', name)), settings=settings)
        else:
            return redirect('/')


    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(os.getcwd(), 'users', name, file.filename))
        return redirect('/account/'+name)

@app.route('/download/<name>/<file>')
def download(name, file):
    return send_from_directory(os.path.join(os.getcwd(), 'users', name), file, as_attachment=True)


@app.route('/delete/<name>/<file>')
def delete(name, file):
    os.remove(os.path.join(os.getcwd(), 'users', name, file))
    return redirect('/account/'+name)


@app.route('/add-user', methods=['POST'])
def add_user():
    name = request.form['name']
    password = request.form['password']

    os.mkdir(os.path.join(os.getcwd(), 'users', name))
    with open(os.path.join(os.getcwd(), 'users', name, 'dont_remove.conf'), 'w') as file:
        file.write("%s\nregular" % password)

    return redirect('/account/' + session['connected'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

