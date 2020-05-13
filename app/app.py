from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'treesData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Tree Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblTreeImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, trees=result)


@app.route('/view/<int:tree_id>', methods=['GET'])
def record_view(tree_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblTreeImport WHERE id=%s', tree_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', tree=result[0])


@app.route('/edit/<int:tree_id>', methods=['GET'])
def form_edit_get(tree_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblTreeImport WHERE id=%s', tree_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', tree=result[0])


@app.route('/edit/<int:tree_id>', methods=['POST'])
def form_update_post(tree_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Girth_in'), request.form.get('Height_ft'), request.form.get('Volume_ft3'),
                  tree_id)
    sql_update_query = """UPDATE tblTreeImport t SET t.Girth_in = %s, t.Height_ft = %s, t.Volume_ft3 = %s, WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/trees/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New tree Form')


@app.route('/trees/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Girth_in'), request.form.get('Height_ft'), request.form.get('Volume_ft3'))
    sql_insert_query = """INSERT INTO tblTreeImport (Girth_in,Height_ft,Volume_ft3) VALUES (%s,%s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:tree_id>', methods=['POST'])
def form_delete_post(tree_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblTreeImport WHERE id = %s """
    cursor.execute(sql_delete_query, tree_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/trees', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblTreeImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/trees/<int:tree_id>', methods=['GET'])
def api_retrieve(tree_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblTreeImport WHERE id=%s', tree_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/trees', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    inputData = (content['Girth_in'], content['Height_ft'], content['Volume_ft3'])
    sql_insert_query = """INSERT INTO tblTreeImport (Girth_in,Height_ft,Volume_ft3) VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/trees/<int:tree_id>', methods=['PUT'])
def api_edit(tree_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Girth_in'], content['Height_ft'], content['Volume_ft3'], tree_id)
    sql_update_query = """UPDATE tblTreeImport t SET t.Girth_in = %s, t.Height_ft = %s, t.Volume_ft3 = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/trees/<int:tree_id>', methods=['DELETE'])
def api_delete(tree_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblTreeImport WHERE id = %s """
    cursor.execute(sql_delete_query, tree_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
