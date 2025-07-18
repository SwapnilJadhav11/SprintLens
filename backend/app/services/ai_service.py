from openai import OpenAI
from app.core.config import settings
from typing import List, Dict

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_summary(messages: List[Dict], github_data: Dict | None = None, jira_data: Dict | None = None) -> str:
    """
    Generate a comprehensive sprint summary from Slack messages, GitHub data, and Jira data using OpenAI GPT.
    
    Args:
        messages: List of message dicts with 'user', 'timestamp', 'text' keys
        github_data: Optional GitHub repository data
        jira_data: Optional Jira project data
    
    Returns:
        Generated summary string
    """
    if not messages:
        return "No messages found for the specified time period."
    
    # Format messages for the prompt
    formatted_messages = []
    for msg in messages:
        # Skip system messages like "user joined channel"
        if "has joined the channel" in msg.get("text", ""):
            continue
        formatted_messages.append(f"- {msg.get('text', '')}")
    
    if not formatted_messages:
        return "No relevant messages found for summary generation."
    
    messages_text = "\n".join(formatted_messages)
    
    # Create the prompt
    system_prompt = """You are a helpful assistant that generates sprint summaries from team communications. 
    Focus on identifying key accomplishments, blockers, and next steps from the conversation."""
    
    # Build comprehensive context
    context_parts = []
    
    # Add Slack messages
    if messages_text:
        context_parts.append(f"**Slack Communications:**\n{messages_text}")
    
    # Add GitHub data
    if github_data and "error" not in github_data:
        github_context = []
        if github_data.get("pull_requests"):
            github_context.append(f"**Pull Requests:** {len(github_data['pull_requests'])} PRs")
        if github_data.get("issues"):
            github_context.append(f"**Issues:** {len(github_data['issues'])} issues")
        if github_data.get("commits"):
            github_context.append(f"**Commits:** {len(github_data['commits'])} commits")
        if github_context:
            context_parts.append("\n".join(github_context))
    
    # Add Jira data
    if jira_data and "error" not in jira_data:
        jira_context = []
        if jira_data.get("issues"):
            jira_context.append(f"**Jira Issues:** {len(jira_data['issues'])} issues")
        if jira_data.get("sprints"):
            jira_context.append(f"**Sprints:** {len(jira_data['sprints'])} sprints")
        if jira_context:
            context_parts.append("\n".join(jira_context))
    
    full_context = "\n\n".join(context_parts)
    
    user_prompt = f"""Here is comprehensive data from our team's communication and development activities this week. 
    Please analyze and summarize under these categories:
    
    - Key Accomplishments (from Slack, GitHub, and Jira)
    - Blockers & Issues
    - Next Steps & Action Items
    - Development Progress (PRs, commits, releases)
    
    Data:
    {full_context}
    
    Please provide a comprehensive, actionable summary that would be useful for sprint planning and team coordination."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        return content.strip() if content else "No summary generated."
        
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return f"Error generating summary: {str(e)}" 