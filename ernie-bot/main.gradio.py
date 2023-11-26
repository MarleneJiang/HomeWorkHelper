import gradio as gr
import erniebot
import requests


def format_tuples(array):
    formatted_list = []
    for tuple_pair in array:
        formatted_list.append({"role": "user", "content": tuple_pair[0]})
        formatted_list.append({"role": "assistant", "content": tuple_pair[1]})
    return formatted_list


def search_answers(question):
    # 定义请求的URL
    url = "https://gpts.idealeap.cn/search"

    # 设置查询参数
    params = {"question": question}

    try:
        # 发送GET请求
        response = requests.get(url, params=params)

        # 检查响应的状态码
        if response.status_code == 200:
            # 解析JSON响应
            data = response.json()

            # 提取答案
            answers = data.get("answers", [])
            formatted_output = "\n".join(
                f"相关问题: {item['question']}\n相关答案: {item['answer']}" for item in answers
            )
            return formatted_output + f"\n\n我想问的是：{question}"
        else:
            # 处理错误响应
            error = response.json().get("error", "Unknown Error")
            return f"Error: {error}"
    except Exception as e:
        # 捕获并处理任何异常
        return f"Exception occurred: {e}"


erniebot.api_type = "aistudio"


def get_answer(searched_answer):
    response = erniebot.ChatCompletion.create(
        model="ernie-bot-turbo",
        messages=[
            {
                "role": "user",
                "content": f"你将遵守以下规则：不直接告诉我答案，而是通过提示和问题引导我自己思考。你会结合搜索到的答案，告诉我需要的相关知识点，指导我如何思考出正确答案。\n{searched_answer}",
            }
        ],
    )
    return response.get_result()


with gr.Blocks() as demo:
    gr.Markdown(
        """
    # 大学生作业帮
    大学生哪有不疯的，只是硬撑罢了～
    > 本应用内置网络题库数据源，不仅有答案，还有推导过程！
    """
    )
    with gr.Row():
        access_token_box = gr.Textbox(
            label="文心一言AccessToken",
            placeholder="请输入文心一言AccessToken",
            lines=1,
            container=False,
            show_label=False,
            scale=4,
        )        
        access_token_button = gr.Button("保存")
    def save_access_token(access_token):
        global erniebot
        erniebot.access_token = access_token
        return access_token
    access_token_button.click(save_access_token, [access_token_box], [access_token_box])


    chatbot = gr.Chatbot()
    with gr.Row():
        msg = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="请输入问题～",
            container=False,
        )
        msg_submit = gr.Button("发送")
    clear = gr.ClearButton([msg, chatbot], value="重置对话")

    def respond(message, chat_history):
        if len(chat_history) == 0:
            searched_answer = search_answers(message)
            print("正在输出答案～")
            chat_history.append((message, get_answer(searched_answer)))
        else:
            messages = format_tuples(chat_history)
            messages.append({"role": "user", "content": message})
            print("正在输出答案～")
            new_answer = erniebot.ChatCompletion.create(
                model="ernie-bot",
                messages=messages,
            ).get_result()
            chat_history.append((message,new_answer))

        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    msg_submit.click(respond, [msg, chatbot], [msg, chatbot])
    gr.Markdown(
    """
    > 建议一个问题一次对话哦～
    ---
    ## 交流群
    ![联系方式](https://cos.idealeap.cn/Other/WeChat.jpg)
    """
    )

demo.launch()
