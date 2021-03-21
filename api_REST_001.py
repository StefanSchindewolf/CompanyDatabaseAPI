import flask
from flask import request, jsonify, render_template
from werkzeug.http import HTTP_STATUS_CODES
import datetime
import sys
import sqlite3
import os
from CompanyModel import Company, CompanySchema
from setup import db


# Setup Flask Application
from setup import app, log



# Internal methods
def create_dict_from_row(cursor, row):
    d = dict()
    for id, col in enumerate(cursor.description):
        d[col[0]] = row[id]
    return d


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


### External methods
@app.route('/api/v1/company/all', methods=['GET'])
def show_company_all():

    # Initialize defaults
    all_default = 20
    log.info('Showing complete list of companies')
    
    # Retrieve data from database
    companies = Company.query.order_by(Company.c_id).all()
    company_schema = CompanySchema(many=True)
    
    return_dict = company_schema.dump(companies)
  
    log.info(return_dict)
    # Return as Json
    return jsonify(return_dict)


@app.route('/api/v1/company', methods=['GET'])
def show_company_by():
    """ Shows company data based on given company id (c_id) number.
    
        :return: json containing all data for this company
        """
    
    if 'c_id' in request.args:
        c_id = int(request.args['c_id'])
        log.info('Received GET request for ID {}'.format(c_id))
    else:
        return bad_request('Error: Company ID not specified')
    
    company = Company.query.filter(Company.c_id == c_id).one_or_none()
    
    if company is not None:
        company_schema = CompanySchema()
        log.info('Found company data for company ID {}'.format(c_id))
        return company_schema.dump(company)

    else:
        return bad_request('Could not find company using ID {}'.format(c_id))


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

app.run(debug=True)

