from modelscope_agent.tools.tool import Tool, ToolSchema
import requests

class SearchAnswersTool(Tool):

    description = '搜索用户问题的答案'
    name = 'search_answers'
    parameters: list = [{
        'name': 'question',
        'description': '用户的查询问题',
        'required': True
    }]

    def _local_call(self, *args, **kwargs):
        question = kwargs['question']
        try:
            response = requests.get("https://gpts.idealeap.cn/search", params={"question": question})
            response.raise_for_status()
            return {'result': response.json()}
        except requests.RequestException as e:
            return {'result': str(e)}

