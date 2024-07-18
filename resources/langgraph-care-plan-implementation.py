from langgraph.graph import Graph
from langgraph.graph import StateGraph, END
from gemini_initializer import GeminiInitializer
from datetime import date
from typing import List, Dict
import json
import sub_plan
import time
from typing import TypedDict, List, Dict

# Initialize the GeminiInitializer
standardize_care_plan_llm = GeminiInitializer()

# Define the state schema
class CareState(TypedDict):
    subplans: List[str]
    analyzed_subplans: List[str]
    similarity_analysis: str
    combined_subplans: str
    enhanced_subplans: str
    review_summary: str
    final_plan_summary: str

# Define the agents (nodes)

def subplan_analyzer(state):
    """Analyzes each subplan and identifies main components."""
    print("\n--- Subplan Analyzer Started ---")
    analyzed_subplans = []
    for i, subplan in enumerate(state['subplans']):
        prompt = f"""
        Analyze the following subplan and identify its main components:
        Subplan {i+1}:
        {subplan}

        Identify and summarize the following components:
        1. Assessed Current Situation
        2. Care Needs
        3. Outcomes and Goals
        4. Description of Care Actions
        5. Reviews
        """
        response = standardize_care_plan_llm.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0)
        analyzed_subplans.append(response)
        print(f"Analyzed Subplan {i+1}")
    
    state['analyzed_subplans'] = analyzed_subplans
    print(analyzed_subplans)
    print("--- Subplan Analyzer Completed ---")
    return state

def similarity_detector(state):
    """Compares analyzed subplans for similarities and decides which should be combined."""
    print("\n--- Similarity Detector Started ---")
    prompt = f"""
    Compare the following analyzed subplans for similarities:
    {state['analyzed_subplans']}

    Identify groups of subplans that are highly similar and would benefit from combination.
    Provide a list of subplan groups that should be combined, and explain your reasoning.
    """
    response = standardize_care_plan_llm.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0)
    state['similarity_analysis'] = response
    print("Similarity Analysis Completed")
    print(response)
    print("--- Similarity Detector Completed ---")
    return state

def combination_agent(state):
    """Combines similar subplans as identified by the Similarity Detector."""
    print("\n--- Combination Agent Started ---")
    prompt = f"""
    Based on the following similarity analysis:
    {state['similarity_analysis']}

    Combine the identified similar subplans into comprehensive subplans.
    Provide the combined subplans, ensuring all unique elements from the original subplans are incorporated.
    """
    response = standardize_care_plan_llm.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0)
    state['combined_subplans'] = response
    print("Subplans Combined")
    print(response)
    print("--- Combination Agent Completed ---")
    return state

def enhancement_agent(state):
    """Improves clarity, fixes grammar, and enhances content for all subplans."""
    print("\n--- Enhancement Agent Started ---")
    prompt = f"""
    Enhance the following subplans:
    {state['combined_subplans']}

    1. Improve clarity and coherence of the content.
    2. Ensure consistent and professional language throughout.
    3. Fix any grammar and spelling mistakes.
    4. Enhance content accuracy and completeness.
    5. Reformat and expand sentences for better readability and comprehensiveness.
    """
    response = standardize_care_plan_llm.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0)
    state['enhanced_subplans'] = response
    print("Subplans Enhanced")
    print(response)
    print("--- Enhancement Agent Completed ---")
    return state

def review_agent(state):
    """Checks the enhanced subplans for consistency and completeness."""
    print("\n--- Review Agent Started ---")
    prompt = f"""
    Review the following enhanced subplans:
    {state['enhanced_subplans']}

    Ensure:
    1. All original information is preserved.
    2. The subplans are consistent and complete.
    3. The enhancements have not introduced any errors or inconsistencies.

    Provide a review summary and any necessary corrections.
    """
    response = standardize_care_plan_llm.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0)
    state['review_summary'] = response
    print("Review Completed")
    print(response)
    print("--- Review Agent Completed ---")
    return state

def summary_generator(state):
    """Creates a final summary of the entire process."""
    print("\n--- Summary Generator Started ---")
    prompt = f"""
    Based on the entire care plan analysis process, generate a comprehensive summary including:
    1. The number of original subplans
    2. The number of resulting subplans after analysis and combination
    3. A brief overview of how the subplans were reorganized
    4. Any key observations or recommendations based on the analysis

    Use the following information to create your summary:
    {state}
    """
    response = standardize_care_plan_llm.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0)
    state['final_plan_summary'] = response
    print("Final Summary Generated")
    print("--- Summary Generator Completed ---")
    return state

# Create the graph
workflow = StateGraph(CareState)

# Add nodes to the graph
workflow.add_node("Subplan Analyzer", subplan_analyzer)
workflow.add_node("Similarity Detector", similarity_detector)
workflow.add_node("Combination Agent", combination_agent)
workflow.add_node("Enhancement Agent", enhancement_agent)
workflow.add_node("Review Agent", review_agent)
workflow.add_node("Summary Generator", summary_generator)

# Define the edges (connections between nodes)
workflow.set_entry_point("Subplan Analyzer")
workflow.add_edge("Subplan Analyzer", "Similarity Detector")
workflow.add_edge("Similarity Detector", "Combination Agent")
workflow.add_edge("Combination Agent", "Enhancement Agent")
workflow.add_edge("Enhancement Agent", "Review Agent")
workflow.add_edge("Review Agent", "Summary Generator")
workflow.add_edge("Summary Generator", END)

def final_care_plan(*subplans: str) -> Dict:
    """
    Analyzes, potentially combines, and enhances multiple care plan subplans using a LangGraph workflow.

    Args:
    - *subplans: Variable number of input strings, each containing a care plan subsection for a resident.

    Returns:
    - Dict: A dictionary containing the updated care plans and analysis summary.
    """
    today = date.today()
    formatted_date = today.strftime("%d/%m/%y")
    print("Today's date:", formatted_date)

    # Initialize the state with the input subplans
    initial_state = CareState(
        subplans=list(subplans),
        analyzed_subplans=[],
        similarity_analysis="",
        combined_subplans="",
        enhanced_subplans="",
        review_summary="",
        final_plan_summary=""
    )

    print(f"\nInitializing workflow with {len(subplans)} subplans")

    # Create a new instance of the graph for each run
    app = workflow.compile()

    # Run the graph
    try:
        for output in app.invoke(initial_state):
            print(f"Current output type: {type(output)}")
            print(f"Current output content: {output}")
            
            if isinstance(output, dict) and "final_plan_summary" in output and output["final_plan_summary"]:
                final_state = output
                break
        else:
            print("Warning: Workflow completed without producing a final plan summary.")
            final_state = output  # Use the last state as the final state
    except Exception as e:
        print(f"An error occurred during workflow execution: {str(e)}")
        return {"error": str(e)}

    print("\n--- Final State ---")
    print(json.dumps(final_state, indent=2))
    
    return final_state

# Example usage
if __name__ == "__main__":
    print("Starting Care Plan Analysis")
    start_time = time.time()

    try:
        result = final_care_plan(
            sub_plan.sub_plan_1,
            sub_plan.sub_plan_2,
            sub_plan.sub_plan_3,
            sub_plan.sub_plan_4,
            sub_plan.sub_plan_5,
            sub_plan.sub_plan_6
        )
        
        if "error" in result:
            print(f"Error in care plan analysis: {result['error']}")
        else:
            print("Care Plan Analysis Completed Successfully")
            
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

    end_time = time.time()
    inference_time = end_time - start_time
    print(f"\nInference Time: {inference_time:.2f} seconds")