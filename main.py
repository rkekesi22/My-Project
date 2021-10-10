import datetime

from website import create_app

def write_date_text():
    with open('date.txt', mode='w') as f:
        year = datetime.date.today().year
        month = datetime.date.today().month
        f.write(str(year) + "/" + str(month))
        f.close()

app = create_app()

# Entry Point
if __name__ == '__main__':
    write_date_text()
    app.run(debug=True)
