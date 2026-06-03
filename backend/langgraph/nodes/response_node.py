"""
响应生成节点
"""

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

RESPONSE_PROMPT = PromptTemplate(
    input_variables=["intent", "recommendations"],
    template="""根据以下生成回复：
意图: {intent}
推荐: {recommendations}

请用中文解释。
"""
)

async def response_generation_node(state, llm):
    """响应生成节点"""
    chain = LLMChain(llm=llm, prompt=RESPONSE_PROMPT)
    
    response = chain.run(
        intent=state.get("intent", ""),
        recommendations=str(state.get("meal_recommendations", []))
    )
    
    state["final_response"] = response
    return state
