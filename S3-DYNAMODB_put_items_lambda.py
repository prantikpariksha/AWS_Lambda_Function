import boto3
from datetime import datetime
list1=[]

def convert (t1):
    t_min,t_hr = t1[3:],t1[:2]
    temp1 = int(t_min) + 30
    
    if temp1 >= 60:
        t_min_final = temp1 - 60
        t_hr_final = int(t_hr) + 1 + 5
        final_time = str(t_hr_final) + ':' + str(t_min_final)
        return final_time
    
    else:
        t_hr_final = int(t_hr) + 5
        t_min_final = int(t_min) + 30
        final_time = str(t_hr_final) + ':' + str(t_min_final)
        return final_time
    
def lambda_handler(event, context):
    now = datetime.now()
    t = now.strftime("%H:%M")
    invctn_time = convert(t)   
    lambda_invctn_time = datetime.strptime(invctn_time,'%H:%M')
    
    s3_cnsle = boto3.resource("s3","us-east-1")
    dynamodb_cnsle = boto3.resource('dynamodb')
    topic = boto3.client("sns")

    for each_bucket in s3_cnsle.buckets.all():
        if each_bucket.name == "getimage1":    #edit this name as per requirement
            for each_obj in each_bucket.objects.all():
                time1  = each_obj.last_modified.strftime("%H:%M")
                upload_time = convert(time1)   
                upload_time_final = datetime.strptime(upload_time,'%H:%M')
                diff_in_min = str(lambda_invctn_time - upload_time_final)
                diff_in_min_final = diff_in_min[-5:-3]
             
                if  int(diff_in_min_final) <= 2 :
                    key_name = each_obj.key
                    obj_size = str(each_obj.size)
                    obj_storage = each_obj.storage_class
                 
                    table_name = dynamodb_cnsle.Table("GETIMAGES_table") . #edit this name as per requirement
                    table_name.put_item(
                         Item = {
                                 'OBJ_KEY':key_name,
                                 'OBJ_SIZE(KB)':obj_size,
                                 'OBJ_STORAGE_CLASS':obj_storage
                                 
                                }
                                                )
                    print("PutItem succeeded:")
                    
                    topic.publish(TargetArn='arn:aws:sns:ap-south-1:243874029274:dynamodb',
                                  Message='prantik',
                                  Subject='testing done'
                                  )
                    print("message sent")
                else:
                    print("do nothing")
        else:
            print("DO NOTHING2")
                 
