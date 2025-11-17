"""
Content extraction service for PPT, PDF, and DOCX files
"""
import logging
from typing import List, Dict, Any, Optional
from pptx import Presentation
import PyPDF2
import docx
import os
from PIL import Image
import io

logger = logging.getLogger(__name__)

class ContentExtractor:
    """Extract content from various file formats"""

    def __init__(self):
        self.supported_formats = ['.ppt', '.pptx', '.pdf', '.docx', '.doc']

    def extract_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Extract content from file based on extension

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with extracted content
        """
        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext in ['.ppt', '.pptx']:
            return self.extract_from_ppt(file_path)
        elif file_ext == '.pdf':
            return self.extract_from_pdf(file_path)
        elif file_ext in ['.docx', '.doc']:
            return self.extract_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")

    def extract_from_ppt(self, file_path: str) -> Dict[str, Any]:
        """
        Extract content from PowerPoint files

        Args:
            file_path: Path to PPT/PPTX file

        Returns:
            Dictionary with slides, text, and metadata
        """
        logger.info(f"Extracting content from PowerPoint: {file_path}")

        try:
            prs = Presentation(file_path)
            slides_content = []

            for idx, slide in enumerate(prs.slides):
                slide_data = {
                    'slide_number': idx + 1,
                    'title': '',
                    'content': [],
                    'notes': '',
                    'has_images': False
                }

                # Extract text from shapes
                for shape in slide.shapes:
                    if hasattr(shape, "text") and shape.text:
                        text = shape.text.strip()
                        if text:
                            # Try to identify title
                            if shape.is_placeholder and shape.placeholder_format.type == 1:  # Title placeholder
                                slide_data['title'] = text
                            else:
                                slide_data['content'].append(text)

                    # Check for images
                    if shape.shape_type == 13:  # Picture
                        slide_data['has_images'] = True

                # Extract notes
                if slide.has_notes_slide:
                    notes_text = slide.notes_slide.notes_text_frame.text.strip()
                    if notes_text:
                        slide_data['notes'] = notes_text

                slides_content.append(slide_data)

            # Get presentation title (from first slide or filename)
            title = slides_content[0]['title'] if slides_content and slides_content[0]['title'] else os.path.splitext(os.path.basename(file_path))[0]

            return {
                'title': title,
                'total_slides': len(slides_content),
                'slides': slides_content,
                'source_type': 'presentation',
                'metadata': {
                    'file_name': os.path.basename(file_path),
                    'file_type': 'pptx'
                }
            }

        except Exception as e:
            logger.error(f"Error extracting from PowerPoint: {str(e)}")
            raise

    def extract_from_pdf(self, file_path: str) -> Dict[str, Any]:
        """
        Extract content from PDF files

        Args:
            file_path: Path to PDF file

        Returns:
            Dictionary with pages, text, and metadata
        """
        logger.info(f"Extracting content from PDF: {file_path}")

        try:
            pages_content = []

            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)

                for idx, page in enumerate(pdf_reader.pages):
                    text = page.extract_text().strip()

                    if text:
                        pages_content.append({
                            'page_number': idx + 1,
                            'content': text
                        })

            # Get title from first page or filename
            title = os.path.splitext(os.path.basename(file_path))[0]

            return {
                'title': title,
                'total_pages': len(pages_content),
                'pages': pages_content,
                'source_type': 'document',
                'metadata': {
                    'file_name': os.path.basename(file_path),
                    'file_type': 'pdf'
                }
            }

        except Exception as e:
            logger.error(f"Error extracting from PDF: {str(e)}")
            raise

    def extract_from_docx(self, file_path: str) -> Dict[str, Any]:
        """
        Extract content from Word documents

        Args:
            file_path: Path to DOCX file

        Returns:
            Dictionary with paragraphs, text, and metadata
        """
        logger.info(f"Extracting content from DOCX: {file_path}")

        try:
            doc = docx.Document(file_path)
            paragraphs_content = []

            for idx, para in enumerate(doc.paragraphs):
                text = para.text.strip()
                if text:
                    paragraphs_content.append({
                        'paragraph_number': idx + 1,
                        'content': text,
                        'style': para.style.name
                    })

            # Get title from first heading or filename
            title = os.path.splitext(os.path.basename(file_path))[0]
            for para in doc.paragraphs:
                if para.style.name.startswith('Heading'):
                    title = para.text.strip()
                    break

            return {
                'title': title,
                'total_paragraphs': len(paragraphs_content),
                'paragraphs': paragraphs_content,
                'source_type': 'document',
                'metadata': {
                    'file_name': os.path.basename(file_path),
                    'file_type': 'docx'
                }
            }

        except Exception as e:
            logger.error(f"Error extracting from DOCX: {str(e)}")
            raise

    def get_summary(self, extracted_content: Dict[str, Any]) -> str:
        """
        Get a text summary of extracted content

        Args:
            extracted_content: Dictionary with extracted content

        Returns:
            Text summary
        """
        summary_parts = []

        if 'slides' in extracted_content:
            for slide in extracted_content['slides']:
                if slide['title']:
                    summary_parts.append(f"Slide {slide['slide_number']}: {slide['title']}")
                if slide['content']:
                    summary_parts.append('\n'.join(slide['content']))
                if slide['notes']:
                    summary_parts.append(f"Notes: {slide['notes']}")
                summary_parts.append('')

        elif 'pages' in extracted_content:
            for page in extracted_content['pages']:
                summary_parts.append(f"Page {page['page_number']}:")
                summary_parts.append(page['content'])
                summary_parts.append('')

        elif 'paragraphs' in extracted_content:
            for para in extracted_content['paragraphs']:
                summary_parts.append(para['content'])

        return '\n'.join(summary_parts)
