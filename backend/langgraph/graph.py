"""
LangGraph 主图定义
"""

from langgraph.graph import StateGraph, END
from langgraph.state import ConversationState
from .nodes.intent_node import intent_recognition_node
from .nodes.retrieval_node import retrieval_node
from .nodes.tool_node import tool_execution_node
from .nodes.nutrition_node import nutrition_calculation_node
from .nodes.response_node import response_generation_node
from .edges.conditions import should_use_rag, should_calculate_nutrition


class FitMealGraph:
    """LangGraph 图定义"""
    
    def __init__(self, db_session, llm):
        self.db = db_session
        self.llm = llm
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """构建 LangGraph"""
        graph = StateGraph(ConversationState)
        
        # 添加节点
        graph.add_node("intent_recognition", 
                      lambda state: intent_recognition_node(state, self.llm))
        graph.add_node("retrieval", 
                      lambda state: retrieval_node(state, self.db))
        graph.add_node("tool_execution", 
                      lambda state: tool_execution_node(state, self.db))
        graph.add_node("nutrition_calculation", 
                      lambda state: nutrition_calculation_node(state, self.db))
        graph.add_node("response_generation", 
                      lambda state: response_generation_node(state, self.llm))
        
        # 设置入口和边
        graph.set_entry_point("intent_recognition")
        graph.add_edge("intent_recognition", "retrieval")
        graph.add_edge("retrieval", "tool_execution")
        graph.add_edge("tool_execution", "nutrition_calculation")
        graph.add_edge("nutrition_calculation", "response_generation")
        graph.add_edge("response_generation", END)
        
        return graph.compile()
    
    async def invoke(self, state):
        """执行图"""
        return self.graph.invoke(state)
