from flask import Flask, jsonify, request
from datastore import Query

app = Flask(__name__)

@app.route("/")
def help_message():
    return """Welcome to the organizations API!

Try our /organizations endpoint.

You can filter the results:

/organizations?city=Washington&category=Greek

Available filters: id, city, state, postal, category

You can also provide an "orderBy" parameter
with an optional "direction" parameter (ASC or DSC):

/organizations?city=Washington&orderBy=postal&direction=DSC

"""

@app.route("/organizations")
def get_organizations():
    # Gather filter and order information from query
    filters = {}
    for key in ('id', 'name', 'city', 'state', 'postal', 'category'):
        value = request.args.get(key)
        if value:
            filters[key] = value

    isAscending = not (request.args.get('direction') == 'DSC')

    cursor = Query(filters=filters, orderBy=request.args.get('orderBy'), isAscending=isAscending).cursor()

    results = []
    schema = cursor.description
    for row in cursor:
        entry = {}
        for (idx, desc) in enumerate(schema):
            entry[desc[0]] = row[idx]
        results.append(entry)

    return jsonify({ 'organizations': results })


