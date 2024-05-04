import get_OCR_check
import ai_check_answer



def check_answer(path):

    handwriting_result = get_OCR_check.ocr_test(path)

    # correct_result = get_OCR_check.ocr_test('/Users/apple/PycharmProjects/aigc_api_test/hw_pp_check/地理题/地理+答案_01.jpg')

    message = "学生提交:" + str(handwriting_result["result"])

    result1 = ai_check_answer.sync_vivogpt(message)

    print(result1)

    # result2 = ai_check_answer.sync_vivogpt("请再次仔细检查："+message)

    # print(result2)
    # if handwriting_result == correct_result:
    #     print("正确")
    # else:
    #     print("有错")

# path = '/Users/apple/PycharmProjects/aigc_api_test/hw_pp_check/地理题/地理 +手写答案_01.jpg'
# check_answer(path)