"""
Diagram generation service using Mermaid syntax
"""
import logging
from typing import Optional, Dict, Any
from services.llm_service import LLMService

logger = logging.getLogger(__name__)

class DiagramService:
    """Service for generating Mermaid diagrams"""

    def __init__(self):
        self.llm_service = LLMService()

    async def generate_diagram(
        self,
        concept: str,
        diagram_type: Optional[str] = None,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate Mermaid diagram for a concept

        Args:
            concept: Concept to visualize
            diagram_type: Type of diagram (flowchart, mindmap, etc.)
            context: Additional context

        Returns:
            Dictionary with diagram code and metadata
        """
        logger.info(f"Generating diagram for concept: {concept}")

        # If no diagram type specified, let AI decide
        if not diagram_type:
            diagram_type = await self._determine_diagram_type(concept, context)

        # Generate diagram code based on type
        diagram_code = await self._generate_diagram_code(concept, diagram_type, context)

        return {
            "diagram_code": diagram_code,
            "diagram_type": diagram_type,
            "explanation": f"Visual representation of {concept}"
        }

    async def _determine_diagram_type(self, concept: str, context: Optional[str]) -> str:
        """
        Determine the best diagram type for a concept

        Args:
            concept: Concept to visualize
            context: Additional context

        Returns:
            Diagram type
        """
        system_prompt = """You are an expert at choosing the best visualization type for educational concepts.

Available diagram types:
- flowchart: For processes, algorithms, decision flows
- mindmap: For concept relationships, brainstorming, hierarchies
- timeline: For chronological events, historical sequences
- tree: For classifications, taxonomies, organizational structures
- network: For connections, relationships between entities
- sequence: For interactions, communications, step-by-step processes

Choose the most appropriate diagram type."""

        prompt = f"""Concept: {concept}
Context: {context or 'None'}

Which diagram type would best visualize this concept? Respond with just the diagram type name (flowchart, mindmap, timeline, tree, network, or sequence)."""

        response = await self.llm_service.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=50
        )

        diagram_type = response.strip().lower()

        # Validate response
        valid_types = ['flowchart', 'mindmap', 'timeline', 'tree', 'network', 'sequence']
        if diagram_type not in valid_types:
            logger.warning(f"Invalid diagram type '{diagram_type}', defaulting to flowchart")
            diagram_type = 'flowchart'

        return diagram_type

    async def _generate_diagram_code(
        self,
        concept: str,
        diagram_type: str,
        context: Optional[str]
    ) -> str:
        """
        Generate Mermaid diagram code

        Args:
            concept: Concept to visualize
            diagram_type: Type of diagram
            context: Additional context

        Returns:
            Mermaid diagram code
        """
        system_prompt = f"""You are an expert at creating Mermaid diagrams for educational purposes.

Generate clear, well-structured Mermaid {diagram_type} diagrams that help students visualize and understand concepts.

Guidelines:
- Use proper Mermaid syntax
- Keep diagrams clear and not too complex
- Use descriptive labels
- Organize logically
- Make it educational and easy to understand"""

        # Different prompts for different diagram types
        if diagram_type == 'flowchart':
            example = """graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E"""
            instruction = "Create a flowchart showing the process or flow"

        elif diagram_type == 'mindmap':
            example = """mindmap
  root((Main Concept))
    Topic 1
      Subtopic 1.1
      Subtopic 1.2
    Topic 2
      Subtopic 2.1
      Subtopic 2.2"""
            instruction = "Create a mind map showing concept relationships"

        elif diagram_type == 'timeline':
            example = """timeline
    title Historical Timeline
    1900 : Event 1
    1920 : Event 2
    1940 : Event 3
    1960 : Event 4"""
            instruction = "Create a timeline showing chronological sequence"

        elif diagram_type == 'tree':
            example = """graph TD
    A[Root] --> B[Branch 1]
    A --> C[Branch 2]
    B --> D[Leaf 1]
    B --> E[Leaf 2]
    C --> F[Leaf 3]"""
            instruction = "Create a tree diagram showing hierarchical structure"

        elif diagram_type == 'sequence':
            example = """sequenceDiagram
    participant A as Entity A
    participant B as Entity B
    A->>B: Action 1
    B->>A: Response 1
    A->>B: Action 2"""
            instruction = "Create a sequence diagram showing interactions"

        else:  # network
            example = """graph LR
    A[Node A] --- B[Node B]
    B --- C[Node C]
    C --- D[Node D]
    A --- D"""
            instruction = "Create a network diagram showing connections"

        prompt = f"""Concept: {concept}
Context: {context or 'Use general knowledge'}

{instruction} for this concept using Mermaid syntax.

Example format:
```mermaid
{example}
```

Generate the Mermaid code now. Return ONLY the Mermaid code, no explanations."""

        response = await self.llm_service.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.5,
            max_tokens=1000
        )

        # Extract mermaid code from response
        import re
        mermaid_match = re.search(r'```mermaid\s*(.*?)\s*```', response, re.DOTALL)
        if mermaid_match:
            diagram_code = mermaid_match.group(1).strip()
        else:
            # Remove any markdown code blocks
            diagram_code = re.sub(r'```.*?\n', '', response)
            diagram_code = re.sub(r'```', '', diagram_code)
            diagram_code = diagram_code.strip()

        return diagram_code

    async def enhance_section_with_diagram(
        self,
        section_title: str,
        section_content: str,
        diagram_description: str,
        diagram_type: str
    ) -> str:
        """
        Generate diagram for a specific lesson section

        Args:
            section_title: Section title
            section_content: Section content
            diagram_description: What the diagram should show
            diagram_type: Type of diagram

        Returns:
            Mermaid diagram code
        """
        context = f"Section: {section_title}\n\nContent: {section_content}\n\nDiagram should show: {diagram_description}"

        result = await self.generate_diagram(
            concept=section_title,
            diagram_type=diagram_type,
            context=context
        )

        return result["diagram_code"]
