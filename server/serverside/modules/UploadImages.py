from flask import request
from flask_restful import Resource, reqparse
import os

from .Models.User import UserModel
from .Models.Image import ImageModel

from .Utils import Utils

class UploadImages(Resource):
    def __init__(self):
        self.__UA = UserModel()
        self.__im = ImageModel()
        self.ALLOW_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp']


    def get_api_token(self):

        api_token = request.args.get('api_token')

        if api_token == None:
            raise Exception('Missing API Token')
        else: 
            return api_token
        
    def get_user_id(self):
        user_id = request.args.get('id')

        if user_id == None: 
            raise Exception('Missing user_id')
        else: 
            return user_id
        
    def get_passphrase(self):
        passphrase = request.args.get('passphrase')

        if passphrase == None: 
            raise Exception('Missing passphrase')
        else: 
            return passphrase
        
        
    def get_image(self):
        try: 
            image_file = request.files['image']
        except Exception: 
            raise Exception('No image selected')
        else: 
            _, extension = os.path.splitext(image_file.filename.lower())

            if extension not in self.ALLOW_EXTENSIONS: 
                raise Exception('Extension not allowed')
            else:  
                return image_file
        
    def post(self):
        try: 
            user_id = Utils.get_input('user_id')

            api_token = Utils.get_input('api_token')

            passphrase = Utils.get_input('passphrase')

            real_name = Utils.get_input('real_name')

            check_sum = Utils.get_input('checksum')

            image =  self.get_image()

            if not self.__UA.check_api_token(user_id, api_token):
                raise Exception('Permission denied: either user_id or api_token is wrong')
            
            else: 
                new_path, new_img_id = self.__im.save_img_dir(image)
                self.__im.save_img_record(
                    user_id, new_img_id, 
                    passphrase, new_path, 
                    real_name, check_sum
                )
        
        except Exception as e: 
            print(e)
            return {
                'error': True, 
                'message': str(e)
            }, 400
        else: 
            return {
                'error': False, 
                'image_filename': real_name, 
                'image_id': new_img_id, 
                'message': 'Upload successfully'
            }, 200

