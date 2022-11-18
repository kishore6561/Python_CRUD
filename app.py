from flask import Flask
from flask_restful import Api
from sample.hello import hello
from connections.mongodb_connect import Insert_data_by_type, Mongoconnect,Insert_data_by_guid,Repalce_string,Update_in_engage,Data_retrive_in_settings
from connections.Mysql_connection import Mysqlconnect
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app=Flask(__name__)

#Swagger 
SWAGGER_URL="/swagger"
API_URL="/static/like_reaction_ui.json"
SWAGGER_BLUEPRINT=get_swaggerui_blueprint(
	SWAGGER_URL,
	API_URL,
	config={
		'app_name':"Engage_API"
	}
)
app.register_blueprint(SWAGGER_BLUEPRINT,url_prefix=SWAGGER_URL)
application=Api(app)
CORS(app, supports_credentials=True)

application.add_resource(hello,"/hello")
application.add_resource(Mongoconnect,"/mongo")
application.add_resource(Insert_data_by_guid,"/mongo/<app_id>/<colllection_name>/<key>/<value>/guid/<guid>")
application.add_resource(Insert_data_by_type,"/mongo/<app_id>/<colllection_name>/<key>/<value>/type/<type>")
application.add_resource(Repalce_string,"/mongo/replace")
application.add_resource(Mysqlconnect,"/mysql")
application.add_resource(Update_in_engage,"/mongo/update_in_engage")
application.add_resource(Data_retrive_in_settings,"/mongo/<type_of_app>/<name_of_collection>/<type_of_key>/<type_of_data>")

    
if __name__ == "__main__":
	app.run(debug=True)
    