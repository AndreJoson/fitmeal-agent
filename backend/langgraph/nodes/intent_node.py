"""
意图识别节点
"""

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

INTENT_PROMPT = PromptTemplate(
    input_variables=["user_message"],
    template="""分析用户意图，分类为：
- query_meal: 询问食物信息
- get_nutrition: 询问营养信息
- plan_week: 生成周餐计划
- compare_foods: 比较食物
- other: 其他

用户消息: {user_message}

格式: 意图: [intent]\n置信度: [0-1]
"""
)

async def intent_recognition_node(state, llm):
    """意图识别节点"""
    chain = LLMChain(llm=llm, prompt=INTENT_PROMPT)
    response = chain.run(user_message=state["user_message"])
    
    intent = "query_meal"
    confidence = 0.8
    
    try:
        if "意图:" in response:
            intent = response.split("意图:")[1].split("\n")[0].strip()
        if "置信度:" in response:
            confidence = float(response.split("置信度:")[1].strip())
    except:
        pass
    
    state["intent"] = intent
    state["confidence"] = confidence
    return state
