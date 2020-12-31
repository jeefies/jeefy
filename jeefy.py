from app import create_app

app = create_app('default')

if __name__ == '__main__':
        try:
            app.run('0.0.0.0', 80)
        except:
            app.run('0.0.0.0')
