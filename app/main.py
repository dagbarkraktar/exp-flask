from flask import Flask, render_template, redirect, url_for, request, Response, json, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import os

import utils
from config import Config
import models


app = Flask(__name__)

# Get creds from env
MYSQL_EXP_USER = os.environ.get("MYSQL_EXP_USER") or "MYSQL_USER"
MYSQL_EXP_PASS = os.environ.get("MYSQL_EXP_PASS") or "MYSQL_PASS"
MYSQL_EXP_HOST = os.environ.get("MYSQL_EXP_HOST") or "192.168.10.210"

# TODO: Move mysql creds to config
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{MYSQL_EXP_USER}:{MYSQL_EXP_PASS}@{MYSQL_EXP_HOST}/expeddb"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_RECYCLE"] = 300
app.config["SQLALCHEMY_MAX_OVERFLOW"] = 30

db = SQLAlchemy(app)

# beginning of current year YYYY-MM-DD
first_january = f"{Config.CURRENT_YEAR}-01-01"
year_last_day = f"{Config.CURRENT_YEAR}-12-31"

# root
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    print(f"Client addr:{request.remote_addr}")

    #  get last number in case journal
    last_num = get_last_number()

    # get current page number (form GET request)
    cur_page = request.args.get('page', 1, type=int)

    # SELECT ... WHERE case_in_date > YYYY-01-01
    case_list = db.session.query(models.ExpInCase) \
                .filter(models.ExpInCase.case_in_date > first_january) \
                .filter(models.ExpInCase.case_in_date < year_last_day) \
                .order_by(models.ExpInCase.record_id.desc()) \
                .paginate(page=cur_page, per_page=Config.ROWS_PER_PAGE, error_out=False)

    return render_template("index.html", current_year=Config.CURRENT_YEAR, case_list=case_list, last_num=last_num)


# record_edit_form
@app.route("/record_edit_form", methods=['GET', 'POST'])
def record_edit_form():

    # get record_id (form GET request)
    rec_id = request.args.get('record_id', 0, type=int)
    ret_page_num = request.args.get('ret_page', 1, type=int)

    # SELECT ... WHERE RECORD_ID=REC_ID
    case = db.session.query(models.ExpInCase).get(rec_id)

    # check: is there a given rec_id in DB
    if case is None:
        return redirect(url_for("index"))
    else:
        return render_template("record_edit_form.html", case=case, ret_page_num=ret_page_num)


# court list for form select (id=court_name)
@app.route("/courts", methods=['GET', 'POST'])
def courts():

    # GET request
    if request.method == "GET":
        court_list = []

        # SELECT * ...
        response = db.session.query(models.CourtModel).all()
        for court in response:
            court_list.append({"id":court.id, "name":f"{court.court_name} ({court.locality})"})

        return json.dumps(court_list)
    
    # POST request
    if request.method == "POST":

        form_data = request.form.to_dict()

        company_name = form_data["company_name"]
        company_locality = form_data["company_locality"]

        # Create
        company_record = models.CourtModel(court_name=company_name, locality=company_locality)

        # Add record to db
        db.session.add(company_record)
        db.session.commit()

        print(f"COMPANY_ID: {company_record.id}")
        
        return str(company_record.id)


# employee list for form select (id=empl_name)
@app.route("/employee", methods=['GET', 'POST'])
def employee_list():

    # GET request
    if request.method == "GET":

        empl_list = []
        # SELECT ... WHERE STATUS = 1
        response = db.session.query(models.EmplModel).filter(models.EmplModel.status==1)
        for empl in response:
            empl_list.append({"id":empl.empl_id, "name":empl.fio})

        return json.dumps(empl_list)

    # POST request
    if request.method == "POST":

        form_data = request.form.to_dict()
        empl_fio = form_data["empl_fio"]
        empl_comment = form_data["empl_comment"]

        # Create
        empl_record = models.EmplModel(fio=empl_fio, comments=empl_comment, status=1)

        # Add record to db
        db.session.add(empl_record)
        db.session.commit()

        print(f"EMPL_ID: {empl_record.empl_id}")
        
        return str(empl_record.empl_id)


@app.route("/case_update", methods=['POST',])
def case_update():

    ret_page_num = 1

    if request.method == "POST":

        form_data = request.form.to_dict()

        # page number in pagination
        ret_page_num = form_data['ret_page_num']

        # Get record from DB
        record_id = form_data['record_id']
        case_record = db.session.query(models.ExpInCase).get(record_id)

        # set fields values
        case_record.record_num_thru_year = form_data['record_num']
        # convert dd.mm.yyyy to yyy-mm-dd
        case_record.case_in_date = utils.dmy_to_iso_date(form_data['case_in_date'])
        case_record.case_court_id = form_data['court_name']
        case_record.case_num = form_data['case_num']
        case_record.case_year = form_data['case_year']
        case_record.case_books_num = form_data['case_book_num']
        case_record.case_person = form_data['case_person']
        case_record.empl_id = form_data['empl_name']
        case_record.comments = form_data['comments']

        # Update record
        db.session.add(case_record)
        db.session.commit()

    # redirect back to page in case list
    return redirect(url_for("index", page=ret_page_num))

@app.route("/case_add", methods=['POST',])
def case_add():

    if request.method == "POST":

        # Retrieve form data
        form_data = request.form.to_dict()

        # Set fields values
        # record_num_thru_year = form_data['record_num']
        # get last number in case journal
        record_num_thru_year = get_last_number() + 1
        # сonvert dd.mm.yyyy to yyy-mm-dd
        case_in_date = utils.dmy_to_iso_date(form_data['case_in_date'])
        case_court_id = form_data['court_name']
        case_num = form_data['case_num']
        case_year = form_data['case_year']
        case_books_num = form_data['case_book_num']
        case_person = form_data['case_person']
        empl_id = form_data['empl_name']
        comments = form_data['comments']

        # Create
        case_record = models.ExpInCase(record_num_thru_year=record_num_thru_year, case_in_date=case_in_date, \
            case_court_id=case_court_id, case_num=case_num, case_year=case_year, case_books_num=case_books_num, \
            case_person=case_person, empl_id=empl_id, comments=comments)

        # Add record to db
        db.session.add(case_record)
        db.session.commit()

    # redirect back to page in case list
    return redirect(url_for("index"))


@app.route("/print_form", methods=['POST',])
def print_form():
    
    if request.method == "POST":

        # Retrieve form data
        # (checkbox array with id)
        row_checked = request.form.getlist("row_checked")

        filter_list = []
        for row_id in row_checked:
            filter_list.append((models.ExpInCase.record_id==row_id))

        print_form_list = db.session.query(models.ExpInCase).filter(or_(*filter_list)).all()

        print(f"PF List: {print_form_list}")

        # render print form template
        return render_template("print_form.html", pf_list=print_form_list)


def get_last_number():
    """
    Helper function.
    Return: value of last record_num_thru_year
    """
    last_rec = db.session.query(models.ExpInCase) \
        .filter(models.ExpInCase.case_in_date > first_january) \
        .order_by(models.ExpInCase.record_num_thru_year.desc()).first()

    return last_rec.record_num_thru_year


if __name__ == "__main__":
    app.run()
