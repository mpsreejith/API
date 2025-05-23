import pyodbc
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/DB_API', methods=['GET', 'POST'])
def operation():
    user_data = request.get_json()
    action = user_data.get('operation')
    db = user_data.get('DB')
    table = user_data.get('table')  # optional: specify which table to select from

    if action is None or db is None:
        return jsonify({'status': 'error', 'message': 'DB and operation are required'})

    server = 'ELEVEN\\SQLEXPRESS'

    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={db};'
        f'Trusted_Connection=yes;'
    )

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        if action == 'select':
            if not table:
                return jsonify({'status': 'error', 'message': 'Table name is required for select operation'})

            cursor.execute(f'SELECT TOP 10 * FROM {table}')
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return jsonify({'status': 'success', 'data': rows})

        else:
            return jsonify({'status': 'error', 'message': f'Unsupported operation: {action}'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

    finally:
        try:
            conn.close()
        except:
            pass


if __name__ == '__main__':
    app.run(debug=True)
