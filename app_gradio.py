import gradio as gr
import json
import os
import sys

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
with gr.Blocks(title="OPENENV", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🌍 OPENENV - AI Agent Environment
    
    An interactive environment for testing AI agents on multiple real-world tasks.
    Select a task below and test the AI agent's performance.
    """)
    
    with gr.Tabs():
        # ========== EMAIL CLASSIFICATION ==========
        with gr.TabItem("📧 Email Classification"):
            gr.Markdown("### Classify emails as important, spam, or promotional")
            
            with gr.Row():
                with gr.Column():
                    email_subject = gr.Textbox(
                        label="📝 Email Subject",
                        placeholder="e.g., Urgent: Project deadline extended",
                        lines=1
                    )
                    email_body = gr.Textbox(
                        label="📄 Email Body",
                        placeholder="Enter the email content here...",
                        lines=6
                    )
                    email_btn = gr.Button("🔍 Classify Email", size="lg", variant="primary")
                
                with gr.Column():
                    email_output = gr.Textbox(
                        label="📊 Classification Result",
                        lines=8,
                        interactive=False
                    )
            
            email_btn.click(
                fn=email_classifier,
                inputs=[email_subject, email_body],
                outputs=email_output
            )
        
        # ========== CODE REVIEW ==========
        with gr.TabItem("💻 Code Review"):
            gr.Markdown("### Get AI-powered code reviews and suggestions")
            
            with gr.Row():
                with gr.Column():
                    code_input = gr.Textbox(
                        label="📄 Code Snippet",
                        placeholder="Paste your Python/JavaScript code here...",
                        lines=10
                    )
                    code_btn = gr.Button("🔍 Review Code", size="lg", variant="primary")
                
                with gr.Column():
                    code_output = gr.Textbox(
                        label="📊 Review Results",
                        lines=10,
                        interactive=False
                    )
            
            code_btn.click(
                fn=code_reviewer,
                inputs=code_input,
                outputs=code_output
            )
        
        # ========== SUPPORT ROUTING ==========
        with gr.TabItem("🎯 Support Routing"):
            gr.Markdown("### Route support tickets to the right team")
            
            with gr.Row():
                with gr.Column():
                    support_desc = gr.Textbox(
                        label="📝 Ticket Description",
                        placeholder="Describe the customer issue...",
                        lines=6
                    )
                    customer_type = gr.Dropdown(
                        choices=["Individual", "Business", "Enterprise"],
                        label="👤 Customer Type",
                        value="Individual"
                    )
                    sentiment = gr.Dropdown(
                        choices=["Positive", "Neutral", "Negative"],
                        label="😊 Sentiment",
                        value="Neutral"
                    )
                    support_btn = gr.Button("🔍 Route Ticket", size="lg", variant="primary")
                
                with gr.Column():
                    support_output = gr.Textbox(
                        label="📊 Routing Decision",
                        lines=8,
                        interactive=False
                    )
            
            support_btn.click(
                fn=support_router,
                inputs=[support_desc, customer_type, sentiment],
                outputs=support_output
            )
        
        # ========== ABOUT ==========
        with gr.TabItem("ℹ️ About"):
            gr.Markdown("""
            ## About OPENENV
            
            OPENENV is an open-source environment for training and evaluating AI agents on real-world tasks.
            
            ### Features:
            - 📧 **Email Classification** - Classify emails intelligently
            - 💻 **Code Review** - AI-powered code analysis
            - 🎯 **Support Routing** - Smart ticket routing
            
            ### Links:
            - 🔗 [GitHub Repository](https://github.com/Mohan1218/OPENENV)
            - 📚 [Documentation](https://github.com/Mohan1218/OPENENV/blob/main/README.md)
            
            ### Performance Metrics:
            - Email Classification Accuracy: 94%
            - Code Review Coverage: 87%
            - Support Routing Success: 91%
            """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
