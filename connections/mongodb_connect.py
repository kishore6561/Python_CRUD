from flask import Flask,request,jsonify,make_response
from flask_restful import Resource
import pymongo
import json
import config


class Mongoconnect(Resource):
    def post(self):

            try:
                meta_data_dict = get_meta_data_json_replace_quotes()
            except:
               pass

            config.ACTIVE_ENV = meta_data_dict["environment"]
            databaselist = []
            samplelist = meta_data_dict["data"]
            print(samplelist)

            given_data_storing_list=list(meta_data_dict["data"].keys())
            args=config.ENVS[config.ACTIVE_ENV]
            myclient = pymongo.MongoClient(host=args['DB_HOST'], port=args['DB_PORT'], username=args['DB_USERNAME'], 
            password=args['DB_PASSWORD'])
            mydb = myclient[args["DB_NAME"]]
            mycol = mydb["settings"]

            result=mycol.find_one({"type":meta_data_dict["type_of_app"]})
            databaselist=result["clients"]
            

            print(databaselist)
            print("connected to "+config.ACTIVE_ENV)

            try:
                for name_of_db in databaselist:
                    print(name_of_db)
                    if meta_data_dict["Operation_type"]=="update" or meta_data_dict["Operation_type"]=="Update":
                            for i in given_data_storing_list: 
                                myclient = pymongo.MongoClient(host=args['DB_HOST'], port=args['DB_PORT'], username=args['DB_USERNAME'], 
                                password=args['DB_PASSWORD'])
                                mydb = myclient[name_of_db]
                                mycol = mydb[meta_data_dict["collection_details"]]

                                mycol.update_one({meta_data_dict["name_key_find"]:meta_data_dict["key_value_to_find"]},
                                    {"$set":{i:samplelist[i]}})

                    elif meta_data_dict["Operation_type"]=="insert" or meta_data_dict["Operation_type"]=="Insert":
                        
                        myclient = pymongo.MongoClient(host=args['DB_HOST'], port=args['DB_PORT'], username=args['DB_USERNAME'], 
                        password=args['DB_PASSWORD'])
                        mydb = myclient[name_of_db]
                        mycol = mydb[meta_data_dict["collection_details"]]
                        mycol.save(samplelist)
                        #return make_response(jsonify({"result":"Insert data success","status_code":200}),200)

                    else:
                        print("Operation not allowed")
                        return make_response(jsonify({"result":"NO Operation","status_code":400}),400)
                        
                return make_response(jsonify({"result":"Updated success","status_code":200}),200)
            except Exception as e :
                print(str(e))
                
class Insert_data_by_type(Resource):
        #config.ACTIVE_ENV="testing"
        def get(self,app_id,colllection_name,key,value,type):

            args=config.ENVS[config.ACTIVE_ENV]
            myclient = pymongo.MongoClient(host=args['DB_HOST'], port=args['DB_PORT'], username=args['DB_USERNAME'], 
                password=args['DB_PASSWORD'])
            mydb = myclient[app_id]
            mycol = mydb[colllection_name]
            if type!="":
                mycol.update_one({"type":type},{"$set":{key:value}})
                return make_response(jsonify({"result":"Updated success","status_code":200}),200)
            else:
                return make_response(jsonify({"result":"NO Operation Type and Guid is empty","status_code":400}),400)

class Insert_data_by_guid(Resource):
    #config.ACTIVE_ENV="testing"
    def get(self,app_id,colllection_name,key,value,guid):
        args=config.ENVS[config.ACTIVE_ENV]
        myclient = pymongo.MongoClient(host=args['DB_HOST'], port=args['DB_PORT'], username=args['DB_USERNAME'], 
            password=args['DB_PASSWORD'])
        mydb = myclient[app_id]
        mycol = mydb[colllection_name]
        if guid!="":
            mycol.update_one({"guid":guid},{"$set":{key:value}})
            return make_response(jsonify({"result":"Updated success","status_code":200}),200)
        else:
            return make_response(jsonify({"result":"NO Operation Type and Guid is empty","status_code":400}),400)

