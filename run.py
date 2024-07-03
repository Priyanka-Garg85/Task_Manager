from app import create_app,db
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5004)
    with app.app_context():
        db.create_all()
