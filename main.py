import helper
from flask import Flask, request, Response
import json
from flask_restful import Resource, Api
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs

app = Flask(__name__)  # Flask app instance initiated
api = Api(app)  # Flask restful wraps Flask app around it.
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Note Taking Application',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='3.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)


class ResponseSchema(Schema):
    title = fields.String(required=True)
    desc = fields.String(required=True)


class RequestSchema(Schema):
    title = fields.String(required=True)
    desc = fields.String(required=True)


class addNote(MethodResource, Resource):
    @doc(description='Add notes', tags=['Awesome'])
    @use_kwargs(RequestSchema, location=('json'))
    @marshal_with(ResponseSchema)  # marshalling
    def post(self, title, desc):
        # Get item from the POST body
        print("hello")
        req_data = request.get_json()
        title = req_data['title']
        desc = req_data['desc']
        print(title)
        # Add item to the list
        res_data = helper.add_to_notes(title, desc)

        # Return error if item not added
        if res_data is None:
            response = Response("{'error': 'Notes not added - '}" +
                                title, status=400, mimetype='application/json')
            return response
        # Return response
        response = Response(json.dumps(res_data), mimetype='application/json')
        return response


api.add_resource(addNote, '/notes/new')
docs.register(addNote)


class getNotes(MethodResource, Resource):
    @doc(description='Get all notes', tags=['Awesome'])
    @marshal_with(ResponseSchema)  # marshalling
    def get(self):
        # Get items from the helper
        res_data = helper.get_all_notes()
        # Return response
        response = Response(json.dumps(res_data), mimetype='application/json')
        return response


api.add_resource(getNotes, '/notes/all')
docs.register(getNotes)


class deleteNote(MethodResource, Resource):
    @doc(description='Delete notes', tags=['Awesome'])
    @use_kwargs(RequestSchema, location=('json'))
    @marshal_with(ResponseSchema)  # marshalling
    def delete(self):
        # Get item from the POST body
        req_data = request.get_json()
        title = req_data['title']
        # Delete item from the list
        res_data = helper.delete_item(title)
        if res_data is None:
            response = Response("{'error': Error deleting item - " +
                                title + "}", status=400, mimetype='application/json')
            return response
        # Return response
        response = Response(json.dumps(res_data), mimetype='application/json')
        return response


api.add_resource(deleteNote, '/notes/remove')
docs.register(deleteNote)


class updateNote(MethodResource, Resource):
    @doc(description='Update note', tags=['Awesome'])
    @use_kwargs(RequestSchema, location=('json'))
    @marshal_with(ResponseSchema)  # marshalling
    def put(self):
        # Get item from the POST body
        req_data = request.get_json()
        title = req_data['title']
        desc = req_data['desc']
        # Delete item from the list
        res_data = helper.update_note(title, desc)
        if res_data is None:
            response = Response("{'error': Error updating item - " +
                                title + "}", status=400, mimetype='application/json')
            return response
        # Return response
        response = Response(json.dumps(res_data), mimetype='application/json')
        return response


api.add_resource(updateNote, '/notes/update')
docs.register(updateNote)


if __name__ == "__main__":
    app.run(debug=True)
