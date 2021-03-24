import flask
from flask import request, jsonify, render_template
from werkzeug.http import HTTP_STATUS_CODES
import datetime
from marshmallow import ValidationError, EXCLUDE, INCLUDE
from CompanyModel import Company, CompanySchema, Note, CompanyNoteSchema

# Setup Flask Application
from setup import app, log, db


# Internal methods
def create_dict_from_row(cursor, row):
    d = dict()
    for id, col in enumerate(cursor.description):
        d[col[0]] = row[id]
    return d


def validate(input_data, schema, required=None):
    """ Validates provided content against the schema setting "required"
        fields and accepting partial data on the others.

        Requires "input_data" as dictionary
        Requires "schema" as instance (should be created in calling function)

        Returns: Validated instance of schema or string with error message
    """

    try:
        # If only a subset of keys is required
        if required is not None:
            for key in required:
                check_key = input_data[key]
            # Then do a PARTIAL load into schema (missing fields allowed)
            # Maybe this works also: "partial=[~required]" (???)
            loaded = schema.load(input_data, partial=True)
        else:
            # Else do a STRICT load into schema (no missing fields)
            loaded = schema.load(input_data, partial=False)

        log.info('Content fits into schema: {}'.format(schema.dumps(loaded)))
        return loaded

    except ValidationError as e:
        msg = 'Failed to validate Json content at: {}'.format(e)
        log.warning(msg)
        raise Exception(msg)
    except KeyError as e:
        msg = 'Missing required field: {}'.format(e)
        log.warning(msg)
        raise Exception(msg)
    except Exception as e:
        msg = 'Other error in input data: {}'.format(e)
        log.warning(msg)
        raise Exception(msg)


def row_exists(input_data, search_object, search_columns):
    """ Check if a row exists in the db if searched by the search columns
        Matching is done against input data.
    
        Returns: True if exists and False if not
        """
    
    search_query = eval(search_object).query
    search_object = search_object.strip('()')
    
    # Check all required fields and setup a query
    try:
        for field in search_columns:
            search_query = search_query.filter(getattr(eval(search_object), field).like(input_data[field]))
        
        results = search_query.all()
    
        # If we got results, return them, else 
        if results != []:
            msg = 'Found entry for: {}'.format(results)
            log.info(msg)
            return results
        else:
            msg = 'No row found searching for: {}'.format(search_columns)
            log.info(msg)
            return None
    except Exception as e:
        log.warning('Could not search - unknown error {}'.format(e))
        return None