class Repalce_string(Resource):
    #config.ACTIVE_ENV="testing"
    def post(self):
        my_json = request.data.decode('utf8').replace("'", '"') 
        meta_data_dict = json.loads(my_json)
        args=config.ENVS[config.ACTIVE_ENV]
        myclient = pymongo.MongoClient(host=args['DB_HOST'], port=args['DB_PORT'], username=args['DB_USERNAME'], 
                                password=args['DB_PASSWORD'])
        mydb = myclient[meta_data_dict["app_id"]]
        mycol = mydb[meta_data_dict["collection_details"]]

        result=mycol.find( {meta_data_dict["key_to_replace"]: {"$regex": meta_data_dict["value_to_replace"] }})
        for i in result:
            if result.retrieved != 0:
                    for k,v in i.items():
                        if k==meta_data_dict["key_to_replace"]:
                            print(v)
                            replace_string=v.replace(meta_data_dict["value_to_replace"],"")
                            print(replace_string)
                            mycol.update({meta_data_dict["key_to_replace"]:v},{"$set":{meta_data_dict["key_to_replace"]:replace_string}})
            else:
                return make_response(jsonify({"result":"NO key vaule to be replaced","status_code":400}),400)
        return make_response(jsonify({"result":"Updated success","status_code":200}),200)


class Update_in_engage(Resource):
    def post(self):
        my_json = request.data.decode('utf8').replace("'", '"') 
        meta_data_dict = json.loads(my_json)
        config.ACTIVE_ENV=meta_data_dict["environment"]
        samplelist=meta_data_dict["data"]
        print(samplelist)
        given_data_storing_list=list(meta_data_dict["data"].keys())
        args=config.ENVS[config.ACTIVE_ENV]
        myclient = pymongo.MongoClient(host=args['DB_HOST'], port=args['DB_PORT'], username=args['DB_USERNAME'], 
        password=args['DB_PASSWORD'])
        mydb = myclient[args["DB_NAME"]]
        mycol = mydb["settings"]
        result=mycol.find_one({"type":meta_data_dict["type_of_app"]})
        databaselist=result["clients"]
        print(databaselist)
        for name_of_db in databaselist:
            for i in given_data_storing_list:
                myclient = pymongo.MongoClient(host=args['DB_HOST'], port=args['DB_PORT'], username=args['DB_USERNAME'], 
                password=args['DB_PASSWORD'])
                mydb = myclient[args["DB_NAME"]]
                mycol = mydb["global_settings"]
                mycol.update_one({"apikey":name_of_db},{"$set":{"message_dict."+i:samplelist[i]}})
            print(name_of_db)
        return make_response(jsonify({"result":"Updated success","status_code":200}),200)    
    
class Data_retrive_in_settings(Resource):
    def get(self,type_of_app,name_of_collection,type_of_key,type_of_data):
        #config.ACTIVE_ENV="testing"
        config.ACTIVE_ENV="live"
        list_of_data=[]
        args=config.ENVS[config.ACTIVE_ENV]
        myclient = pymongo.MongoClient(host=args['DB_HOST'], port=args['DB_PORT'], username=args['DB_USERNAME'], 
        password=args['DB_PASSWORD'])
        mydb = myclient[args["DB_NAME"]]
        mycol = mydb["settings"]
        result=mycol.find_one({"type":type_of_app})
        databaselist=result["clients"]
        print(databaselist)
        for name_of_db in databaselist:
                result={}
                myclient = pymongo.MongoClient(host=args['DB_HOST'], port=args['DB_PORT'], username=args['DB_USERNAME'], 
                password=args['DB_PASSWORD'])
                mydb = myclient[name_of_db]
                mycol = mydb[name_of_collection]
                result=mycol.find_one({type_of_key:type_of_data})
                try:
                    result["app_id"]=name_of_db
                except:
                    if result==None:
                        result={}
                        result["app_id"]=name_of_db
                    else:
                        result["app_id"]=""
                if "_id" in result:
                    result.pop("_id")
                list_of_data.append(result)
                print(name_of_db)

        return make_response(jsonify({"result":list_of_data,"status_code":200}),200)


def get_meta_data_json_replace_quotes() -> dict:
    if 'json' in request.form:
        json_of_metadata = request.form.to_dict(flat=False)
        try:
            meta_data_from_json = json_of_metadata['json']
            meta_data_from_json_0 = meta_data_from_json[0]
            str_meta_data_from_json_0 = str(meta_data_from_json_0)
            meta_data_dict = json.loads(str_meta_data_from_json_0)
        except Exception as e:
            print(str(e))
    else:
        if request.data is not None:
            try:
                my_json = request.data.decode('utf8').replace("'", '\'')
                meta_data_dict = json.loads(my_json)
            except:
                pass
        else:
            return make_response(jsonify({"result":"no json"}), 400)
    return meta_data_dict