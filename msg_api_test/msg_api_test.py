from api_project_get.get_api import sync_vivogpt
from api_project_get.get_api_msg import sync_vivogpt_msg


def get_msg_answer(data):
    print(data)
    q1 = data
    a1 = sync_vivogpt(data)
    print(a1)

    q2 = "成都"
    result = sync_vivogpt_msg(q1,a1,q2)
    print(result)
    return result