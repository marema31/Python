from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from models.creator import CreatorModel
from flask_restful_swagger import swagger

class Creator(Resource):
    "Creator resource"
    @swagger.operation(
        notes='Get a creator item by ID',
        responseClass = CreatorModel.__name__,
        nickname      = 'get',
        parameters    = [
            {
              "name": "_id",
              "description": "Creator id",
              "required": True,
              "allowMultiple": False,
              "dataType": "integer",
              "paramType": "path"
            }
        ],
        responseMessages = [
            {
              "code": 200,
              "message": "Creator found"
            },
            {
              "code": 404,
              "message": "Creator not found"
            }
        ]
    )

    def get(self, _id):
        
        creator = CreatorModel.find_by_id(_id)
    
        if creator:
            return creator.json(), 200 # OK
        else:
            return{"message":"Creator {} not found".format(_id)}, 404 #not found

    def delete(self, _id):
        creator = CreatorModel.find_by_id(_id)
        if creator:
            creator.delete_from_db()
            return {'message': "Creator id {} has been deleted".format(_id)},200
        return {'message': "No Creator id {} to delete".format(_id)},200

class CreatorList(Resource):    

    args_required = {
         'lastname'  : fields.String(required = True,
                                     error_messages = { "required": "Creator lastname cannot be blank"}),
         'firstname' : fields.String(required = False),
    }       

    args_optional = {
         'lastname'   : fields.String(required = False),
         'firstname'  : fields.String(required = False),         
    }

    def ErrMsg(self,msg,args):
        if 'lastname' in args.keys() & 'firstname' in args.keys():
            return {"message":"Creator called {} {} {}".format(args['lastname'],args['firstname'],msg)}
        elif 'lastname' in args.keys():                    
            return {"message":"Creator lastname {} {} ".format(args['lastname'],msg)}
        elif 'firstname' in args.keys():                    
            return {"message":"Creator firstname {} {} ".format(args['firstname'],msg)}
        
    @use_args(args_optional)       
    def get(self,args):       
        creators = CreatorModel.find(**args)        
        if creators:
            creatorsJSON = []
            for creator in creators:
                creatorsJSON.append(creator.json())
            return {"creators":creatorsJSON}, 200 # OK
        else:
            return self.ErrMsg("not found",args), 404 # Not found

    @use_args(args_required)        
    def post(self, args):
        if CreatorModel.find(**args):
            return self.ErrMsg("already exist",args), 400 # Bad request

        creator = CreatorModel(**args)   
        # creator = CreatorModel(data['username'], data['password'])
        # for each of the keys in data say key = value  
        # ie username = value, password = value
        creator.save_to_db()

        return self.ErrMsg("created successfully",args), 201 # created

    @use_args(args_required)         
    def delete(self,args):
        creator = CreatorModel.find(**args)
        if creator:
            creator.delete_from_db()
            return self.ErrMsg("has been deleted",args), 200
        return self.ErrMsg("to delete",args), 200    