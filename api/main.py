from bson import ObjectId, errors
from datetime import datetime
from decouple import AutoConfig
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask, jsonify, request, make_response
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from marshmallow.exceptions import ValidationError
from schemas import (
    CreateFormSchema,
    CreateFormSubmissionSchema,
    FormSchema,
    FormSubmissionSchema,
    FormSubmissionsSchema,
    FormTimeSeriesSchema,
    UpdateFormSchema,
    APIErrorSchema,
)
from validators import FormValidator


## App Configs
config = AutoConfig()

app = Flask(__name__)

app.config["MONGO_URI"] = config("MONGO_DB_URI")
app.config["APISPEC_SPEC"] = APISpec(
    title="FormPlus API",
    version="v1.0",
    plugins=[MarshmallowPlugin()],
    openapi_version="2.0.0",
)
app.config["APISPEC_SWAGGER_URL"] = "/swagger/"
app.config["APISPEC_SWAGGER_UI_URL"] = "/swagger/ui/"
api = Api(app)
mongo = PyMongo(app)
docs = FlaskApiSpec(app)

db = mongo.db


## Views

@app.route("/")
def base():
    return "Form API v1.0"


class ListCreateFormResource(MethodResource, Resource):
    """
    Create and Retrieve Forms.
    """
    init_every_request = False

    @marshal_with(FormSchema(many=True), description="Retrieve all forms.", code=200)
    def get(self):
        forms = db.forms.find()
        return FormSchema().load(forms, many=True)

    @use_kwargs(CreateFormSchema)
    @marshal_with(FormSchema, description="Create a new form.", code=201)
    def post(self, **kwargs):
        data = { 'created_at': datetime.now().astimezone(), **kwargs }
        data = CreateFormSchema().dump(data)
        form = db.forms.insert_one(data)
        form = db.forms.find_one({"_id": form.inserted_id})
        return FormSchema().load(form), 201
        

class RetrieveUpdateFormResource(MethodResource, Resource):
    """
    Retrieve and Update Forms.
    """
    init_every_request = False

    @marshal_with(FormSchema, description="Retrieve a form by its id", code=200)
    @marshal_with(APIErrorSchema, code=400)
    def get(self, id: str):
        try:
            form = db.forms.find_one({"_id": ObjectId(id)})
        except errors.BSONError:
            return {"message": "Id is not valid."}, 400

        if not form:
            return {"message": "object does not exist"}, 404

        return FormSchema().load(form)

    @use_kwargs(UpdateFormSchema)
    @marshal_with(FormSchema, description="Update a form by its id", code=200)
    @marshal_with(APIErrorSchema, code=400)
    def put(self, id: str, **kwargs):
        try:
            form = db.forms.update_one(
                {"_id": ObjectId(id)}, {"$set": FormSchema().dump(kwargs)}, upsert=True
            )
        except errors.BSONError as e:
            return {"message": "Id is not valid."}, 400

        form = db.forms.find_one({"_id": ObjectId(id)})
        return FormSchema().load(form)


class SubmitFormResource(MethodResource, Resource):
    """
    Create Form Submissions.
    """
    init_every_request = False

    @use_kwargs(CreateFormSubmissionSchema)
    @marshal_with(FormSubmissionSchema, description="Submit a form.", code=201)
    @marshal_with(APIErrorSchema, code=400)
    def post(self, id: str, **kwargs):
        try:
            form = db.forms.find_one({"_id": ObjectId(id)})
        except errors.BSONError:
            return {"message": "Id is not valid."}, 400

        if not form:
            return {"message": "Object does not exist."}, 404
       
        if not form["is_open"]:
            return {"message": "Form is not open to submissions."}, 400

        submissions_count = db.submissions.count_documents({"form_id": id})
        
        if submissions_count >= form["quota"]:
            return {"message": "Form quota exceeded."}, 400



        data = {"form_id": id, 'created_at': datetime.now().astimezone(), **kwargs}
        validator = FormValidator(form)

        try:
            validator.validate_submission(data)
        except ValidationError as err:
            return make_response(jsonify({"errors": err.messages}), 400)
        
        submission = db.submissions.insert_one(data)
        submission = db.submissions.find_one({"_id": submission.inserted_id}) 
        return submission, 201
       

class FormSubmissionsResource(MethodResource, Resource):
    """ Retrieve Form Submissions by Form ID """
    init_every_request = False

    @marshal_with(
        FormSubmissionsSchema, description="Retrieve form submissions", code=201
    )
    @marshal_with(APIErrorSchema, code=400)
    def get(self, id: str, **kwargs):
        form_submissions = db.submissions.find({"form_id": id})
        submissions_count = db.submissions.count_documents({"form_id": id})
        return {"count": submissions_count, "submissions": form_submissions}


class FormAnalyticsResource(MethodResource, Resource):
    """ Retrieve Form timeseries data by Form ID."""

    @marshal_with(
        FormTimeSeriesSchema(many=True), description="Retrieve form submission analytics", code=200
    )
    @marshal_with(APIErrorSchema, code=400)
    def get(self, id: str, **kwargs):
        pipeline = [
            {"$match": {"form_id": id}},
            {"$project": {"date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}}}},
            {"$group": {"_id": "$date", "total_responses": {"$count": {}}}}
        ]
        
        timeseries = db.submissions.aggregate(pipeline)
        data = FormTimeSeriesSchema().load(list(timeseries), many=True)
       
        return data


## Error handlers
@app.errorhandler(422)
@app.errorhandler(400)
def handle_error(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code


## Endpoints
api.add_resource(ListCreateFormResource, "/forms")
api.add_resource(RetrieveUpdateFormResource, "/forms/<string:id>")
api.add_resource(SubmitFormResource, "/forms/<string:id>/submit")
api.add_resource(FormSubmissionsResource, "/forms/<string:id>/submissions")
api.add_resource(FormAnalyticsResource, "/forms/<string:id>/analytics")

docs.register(ListCreateFormResource)
docs.register(RetrieveUpdateFormResource)
docs.register(SubmitFormResource)
docs.register(FormSubmissionsResource)
docs.register(FormAnalyticsResource)
