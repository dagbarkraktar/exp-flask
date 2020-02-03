from main import db

"""
`record_id` INT(11) NOT NULL AUTO_INCREMENT,
`record_num_thru_year` INT(11) NULL DEFAULT NULL,
`case_in_date` DATE NULL DEFAULT NULL,
`case_court_id` INT(11) NULL DEFAULT NULL,
`case_num` VARCHAR(64) NULL DEFAULT NULL,
`case_year` INT(11) NULL DEFAULT NULL,
`case_books_num` INT(11) NULL DEFAULT NULL,
`case_person` VARCHAR(255) NULL DEFAULT NULL,
`empl_id` INT(11) NULL DEFAULT NULL,
`comments` VARCHAR(255) NULL DEFAULT NULL,
"""
class ExpInCase(db.Model):
    
    __tablename__ = "exp_in_cases"

    record_id = db.Column(db.Integer, primary_key = True)
    record_num_thru_year = db.Column(db.Integer)
    case_in_date = db.Column(db.DateTime)
    case_court_id = db.Column(db.Integer, db.ForeignKey("rsud.id"))
    case_court = db.relationship("CourtModel", backref="exp_in_cases", lazy="joined")
    case_num = db.Column(db.String(64))
    case_year = db.Column(db.Integer)
    case_books_num = db.Column(db.Integer)
    case_person = db.Column(db.String(255))
    empl_id = db.Column(db.Integer, db.ForeignKey("employees.empl_id"))
    empl = db.relationship("EmplModel", backref="exp_in_cases", lazy="joined")
    comments = db.Column(db.String(255))
    sending_type = db.column(db.Integer)
    sending_comments = db.column(db.String(128))

    def __init__(self, record_num_thru_year, case_in_date, case_court_id,
                    case_num, case_year, case_books_num, case_person, empl_id, comments):
        self.record_num_thru_year = record_num_thru_year
        self.case_in_date = case_in_date
        self.case_court_id = case_court_id
        self.case_num = case_num
        self.case_year = case_year
        self.case_books_num = case_books_num
        self.case_person = case_person
        self.empl_id = empl_id
        self.comments = comments
    
    def __repr__(self):
        return f"Num: {self.record_num_thru_year} Year: {self.case_year}"

"""
`id` INT(11) NOT NULL AUTO_INCREMENT,
`court_name` VARCHAR(255) NULL DEFAULT NULL,
`post_addr_raw` VARCHAR(255) NULL DEFAULT NULL,
`locality` VARCHAR(64) NULL DEFAULT NULL,
`locality_type` INT(11) NULL DEFAULT NULL,
`type` INT(11) NULL DEFAULT NULL,
`glas_status` INT(11) NULL DEFAULT NULL,
`launch_date` DATE NULL DEFAULT NULL,
`email` VARCHAR(128) NULL DEFAULT NULL,
`website` VARCHAR(128) NULL DEFAULT NULL,
"""
class CourtModel(db.Model):

    __tablename__ = "rsud"

    id = db.Column(db.Integer, primary_key = True)
    court_name = db.Column(db.String(255))
    post_addr_raw = db.Column(db.String(255))
    locality = db.Column(db.String(64))
    locality_type = db.Column(db.Integer)
    type = db.Column(db.Integer)
    glas_status = db.Column(db.Integer)
    launch_date = db.Column(db.DateTime)
    email = db.Column(db.String(128))
    website = db.Column(db.String(128))

    def __init__(self, court_name, locality):
        self.court_name = court_name
        self.locality = locality

    def __repr__(self):
        return f"{self.court_name}"

"""
`empl_id` INT(11) NOT NULL AUTO_INCREMENT,
`fio` VARCHAR(64) NULL DEFAULT NULL,
`comments` VARCHAR(128) NULL DEFAULT NULL,
`status` INT(11) NULL DEFAULT '1',
"""
class EmplModel(db.Model):

    __tablename__ = "employees"

    empl_id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(64))
    comments = db.Column(db.String(128))
    status = db.Column(db.Integer)

    def __init__(self, fio, comments, status):
        self.fio = fio
        self.comments = comments
        self.status = status

    def __repr__(self):
        return f"{self.fio}"
