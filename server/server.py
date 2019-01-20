#!/usr/bin/python

#pip install flask flask-jsonpify flask-sqlalchemy flask-restful flask-cache
import traceback
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
#from flask.ext.jsonpify import jsonify
from flask_cors import CORS
from flask.json import jsonify
from flask_restful import Resource, Api

db_connect = create_engine('sqlite:///lumberjack.db')
app = Flask(__name__)
CORS(app)
api = Api(app)


class Agents(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from main.agents;")  # This line performs query and returns json result
        return {'agents': [i[0] for i in query.cursor.fetchall()]}  # Fetches first column that is Agent ID

    def post(self):
        # This does not currently allow sending only some fields. All fields must be specified.
        new_agent_id = max(self.get().get('agents')) + 1
        print(new_agent_id)
        print(request.json)
        if not request.json:
            abort(400)

        try:
            if 'agent_name' in request.json and type(request.json['agent_name']) != unicode:
                abort(400)
            if 'agencurt_type' in request.json and type(request.json['agent_type']) != unicode:
                abort(400)
            if 'log_path' in request.json and type(request.json['log_path']) != unicode:
                abort(400)
            if 'notification_channel' in request.json and type(request.json['notification_channel']) != unicode:
                abort(400)
            if 'running_status' in request.json and type(request.json['running_status']) != unicode:
                abort(400)
            if 'skill_type' in request.json and type(request.json['skill_type']) != unicode:
                abort(400)
            if 'training_status' in request.json and type(request.json['training_status']) != unicode:
                abort(400)

            new_agent_name = request.json.get('agent')[0].get('agent_name')
            new_agent_type = request.json.get('agent')[0].get('agent_type')
            new_log_path = request.json.get('agent')[0].get('log_path')
            new_notification_channel = request.json.get('agent')[0].get('notification_channel')
            new_running_status = request.json.get('agent')[0].get('running_status')
            new_skill_type = request.json.get('agent')[0].get('skill_type')
            new_training_status = request.json.get('agent')[0].get('training_status')

            insert_query = ("insert into main.agents (agent_name, agent_type, log_path ,notification_channel, running_status, skill_type, training_status, agent_id ) "
            "values ('" + new_agent_name + "', '" +new_agent_type + "', '" +new_log_path + "', '" +new_notification_channel + "', '" + new_running_status + "', '" + new_skill_type + "', '" + new_training_status + "', '" + str(new_agent_id) + "');")

            print(insert_query)
            conn = db_connect.connect()
            query = conn.execute(insert_query)
            result_json = jsonify({'result': 'success'})
        except TypeError:
            print(traceback.format_exc())
            result_json = jsonify({'result': 'failure'})

        return result_json


class Agent_By_Id(Resource):
    def get(self, agent_id):
        conn = db_connect.connect()
        query = conn.execute("select * from main.agents where agent_id =%d;" % int(agent_id))
        result = {'agent': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

    def delete(self, agent_id):
        conn = db_connect.connect()
        query = conn.execute("delete from main.agents where agent_id =%d;" % int(agent_id))

class Notification_Channels(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from main.notification_channels;")
        # result = {'notification_channels': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        # return jsonify(result)

        return {'notification_channels': [i[0] for i in query.cursor.fetchall()]}

    def post(self):
        # This does not currently allow sending only some fields. All fields must be specified.
        channel_id = max(self.get().get('notification_channels')) + 1

        if not request.json:
            abort(400)
        if 'channel_name' in request.json and type(request.json['channel_name']) != unicode:
            abort(400)
        if 'channel_type' in request.json and type(request.json['channel_type']) is not unicode:
            abort(400)
        if 'configuration' in request.json and type(request.json['configuration']) is not unicode:
            abort(400)

        new_channel_name = request.json.get('notification_channels')[0].get('channel_name')
        new_channel_type = request.json.get('notification_channels')[0].get('channel_type')
        new_configuration = request.json.get('notification_channels')[0].get('configuration')
        try:
            insert_query = ("insert into main.notification_channels  (channel_name, channel_type, configuration, channel_id ) "
            "values ('" + new_channel_name + "', '" + new_channel_type + "', '" + new_configuration + "', '" + str(channel_id) + "');")

            print(insert_query)
            conn = db_connect.connect()
            query = conn.execute(insert_query)
            result_json = jsonify({'result': 'success'})
        except TypeError:
            result_json = jsonify({'result': 'failure'})

        return result_json

class Notification_Channels_By_Id(Resource):
    def get(self, channel_id):
        conn = db_connect.connect()
        query = conn.execute("select * from main.notification_channels where channel_id=%d;" % int(channel_id))
        result = {'notification_channels': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

    def delete(self, channel_id):
        conn = db_connect.connect()
        query = conn.execute("delete from main.notification_channels where channel_id =%d;" % int(channel_id))

api.add_resource(Agents, '/agents')
api.add_resource(Agent_By_Id, '/agents/<agent_id>')
api.add_resource(Notification_Channels, '/notification_channels')
api.add_resource(Notification_Channels_By_Id, '/notification_channels/<channel_id>')


if __name__ == '__main__':
    app.run(port='8888')
