def format_questions_answers_dict(qa_list):
    formatted_qa = []
    for qa in qa_list:
        if isinstance(qa, dict) and 'q' in qa and 'a' in qa:
            formatted_qa.append(f"Question: {qa['q']}\nAnswer: {qa['a']}")
    return "\n\n".join(formatted_qa)