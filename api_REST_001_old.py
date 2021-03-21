import flask
from flask import request, jsonify
from werkzeug.http import HTTP_STATUS_CODES
import logging
import datetime
import sys
import sqlite3
import os


# Setup Flask Application
app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s \t %(message)s ',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout,
)
log = logging.getLogger('log')

# Internal methods
def create_dict_from_row(cursor, row):
    d = dict()
    for id, col in enumerate(cursor.description):
        d[col[0]] = row[id]
    return d


# Create SQLite database
def create_db_connection(file):
    """ Create a database connection to the specified SQLite file
        and return connection handler (print error if not)
    """
    conn = None
    try:
        conn = sqlite3.connect(file)
        print('Connected to ', sqlite3.version)
        return conn
    except Error as e:
        print(e)


def insert_company(c_id, data, conn):
    for item in data:
        conn.execute('insert into companies values ({})'.format(item.values()))


def update_company(c_id, data):
    """ Updates company data from provided dictionary.
    
        Returns: Updated company row
        """
    
    conn = create_db_connection(sqlite_file)
    company = conn.execute(select_stm.format('companies', c_id)) or None
    if company is not None:
        for key, value in company.iterrows:
            conn.execute(update_row.format(key, value))
            msg = 'Updating company ID {} field {} with new data {}'.format('companies', c_id, key, value)
            log.info(msg)
        return company
    else:
        msg = 'Company not found with c_id: {}'.format(c_id)
        log.error(msg)
        return bad_request(msg)
    


def add_new_tag(c_id, tag, entry, list):
    """ Checks if a tag set by API customer is existing and
        if not, creates the tag.

        Returns:    (New | Existing) tag and value as dict
                    None if no entry was found
        """
    
    company = ''
    if 'c_id' in request.args:
        try:
            c_id = int(request.args['c_id'])
            company = c_list[c_id]
        except Error as e:
            msg = 'Company not found with ID: {}'.format(c_id)
            log.info(msg)
            return bad_request(msg)
    else:
        return 'Error: ÍD not specified'

    if company != '':
        if request.args['tag'] in company.keys():
            entry = company[tag]
            msg = 'Field {} already exists with value {}'.format(entry)
            log.info(msg)
            return bad_request(msg)
        else:
            c_list[tag] = entry
            result_dict = c_list[c_id]
            msg = 'New field {} with value {} created successfully'.format(tag, entry)
            log.info(msg)
            return error_response(200, msg)
    else:
        msg = 'Company not found with key {}'.format(c_id)
        return msg


def error_response(status_code, message=None):
    """ Error handling routine which produces short descriptions
        for the provided HTTP error code.
        
        Returns: Response to client
        """
    payload = {'ERROR': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    return error_response(400, message)


# External methods
@app.route('/api/v1/company/all', methods=['GET'])
def show_company_all():

    # Initialize defaults
    all_default = 20

    # Retrieve data from database
    conn = sqlite3.connect(sqlite_file)
    conn.row_factory = create_dict_from_row
    cur = conn.cursor()
    try:
        query = 'select * from companies limit {}'.format(all_default)
        return_dict = cur.execute(query).fetchall()
    except Exception as e:
        return bad_request(e)

    # If it fails, the return test dataset
    if return_dict is not None:
        log.info('Showing complete list of companies')
        return jsonify(return_dict)
    else:
        log.error('No data found')
        return jsonify(return_dict)


@app.route('/api/v1/company', methods=['GET'])
def show_company_by():
    if 'c_id' in request.args:
        c_id = int(request.args['c_id'])
    else:
        return bad_request('Error: Company ID not specified')

    return_dict = []
    for company in c_list:
        if company['c_id'] == c_id:
            return_dict.append(company)
            log.info('Show Company by ID with ID {}'.format(c_id))
    if len(return_dict) == 0:
        msg = 'No company found with ID {}'.format(c_id)
        log.error(msg)
        return bad_request(msg)
    return jsonify(return_dict)


@app.route('/api/v1/company', methods=['POST'])
def change_company():
    """ Changes company data according to incoming JSON file.
        Company needs to be verified correctly by specifying
        the company ID.
        
        Returns: JSON with updated data
        """

    client = 'external'
    # Check if c_id is int
    if 'c_id' in request.args:
        try:
            c_id = int(request.args['c_id'])
            log.info('Receiving Update Company Request from {} with ID {}'.format(client, c_id))
        except Exception as e:
            c_id = request.args['c_id']
            msg = 'Cannot perform update due to invalid ID type {}'.format(type(c_id))
            log.error(msg)
            return bad_request(msg)
    else:
        return bad_request('Error: Company ID missing')
    
    # Get company update from JSON
    company = request.get_json(force=True) or None
    log.info('Processing update to ID {} with data {}'.format(c_id, company))
    if company is not None:
        upped = update_company(c_id, company)
        log.info('Updated company ID {} with item {}'.format(c_id, item))
        return jsonify(upped)
    else:
        msg = 'No data provided for update'
        log.error(msg)
        return bad_request(msg)


@app.errorhandler(404)
def page_not_found(e):
    return '<h1>404</h1><p>No data found</p>', 404



app.run()
