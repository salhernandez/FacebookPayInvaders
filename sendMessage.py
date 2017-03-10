import json
def send_message(recipient_id, message_text):

    #log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    #log("test2 {recipient}".format(recipient="derp"))

    # data = json.dumps({
    #     "recipient": {
    #         "id": recipient_id
    #     },
    #     "message": {
    #         "text": message_text
    #     }
    # })

    dataDict = {}
    dataDict['recipient'] = {}
    dataDict['message'] = {}
    
    
    dataDict['recipient']['id'] = "1"
    dataDict['message']['text'] = "2"
    
    data = json.dumps(dataDict)
    
    return data

def sendShareButton():
    
#     curl -X POST -H "Content-Type: application/json" -d '{
#   "recipient":{
#     "id":"USER_ID"
#   },
#   "message":{
#     "attachment":{
#       "type":"template",
#       "payload":{
#         "template_type":"generic",
#         "elements":[
#           {
#             "title":"Breaking News: Record Thunderstorms",
#             "subtitle":"The local area is due for record thunderstorms over the weekend.",
#             "image_url":"https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
#             "buttons":[
#               {
#                 "type":"element_share"
#               }              
#             ]
#           }
#         ]
#       }
#     }
#   }
    
    dataDict = {}
    dataDict['recipient'] = {}
    dataDict['message'] = {}
    
    dataDict['recipient']['id'] = "1234"
    dataDict['message']['attachment'] = {}
    dataDict['message']['attachment']['type'] =  "template"
    dataDict['message']['attachment']['payload'] = {}
    dataDict['message']['attachment']['payload']['template_type'] = "generic"
    dataDict['message']['attachment']['payload']['elements'] = {}
    dataDict['message']['attachment']['payload']['elements']['title'] = "teheee"
    dataDict['message']['attachment']['payload']['elements']['subtitle'] = "ayeee"
    dataDict['message']['attachment']['payload']['elements']['image_url'] = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
    dataDict['message']['attachment']['payload']['elements']['buttons'] = {}
    dataDict['message']['attachment']['payload']['elements']['buttons']['type'] = "element_share"
    
    data = json.dumps(dataDict)
    
    print data
sendShareButton()