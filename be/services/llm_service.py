"""
LLM Service for AI-powered content generation
Supports OpenAI and Anthropic
"""
import os
import logging
from typing import List, Dict, Any, Optional
import anthropic
import openai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class LLMService:
    """Service for interacting with LLM providers"""

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()

        if self.provider == "openai":
            self.api_key = os.getenv("OPENAI_API_KEY")
            self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
            if self.api_key:
                openai.api_key = self.api_key
        elif self.provider == "anthropic":
            self.api_key = os.getenv("ANTHROPIC_API_KEY")
            self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
            if self.api_key:
                self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

        if not self.api_key:
            logger.warning(f"No API key found for {self.provider}")

    async def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        Generate completion from LLM

        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text
        """
        try:
            if self.provider == "openai":
                return await self._generate_openai(prompt, system_prompt, temperature, max_tokens)
            elif self.provider == "anthropic":
                return await self._generate_anthropic(prompt, system_prompt, temperature, max_tokens)
        except Exception as e:
            logger.error(f"Error generating completion: {str(e)}")
            raise

    async def _generate_openai(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate completion using OpenAI"""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        response = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content

    async def _generate_anthropic(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate completion using Anthropic"""
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}]
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)

        return response.content[0].text

    async def generate_lesson_structure(
        self,
        content: str,
        title: str,
        language: str = "en",
        difficulty_level: str = "intermediate"
    ) -> Dict[str, Any]:
        """
        Generate structured lesson from content

        Args:
            content: Source content to learn from
            title: Lesson title
            language: Target language (en/bn)
            difficulty_level: Difficulty level

        Returns:
            Structured lesson dictionary
        """
        lang_instruction = "in English" if language == "en" else "in Bangla (Bengali)"

        system_prompt = f"""You are an expert educational content creator for students (Class 6-12 & University).
Your task is to create comprehensive, interactive lessons that transform basic content into detailed learning materials.

Guidelines:
- Break down complex concepts into simple, understandable parts
- Provide real-world examples and applications
- Include cultural context relevant to Bangladeshi students when appropriate
- Use progressive difficulty - start simple, build complexity
- Identify key concepts and explain them thoroughly
- Suggest when diagrams would be helpful
- Language: {lang_instruction}
- Difficulty Level: {difficulty_level}"""

        prompt = f"""Create a comprehensive lesson from this content:

Title: {title}

Content:
{content}

Generate a structured lesson with the following sections:
1. Introduction - What is this topic about? Why is it important?
2. Prerequisites - What should students know beforehand?
3. Core Concepts - Break down the main ideas (create multiple sub-sections as needed)
4. Real-world Examples - Practical applications and examples
5. Common Misconceptions - What students often get wrong
6. Practice Questions - Questions to test understanding
7. Summary - Key takeaways

For each section, identify if a diagram would help explain the concept. If yes, describe what type of diagram would be useful (flowchart, mind map, timeline, tree, network, or sequence diagram).

Return the response in JSON format with this structure:
{{
    "title": "lesson title",
    "description": "brief description",
    "subject": "subject area",
    "difficulty_level": "{difficulty_level}",
    "prerequisites": ["prerequisite 1", "prerequisite 2"],
    "sections": [
        {{
            "title": "section title",
            "content": "detailed explanation",
            "order": 1,
            "needs_diagram": true/false,
            "diagram_type": "flowchart/mindmap/timeline/tree/network/sequence or null",
            "diagram_description": "what the diagram should show",
            "examples": ["example 1", "example 2"],
            "key_points": ["point 1", "point 2"]
        }}
    ],
    "summary": "overall summary"
}}"""

        response = await self.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=4000
        )

        # Parse JSON response
        import json
        import re

        # Extract JSON from response (handle markdown code blocks)
        json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = response

        try:
            lesson_data = json.loads(json_str)
            return lesson_data
        except json.JSONDecodeError:
            # Fallback: return basic structure
            logger.warning("Failed to parse JSON response, using fallback")
            return {
                "title": title,
                "description": "Generated lesson content",
                "subject": "General",
                "difficulty_level": difficulty_level,
                "prerequisites": [],
                "sections": [
                    {
                        "title": "Lesson Content",
                        "content": response,
                        "order": 1,
                        "needs_diagram": False,
                        "diagram_type": None,
                        "diagram_description": None,
                        "examples": [],
                        "key_points": []
                    }
                ],
                "summary": "Review the key concepts covered in this lesson."
            }

    async def answer_question(
        self,
        question: str,
        context: str,
        conversation_history: List[Dict[str, str]] = None,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Answer student questions with context

        Args:
            question: Student's question
            context: Lesson context
            conversation_history: Previous conversation
            language: Response language

        Returns:
            Answer dictionary with related concepts
        """
        lang_instruction = "in English" if language == "en" else "in Bangla (Bengali)"

        system_prompt = f"""You are a patient, knowledgeable tutor helping students (Class 6-12 & University) understand their lessons.

Guidelines:
- Provide clear, detailed explanations
- Use examples to illustrate concepts
- Break down complex ideas into simpler parts
- Be encouraging and supportive
- Relate concepts to real-world applications
- Suggest related concepts to explore
- Language: {lang_instruction}"""

        # Build conversation context
        history_text = ""
        if conversation_history:
            for msg in conversation_history[-5:]:  # Last 5 messages
                role = "Student" if msg["role"] == "user" else "Tutor"
                history_text += f"{role}: {msg['content']}\n"

        prompt = f"""Lesson Context:
{context}

Previous Conversation:
{history_text}

Student's Question: {question}

Provide a detailed answer that:
1. Directly answers the question
2. Provides relevant examples
3. Suggests 2-3 related concepts to explore
4. Offers additional practice examples if applicable

Return response in JSON format:
{{
    "answer": "detailed answer to the question",
    "related_concepts": ["concept 1", "concept 2", "concept 3"],
    "additional_examples": ["example 1", "example 2"]
}}"""

        response = await self.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=1500
        )

        # Parse JSON response
        import json
        import re

        json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = response

        try:
            answer_data = json.loads(json_str)
            return answer_data
        except json.JSONDecodeError:
            # Fallback
            return {
                "answer": response,
                "related_concepts": [],
                "additional_examples": []
            }

    async def generate_topic_content(
        self,
        topic: str,
        language: str = "en",
        difficulty_level: str = "intermediate"
    ) -> str:
        """
        Generate comprehensive content for a topic by researching and synthesizing information

        Args:
            topic: Topic to generate content for
            language: Target language
            difficulty_level: Difficulty level

        Returns:
            Comprehensive content text
        """
        lang_instruction = "in English" if language == "en" else "in Bangla (Bengali)"

        system_prompt = f"""You are an expert educator creating comprehensive learning content for students.
Your task is to generate detailed, accurate educational content on any topic requested.

Guidelines:
- Provide factually accurate information
- Use authoritative knowledge
- Include historical context where relevant
- Cover fundamental concepts thoroughly
- Include real-world applications
- Make content engaging and accessible
- Language: {lang_instruction}
- Difficulty Level: {difficulty_level}"""

        prompt = f"""Generate comprehensive educational content about: {topic}

Create detailed content covering:
1. Introduction and overview
2. Historical background (if relevant)
3. Fundamental concepts and principles
4. Key components or elements
5. How it works or functions
6. Real-world applications and examples
7. Current developments or modern relevance
8. Common questions and misconceptions

Make the content detailed enough to create a multi-section lesson. Include specific examples, facts, and explanations that would help a student deeply understand this topic."""

        response = await self.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=3000
        )

        return response
