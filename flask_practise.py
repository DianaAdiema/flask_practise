from flask import Flask, render_template, request, Response

import psycopg2
import pygal

app = Flask(__name__)


@app.route('/')
def hello_world():
    # when the route runs, return back to index.html
    return render_template('index.html')


@app.route('/aboutUs')
def aboutUs():
    # when the route runs, return back to index.html
    return render_template('aboutUs.html')


@app.route('/addMember', methods=['GET','POST'])
def addMember():
    if request.method=='POST':
         conn=psycopg2.connect(database="sunsetdb",
                              user="postgres",
                              password="drugnovmi5",
                              host="localhost",
                              port="5432")

         sql="INSERT INTO memberstbl VALUES (%s,%s,%s,%s,%s,%s)"
         # NB: the real values were not parsed
         m_no = request.form['member_no']
         dob = request.form['dob']
         fname = request.form['fname']
         lname = request.form['lname']
         gender = request.form['gender']
         hdate = request.form['hdate']

         # Create a cursor using the conn
         # The cursor will then execute the SQL query. Cursor, variable, is connected to SQL
         cursor=conn.cursor()
         tuple=(m_no,dob,fname,lname,gender,hdate)
         cursor.execute(sql,tuple)
         try:
             conn.commit()
             return render_template('addMember.html', msg='SAVED SUCCESSFULLY')
         except:
             conn.rollback()
             return render_template('addMember.html', msg='FAILED')
    else:

         return render_template('addMember.html')


@app.route('/deposit',methods=['GET','POST'])
def deposit():
    if request.method == 'POST':
        conn = psycopg2.connect(database="sunsetdb",
                                user="postgres",
                                password="drugnovmi5",
                                host="localhost",
                                port="5432")

        sql = "INSERT INTO deposittbl (member_no,amount,depdate)VALUES (%s,%s,%s)"
        # NB: the real values were not parsed

        member_no = request.form['member_no']
        amount=request.form['amount']
        depdate = request.form['depdate']

        # Create a cursor using the conn
        # The cursor will then execute the SQL query. Cursor, variable, is connected to SQL
        cursor = conn.cursor()
        tuple = (member_no,amount,depdate)
        cursor.execute(sql, tuple)
        try:
            conn.commit()
            return render_template('deposit.html', msg='SAVED SUCCESSFULLY')
        except:
            conn.rollback()
            return render_template('deposit.html', msg='FAILED')
    else:

        return render_template('deposit.html')


@app.route('/reports')
def reports():
    # when the route runs, return back to index.html
    return render_template('reports.html')


@app.route('/loans')
def loans():
    # when the route runs, return back to index.html
    return render_template('loans.html')


@app.route('/search', methods=['GET','POST'])
def search():
    if request.method=='POST':
         conn=psycopg2.connect(database="sunsetdb",
                              user="postgres",
                              password="drugnovmi5",
                              host="localhost",
                              port="5432")

         sql=("SELECT memberstbl.member_no,memberstbl.first_name,deposittbl.amount FROM memberstbl INNER JOIN deposittbl ON memberstbl.member_no=deposittbl.member_no WHERE memberstbl.member_no=%s")
         # NB: the real values were not parsed
         m_no = request.form['member_no']


         # Create a cursor using the conn
         # The cursor will then execute the SQL query. Cursor, variable, is connected to SQL
         cursor=conn.cursor()

         cursor.execute(sql,(m_no,))
         try:
             # conn.commit()
             if cursor.rowcount<1:
                 return render_template('search.html', msg='NOT FOUND')
             else:
                 result=cursor.fetchall()
                 return render_template('search.html', data=result)


         except:
             # conn.rollback()
             return render_template('search.html', msg='FAILED')
    else:

         return render_template('search.html')


@app.route('/pie')
def pie():
    mypie = pygal.Pie()
    mypie.title = "Member gender"
    conn = psycopg2.connect(database="sunsetdb",
                            user="postgres",
                            password="drugnovmi5",
                            host="localhost",
                            port="5432")
    cursor = conn.cursor()
    sql = "SELECT COUNT (gender), gender FROM memberstbl GROUP BY gender"
    cursor.execute(sql)
    list=[]
    results=cursor.fetchall()
    for row in results:
        list.append(row[0])
    print(list)
    mypie.add("Male",list[0])
    mypie.add("Female", list[1])

    return Response(response=mypie.render(), content_type="image/svg+xml")








if __name__ == '__main__':
    app.run(port=5050) # to change port
