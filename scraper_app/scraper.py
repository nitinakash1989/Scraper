from flask import Flask, render_template, url_for, flash, redirect, Response,make_response
from forms import ScrapyForm

from core import *
app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


@app.route("/",  methods=['GET', 'POST'])
@app.route("/home",  methods=['GET', 'POST'])
def home():
    """
    This function is router for home page. 
    """
    url = "http://calistings.cushmanwakefield.com/desktop.aspx"
    sf = ScrapyForm()
    
    if sf.validate_on_submit():
        
        
        prop_df = get_data_from_server(url)
        resp = make_response(prop_df.to_csv(index=False))
        
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        total_rec = len(prop_df)
        if total_rec>0:
            flash(f'{total_rec} records downloaded', 'success')
        else:
            flash(f'Something goes wrong', 'dangour')
    
        return resp
    return render_template('home.html', form = sf)


if __name__ == '__main__':
    app.run(debug=True)