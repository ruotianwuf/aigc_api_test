
from hw_pp_correct.get_OCR_check import ocr_test
from hw_pp_correct.ai_check_answer import sync_vivogpt



def get_correct_check(path):

    handwriting_result = ocr_test(path)

    message = "学生提交:" + str(handwriting_result["result"])

    result1 = sync_vivogpt(message)

    print(result1)

    return result1

# path = '地理题/地理 +手写答案_01.jpg'
# check_answer(path)