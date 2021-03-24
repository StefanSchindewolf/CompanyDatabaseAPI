import os
from setup import db
from datetime import datetime
from CompanyModel import Company, Note

# Data to initialize database with
db_start_data = [\
        {'c_id': 1, 'c_name': 'Oerlikon', 'c_legent': 'AG', 'c_employed': 30000, 'c_shacap': 800000, 'c_other': None, 'c_cdate': '2018-08-08 21:16:01.888444', \
        "notes": [("I am first", ""), \
                    ("And I am second", ""),]}, \
        {'c_id': 2, 'c_name': 'Credit Suisse Schweiz', 'c_legent': 'AG', 'c_employed': 55000, 'c_shacap': 750000, 'c_other': 'None', 'c_cdate': '2019-10-08 21:16:01.888444', \
        "notes": [("I am first", ""), \
                    ("And I am second", ""),]}, \
        {'c_id': 3, 'c_name': 'Signum Wangen', 'c_legent': 'GmbH', 'c_employed': 2899, 'c_shacap': 20000, 'c_other': 'Additional information', 'c_cdate': '2018-11-08 21:16:01.888444', \
        "notes": [("I am first", ""), \
                    ("And I am second", ""),]}, \
        {'c_id': 4, 'c_name': 'Perlakon', 'c_legent': 'OHG', 'c_employed': 278, 'c_shacap': 6000, 'c_other': 'Any other business', 'c_cdate': '2018-09-08 21:16:01.888444', \
        "notes": [("I am first", ""), \
                    ("And I am second", ""),]}, \
        {'c_id': 5, 'c_name': 'Rüblibein', 'c_legent': 'GmbH', 'c_employed': 234, 'c_shacap': 8000, 'c_other': 'Any other business', 'c_cdate': '2019-09-08 21:17:01.888444', \
        "notes": [("I am first", ""), \
                    ("And I am second", ""),]}, \
        {'c_id': 6, 'c_name': 'Werzilae Maschinen', 'c_legent': 'GmbH', 'c_employed': 1200, 'c_shacap': 23000, 'c_other': 'Any other business', 'c_cdate': '2019-09-08 21:16:01.888444', \
        "notes": [("I am first", ""), \
                    ("And I am second", ""),]},
        {'c_id': 7, 'c_name': 'Hengebrecht', 'c_legent': 'OHG', 'c_employed': 1700, 'c_shacap': 6000, 'c_other': 'Any other business', 'c_cdate': '2019-09-08 21:16:01.888444', \
        "notes": [("I am first", ""), \
                    ("And I am second", ""),]}
        ]

def create_new_db(db_file, db_content):
    """ This function creates a new SQLite3 file and loads provided
        db content into that database.

        :returns: Nothing
        """

    print('Test data to be imported: ', db_start_data)

    # Delete database file if it exists currently
    if os.path.exists(db_file):
        os.remove(db_file)
        print('Removed db file ', db_file)

    # Create the database
    db.create_all()

    # Iterate over start data dictionary and add content to db
    for company in db_content:
        c = Company(c_id=company['c_id'], c_name=company['c_name'], \
        c_legent=company['c_legent'], c_shacap=company['c_shacap'], \
        c_other=company['c_other'])
        for note in company.get('notes'):
            text, ts = note
            c.notes.append(Note(content=text))
        db.session.add(c)

    print('Imported test data rows into db ', db_file)
    db.session.commit()

def main():
    print('Resetting database program')
    create_new_db('company.db', db_start_data)

if __name__ == "__main__":
    main()