def error_response(status_code, message=None):
    """ Error handling routine which produces short descriptions
        for the provided HTTP error code.
        
        Returns: Response to client (the message and an HTTP error code)
        """
    payload = {'ERROR': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    return error_response(400, message)


### External methods ####

@app.route('/api/v1/company/show/all', methods=['GET'])
def show_company_all():

    # Initialize defaults
    all_default = 20
    log.info('Receiving Show All Request for all companies')
    
    # Retrieve data from database
    companies = Company.query.order_by(Company.c_id).all()
    company_schema = CompanySchema(many=True)
    
    return_dict = company_schema.dump(companies)
  
    log.info(return_dict)
    # Return as Json
    return jsonify(return_dict)


@app.route('/api/v1/company/show', methods=['GET'])
def show_company_by():
    """ Shows company data based on given company id (c_id) number.
        Works as a simple GET request.  
    
        :return: json containing all data for this company
        """
    
    if 'c_id' in request.args:
        c_id = int(request.args['c_id'])
        log.info('Receiving Show By Request for ID {}'.format(c_id))
    else:
        return bad_request('Error: Company ID not specified')
    
    company = Company.query.filter(Company.c_id == c_id).one_or_none()
    
    if company is not None:
        company_schema = CompanySchema()
        log.info('Found company data for company ID {}'.format(c_id))
        return company_schema.dump(company)

    else:
        return bad_request('Could not find company using ID {}'.format(c_id))


@app.route('/api/v1/company/add', methods=['POST'])
def add_company():
    """ Adds a company to the database including all provided fields.
        Company Name and legal entity are required (c_name, c_legent)
        A dublicity check is done on those fields.
        
        Not filled fields will be set to None, if not provided in the POST
        request.
        
        If the POST requests includes an ID (c_id), it is removed.
        
        :returns: Saved row as Json (as if requested by id) or error response
        """
    
    # Set required fields for adding a new company (or leave empty for all)
    required_fields = ['c_name', 'c_legent']
    
    # Read company data provided by JSON payload
    input_data = request.get_json(force=True) or None
    
    # Set schema to apply for adding new items
    add_schema = CompanySchema()
    
    
    # If we got input, then 
    if input_data is not None:
        log.info('Receiving Insert Request with data: {}'.format(input_data.values()))
        
        # Remove company ID if provided (server assigns ID)
        if 'c_id' in input_data.keys(): input_data.pop('c_id')
        
        # Check if we can load the input data as a company according to schema
        try:
            new_company = validate(input_data, add_schema, required_fields)
        except Exception as e:
            msg = 'Schema validation failed due to {}'.format(e)
            log.warning(msg)
            return bad_request(msg)
        
        # Does the company name with the provided legal entity exist?
        if row_exists(input_data, 'Company()', required_fields) is None:
            msg = 'Company not found by name and legal entity: {} {}'.format(input_data['c_name'], input_data['c_legent'])
            log.info(msg)
            # Add new company to Database
            try:
                db.session.add(new_company)
                db.session.commit()
                msg = 'Creating company with ID {}'.format(new_company.c_id)
                log.info(msg)
                return msg, 201
            except Exception as e:
                db.session.rollback()
                msg = 'Creating company failed with error: {}'.format(e)
                log.warning(msg)
                return bad_request(msg)
        else:
            msg = 'Company already exists, doing nothing: {}'.format(new_company)
            log.warning(msg)
            return bad_request(msg)
    else:
        msg = 'No input data provided'
        return bad_request(msg)


@app.route('/api/v1/company/update', methods=['POST'])
def update_company():
    """ Changes company data according to incoming JSON file.
        Company needs to be specified correctly by using the correct
        company ID.
        
        Note that all other provided fields will OVERWRITE the data in the
        database and kill existing records (handle with care).
        
        Returns: JSON with updated data
        """
        
    # To update a company we need the c_id to exist, all other fields may change
    required_fields = ['c_id',]

    # Get update data from JSON
    input_data = request.get_json(force=True) or None
    log.info('Receiving Update Request with data {}'.format(input_data.items()))

    # Switch to schema with/wo notes
    if 'notes' in input_data.keys():
        add_schema = CompanySchema(many=True)
    else:
        add_schema = CompanySchema()
        
    # Check if we can load the input data as a company according to schema
    try:
        new_company = validate(input_data, add_schema, required_fields)
    except Exception as e:
        msg = 'Schema validation failed due to {}'.format(e)
        log.warning(msg)
        return bad_request(msg)
        
    if row_exists(input_data, 'Company()', required_fields) is not None:
    # Does the company exist?
        try:
            # Then update and return new row
            db.session.add(new_company)
            db.session.commit()
            upped = row_exists(input_data, 'Company()', required_fields)
            upped = add_schema.dumps(upped, many=True)
            msg = 'Updating company with ID {}'.format(new_company.c_id)
            log.info(msg)
            return upped
        except Exception as e:
            # Else throw error
            db.session.rollback()
            msg = 'Updating company failed with error: {}'.format(e)
            log.warning(msg)
            return bad_request(msg)
    else:
        msg = 'Row not found with provided {}'.format(new_company.c_id)
        log.error(msg)
        return bad_request(msg)


@app.errorhandler(404)
def page_not_found(e):
    return '<h1>404</h1><p>No data found</p>', 404

app.run(debug=True)

