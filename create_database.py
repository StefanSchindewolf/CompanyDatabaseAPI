import os
from setup import db
from CompanyModel import Company

def create_new_db(db_file):
    # Data to initialize database with
    db_start_data = [\
        {'c_id': 1, 'c_name': 'BMW AG', 'c_legent': 'AG', 'c_employed': 30000, 'c_shacap': 800000, 'c_other': None, 'c_cdate': '2018-08-08 21:16:01.888444'}, \
        {'c_id': 2, 'c_name': 'Brechtle', 'c_legent': 'AG', 'c_employed': 55000, 'c_shacap': 750000, 'c_other': 'None', 'c_cdate': '2018-10-08 21:16:01.888444'}, \
        {'c_id': 3, 'c_name': 'Signum Wangen GmbH', 'c_legent': 'GmbH', 'c_employed': 2899, 'c_shacap': 20000, 'c_other': 'None', 'c_cdate': '2018-11-08 21:16:01.888444'}, \
        {'c_id': 4, 'c_name': 'Perlakon OHG', 'c_legent': 'OHG', 'c_employed': 278, 'c_shacap': 6000, 'c_other': 'None', 'c_cdate': '2018-09-08 21:16:01.888444'}\
        ]
    print('Test data to be imported: ', db_start_data)

    # Delete database file if it exists currently
    if os.path.exists(db_file):
        os.remove(db_file)
        print('Removed db file ', db_file)

    # Create the database
    db.create_all()

    # Iterate over start data dictionary and add content to db
    for company in db_start_data:
            c = Company(c_id=company['c_id'], c_name=company['c_name'], \
            c_legent=company['c_legent'],c_shacap=company['c_shacap'], \
            c_other=None)
            db.session.add(c)

    print('Imported test data rows into db ', db_file)
    db.session.commit()

def main():
    print('Resetting database program')
    create_new_db('company.db')

if __name__ == "__main__":
    main()


