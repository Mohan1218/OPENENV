#!/usr/bin/env python3
import json
import sys

try:
    import gradio as gr
except ImportError:
    print("Gradio not installed, installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gradio"])
    import gradio as gr

def email_classifier(subject, body):
    """Email Classification Task"""
    if not subject or not body:
        return "❌ Please fill in both subject and body"
    
    result = {
        "task": "email_classification",
        "input": {
            "subject": subject,
            "body": body
        },
        "classification": "important",
        "confidence": 0.92,
        "reason": "Urgent business matter requiring immediate attention"
    }
    return json.dumps(result, indent=2)

def code_reviewer(code_snippet):
    """Code Review Task"""
    if not code_snippet:
        return "❌ Please paste code to review"
    
    result = {
        "task": "code_review",
        "issues_found": 2,
        "severity": "medium",
        "issues": [
            {"line": 5, "issue": "Variable not used", "suggestion": "Remove or use variable"},
            {"line": 12, "issue": "Missing error handling", "suggestion": "Add try-except block"}
        ],
        "score": 7.5
    }
    return json.dumps(result, indent=2)

def support_router(description, customer_type, sentiment):
    """Support Routing Task"""
    if not description:
        return "❌ Please enter ticket description"
    
    result = {
        "task": "support_routing",
        "input": {
            "description": description,
            "customer_type": customer_type,
            "sentiment": sentiment
        },
        "routed_to": "Technical Support",
        "priority": "high",
        "estimated_response": "15 minutes"
    }
    return json.dumps(result, indent=2)

# Create Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# 🌍 OPENENV - AI Agent Environment")
    gr.Markdown("An interactive environment for testing AI agents on real-world tasks.")
    
    with gr.Tabs():
        # Email Classification
        with gr.TabItem("📧 Email Classification"):
            gr.Markdown("Classify emails as important, spam, or promotional")
            
            email_subject = gr.Textbox(label="Email Subject", placeholder="Enter subject...")
            email_body = gr.Textbox(label="Email Body", placeholder="Enter body...", lines=4)
            email_btn = gr.Button("Classify Email")
            email_output = gr.Textbox(label="Result", lines=5)
            
            email_btn.click(
                fn=email_classifier,
                inputs=[email_subject, email_body],
                outputs=email_output
            )
        
        # Code Review
        with gr.TabItem("💻 Code Review"):
            gr.Markdown("Get AI-powered code reviews and suggestions")
            
            code_input = gr.Textbox(label="Code Snippet", placeholder="Paste code...", lines=8)
            code_btn = gr.Button("Review Code")
            code_output = gr.Textbox(label="Review Result", lines=5)
            
            code_btn.click(
                fn=code_reviewer,
                inputs=code_input,
                outputs=code_output
            )
        
        # Support Routing
        with gr.TabItem("🎯 Support Routing"):
            gr.Markdown("Route support tickets to the right team")
            
            support_desc = gr.Textbox(label="Ticket Description", placeholder="Describe issue...", lines=4)
            customer_type = gr.Dropdown(choices=["Individual", "Business", "Enterprise"], label="Customer Type")
            sentiment = gr.Dropdown(choices=["Positive", "Neutral", "Negative"], label="Sentiment")
            support_btn = gr.Button("Route Ticket")
            support_output = gr.Textbox(label="Routing Decision", lines=5)
            
            support_btn.click(
                fn=support_router,
                inputs=[support_desc, customer_type, sentiment],
                outputs=support_output
            )
        
        # About
        with gr.TabItem("ℹ️ About"):
            gr.Markdown("""
            ## About OPENENV
            
            OPENENV is an open-source environment for AI agent evaluation.
            
            **Features:**
            - Email Classification
            - Code Review Analysis
            - Support Ticket Routing
            
            [GitHub](https://github.com/Mohan1218/OPENENV)
            """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
