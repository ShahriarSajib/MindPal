# chat_engine.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import base64
import config

class ChatbotEngine:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model=config.MODEL_NAME,
            google_api_key=api_key,
            temperature=0.7
        )

    def stream_response(self, chat_history: list):
        """
        Yields chunk tokens line-by-line using generators to drive 
        st.write_stream without blocking front-end operations.
        """
        try:
            for chunk in self.llm.stream(chat_history):
                if isinstance(chunk.content, str):
                    yield chunk.content
                elif isinstance(chunk.content, list) and len(chunk.content) > 0:
                    block = chunk.content[0]
                    if isinstance(block, dict) and 'text' in block:
                        yield block['text']
        except Exception as e:
            yield f"⚠️ Stream Processing Exception Raised: {str(e)}"

    @staticmethod
    def format_multimodal_message(text_prompt: str, image_bytes: bytes, mime_type: str) -> HumanMessage:
        """Packages text strings and binary image files into standard LangChain format."""
        base64_encoded = base64.b64encode(image_bytes).decode("utf-8")
        return HumanMessage(
            content=[
                {"type": "text", "text": text_prompt if text_prompt else "Analyze this attachment:"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{base64_encoded}"},
                },
            ]
        )