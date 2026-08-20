import openai
import os
from PyPDF2 import PdfReader
import io
import re

class SmartBotUtils:
    def __init__(self):
        self.openai_client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
    
    def ask_question(self, question):
        """Get answer to a general question"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": question}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def summarize_text(self, text):
        """Summarize long text"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Summarize the following text concisely."},
                    {"role": "user", "content": text}
                ],
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def rewrite_text(self, text, style="professional"):
        """Rewrite text to be clearer and more professional"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Rewrite this text to be more {style} and clear."},
                    {"role": "user", "content": text}
                ],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_ideas(self, topic, count=5):
        """Generate ideas for a given topic"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Generate {count} creative ideas about {topic}."},
                    {"role": "user", "content": f"Generate {count} ideas about {topic}"}
                ],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def explain_topic(self, topic, complexity="simple"):
        """Explain a topic in simple terms"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Explain {topic} in {complexity} terms."},
                    {"role": "user", "content": f"Explain {topic} simply"}
                ],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def translate_text(self, text, target_language):
        """Translate text to target language"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Translate to {target_language}."},
                    {"role": "user", "content": text}
                ],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def analyze_document(self, file_content, file_name):
        """Analyze uploaded document"""
        try:
            # Extract text from PDF
            if file_name.lower().endswith('.pdf'):
                pdf_reader = PdfReader(io.BytesIO(file_content))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
            else:
                # For text files
                text = file_content.decode('utf-8')[:4000]  # Limit text size
            
            # Generate summary
            summary = self.summarize_text(text)
            
            # Extract key points
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Extract key points and provide a summary."},
                    {"role": "user", "content": f"Document content: {text[:3000]}"}
                ],
                max_tokens=300
            )
            
            key_points = response.choices[0].message.content
            return f"📄 **Document Analysis**\n\n**Summary:**\n{summary}\n\n**Key Points:**\n{key_points}"
        except Exception as e:
            return f"Error analyzing document: {str(e)}"
