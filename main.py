from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db = SQLAlchemy(app)



class VideoModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    views = db.Column(db.Integer,nullable=False)
    likes = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"Video(id={self.id},name={self.name},likes={self.likes},views={self.views})"

#db.create_all()

video_post_args = reqparse.RequestParser()
video_post_args.add_argument("name",type=str,help="Name of the video is required",required=True)
video_post_args.add_argument("likes",type=int,help="No.of likes for the video is required",required=True)
video_post_args.add_argument("views",type=int,help="No. of views for the video is required",required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name",type=str,required=False)
video_update_args.add_argument("likes",type=int,required=False)
video_update_args.add_argument("views",type=int,required=False)

resource_fields ={
    'id':fields.Integer,
    'name':fields.String,
    'views':fields.Integer,
    'likes':fields.Integer
                  }


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self,video_id): 
        result = VideoModel.query.filter_by(id=video_id).first()       
        if not result:
            abort(404,message="Video with given id doesn't exist!!!")
        return result
    
    @marshal_with(resource_fields)
    def post(self,video_id):
        args = video_post_args.parse_args()  
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409,message="Video Id already exist")
        video = VideoModel(id=video_id,name = args['name'], views = args['views'],likes = args['likes'])        
        db.session.add(video)
        db.session.commit()
        return VideoModel.query.filter_by(id=video_id).first(),201
    
    def delete(self,video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404,message="Video with given id doesn't exist!!!")                
        db.session.delete(result)
        db.session.commit()
        return '', 204
    
    @marshal_with(resource_fields)
    def patch(self,video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404,message="Video with given id doesn't exist!!!")
        if args['name'] is not None:
            result.name = args['name']            
        if args['likes'] is not None:
            result.likes = args['likes']
        if args['views'] is not None:
            result.views = args['views']
        db.session.commit()
        return VideoModel.query.filter_by(id=video_id).first(),200
        
        
     

api.add_resource(Video,"/video/<int:video_id>")
if __name__ =='__main__':
    app.run(debug=True)