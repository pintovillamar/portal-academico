from db.database import app


from db.database import test_connection

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/connection_test')
def connection_test():
    if test_connection() == 'Connection test failed!':
        return 'Connection test failed!'
    return 'Connection test successful!'

if __name__ == '__main__':
    app.run()