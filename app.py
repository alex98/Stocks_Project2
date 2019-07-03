import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# The database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://vibrato3:masterp99@localhost/project'

db = SQLAlchemy(app)


# Create our database model
class Stock(db.Model):
    __tablename__ = 't_all_stocks_5year'

    stock_date = db.Column(db.String)
    stock_open = db.Column(db.Float)
    stock_low = db.Column(db.Float)
    stock_close = db.Column(db.Float)
    stock_volume = db.Column(db.Integer)
    stock_name = db.Column(db.String)
    stock_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Stock %r>' % (self.stock_name)



@app.route("/")
def home():
   
    return render_template("index.html")

@app.route('/stocks/<stock_name>')
def stocks(stock_name):
    """Render Home Page."""
    results = db.session.query(Stock.stock_date, Stock.stock_open, Stock.stock_low, Stock.stock_close,Stock.stock_volume, Stock.stock_name).\
        filter(Stock.stock_name == stock_name).\
        order_by(Stock.stock_name).\
        all()
    return jsonify(results)


@app.route("/emoji_char")
def emoji_char_data():
    """Return emoji score and emoji char"""

    # Query for the top 10 emoji data
    results = db.session.query(Emoji.emoji_char, Emoji.score).\
        order_by(Emoji.score.desc()).\
        limit(10).all()

    # Create lists from the query results
    emoji_char = [result[0] for result in results]
    scores = [int(result[1]) for result in results]

    # Generate the plot trace
    trace = {
        "x": emoji_char,
        "y": scores,
        "type": "bar"
    }
    return jsonify(trace)


@app.route("/emoji_id")
def emoji_id_data():
    """Return emoji score and emoji id"""

    # Query for the emoji data using pandas
    query_statement = db.session.query(Emoji).\
        order_by(Emoji.score.desc()).\
        limit(10).statement
    df = pd.read_sql_query(query_statement, db.session.bind)

    # Format the data for Plotly
    trace = {
        "x": df["emoji_id"].values.tolist(),
        "y": df["score"].values.tolist(),
        "type": "bar"
    }
    return jsonify(trace)


@app.route("/emoji_name")
def emoji_name_data():
    """Return emoji score and emoji name"""

    # Query for the top 10 emoji data
    results = db.session.query(Emoji.name, Emoji.score).\
        order_by(Emoji.score.desc()).\
        limit(10).all()
    df = pd.DataFrame(results, columns=['name', 'score'])

    # Format the data for Plotly
    plot_trace = {
        "x": df["name"].values.tolist(),
        "y": df["score"].values.tolist(),
        "type": "bar"
    }
    return jsonify(plot_trace)


if __name__ == '__main__':
    app.run(debug=True)
