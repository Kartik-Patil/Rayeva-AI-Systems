"""
Core AI service layer for Rayeva AI Systems.
Handles AI provider interactions with logging and error handling.
"""
import json
import time
from typing import Type, TypeVar, Optional
from pydantic import BaseModel
from openai import OpenAI

from .config import settings
from .logging_service import logging_service


# Type variable for Pydantic models
T = TypeVar('T', bound=BaseModel)


class AIService:
    """
    Centralized AI service for AI provider interactions.
    Provides structured output generation with logging and validation.
    """
    
    def __init__(self):
        self.provider = settings.ai_provider.lower()

        if self.provider == "groq":
            self.client = OpenAI(
                api_key=settings.groq_api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            self.model = settings.groq_model
        elif self.provider == "gemini":
            raise ValueError("Gemini provider is disabled in this build. Set AI_PROVIDER=groq.")
        else:
            raise ValueError(f"Unsupported AI provider: {settings.ai_provider}")

        self.logger = logging_service.get_logger("ai_service")
        self.max_tokens = settings.gemini_max_tokens
        self.temperature = settings.gemini_temperature
    
    def _build_detailed_json_template(self, schema: Type[T]) -> dict:
        """
        Build a detailed JSON template with example values for nested structures.
        
        Args:
            schema: Pydantic model to analyze
            
        Returns:
            Detailed JSON template with realistic example values
        """
        schema_json = schema.model_json_schema()
        properties = schema_json.get("properties", {})
        required_fields = schema_json.get("required", list(properties.keys()))
        definitions = schema_json.get("$defs", {})
        
        def build_field_template(field_name: str, field_schema: dict, depth: int = 0) -> any:
            """Recursively build template for a field."""
            max_recursion_depth = 2
            if depth > max_recursion_depth:
                return "..."
            
            field_type = field_schema.get("type", "string")
            
            # Handle string types
            if field_type == "string":
                # Use description or sensible default
                description = field_schema.get("description", "").lower()
                if "product" in description and "id" in description:
                    return "prod_example123"
                elif "id" in description:
                    return "id_value"
                elif "price" in description or "cost" in description:
                    return 100.0
                elif "date" in description or "time" in description:
                    return "2026-04-15"
                elif "count" in description or "total" in description:
                    return "10"
                else:
                    return "example text"
            
            # Handle number types
            elif field_type == "number":
                # Check for constraints
                maximum = field_schema.get("maximum")
                minimum = field_schema.get("minimum")
                
                # Check field name for clues
                name_lower = field_name.lower()
                if "confidence" in name_lower or "score" in name_lower:
                    return 0.85  # Default confidence value between 0-1
                elif "percentage" in name_lower or "percent" in name_lower:
                    return 50.0
                elif "price" in name_lower or "cost" in name_lower:
                    return 100.0
                
                # Respect maximum constraint
                if maximum is not None:
                    return min(0.95, maximum)  # Use 0.95 if max is 1, or go to max
                elif minimum is not None:
                    return maximum if maximum else (minimum + 10)
                
                return 99.99
            
            # Handle integer types
            elif field_type == "integer":
                # Check for constraints
                maximum = field_schema.get("maximum")
                minimum = field_schema.get("minimum")
                
                name_lower = field_name.lower()
                if "quantity" in name_lower or "count" in name_lower:
                    return 100
                elif "score" in name_lower or "rating" in name_lower:
                    return 5
                
                if maximum is not None and maximum <= 1:
                    return maximum
                elif maximum is not None:
                    return min(10, maximum)
                
                return 10
            
            # Handle boolean types
            elif field_type == "boolean":
                return True
            
            # Handle array types
            elif field_type == "array":
                items_schema = field_schema.get("items", {})
                
                # Check if it's an array of objects with a reference
                if "$ref" in items_schema:
                    # Extract definition name
                    ref_name = items_schema["$ref"].split("/")[-1]
                    if ref_name in definitions:
                        obj_schema = definitions[ref_name]
                        # Build one example object
                        obj_template = {}
                        obj_properties = obj_schema.get("properties", {})
                        obj_required = obj_schema.get("required", [])
                        
                        for obj_field in obj_required:
                            obj_field_schema = obj_properties.get(obj_field, {})
                            obj_template[obj_field] = build_field_template(obj_field, obj_field_schema, depth + 1)
                        
                        return [obj_template]
                    else:
                        return [{}]
                else:
                    # Simple array item type
                    example_item = build_field_template(field_name, items_schema, depth + 1)
                    return [example_item]
            
            # Handle object types
            elif field_type == "object":
                # Check if there's a reference
                if "$ref" in field_schema:
                    ref_name = field_schema["$ref"].split("/")[-1]
                    if ref_name in definitions:
                        obj_schema = definitions[ref_name]
                        obj_template = {}
                        obj_properties = obj_schema.get("properties", {})
                        obj_required = obj_schema.get("required", [])
                        
                        for obj_field in obj_required:
                            obj_field_schema = obj_properties.get(obj_field, {})
                            obj_template[obj_field] = build_field_template(obj_field, obj_field_schema, depth + 1)
                        
                        return obj_template
                else:
                    return {}
            
            return "value"
        
        json_template = {}
        for field_name in required_fields:
            field_schema = properties.get(field_name, {})
            json_template[field_name] = build_field_template(field_name, field_schema)
        
        return json_template

    async def generate_structured_output(
        self,
        system_prompt: str,
        user_prompt: str,
        schema: Type[T],
        temperature: Optional[float] = None,
        max_retries: int = 3
    ) -> T:
        """
        Generate AI response conforming to Pydantic schema.
        
        Args:
            system_prompt: System role and instructions
            user_prompt: User input and context
            schema: Pydantic model class for response validation
            temperature: Override default temperature
            max_retries: Number of retry attempts on failure
            
        Returns:
            Validated Pydantic model instance
            
        Raises:
            ValueError: If response doesn't match schema after retries
            Exception: For API or network errors
        """
        start_time = time.time()
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Build detailed template
                json_template = self._build_detailed_json_template(schema)
                schema_json = schema.model_json_schema()
                required_fields = schema_json.get("required", [])

                schema_instruction = (
                    "Return ONLY a JSON object with real values (NOT a schema). "
                    f"Use EXACTLY these required keys: {required_fields}. "
                    f"Field names must match exactly. "
                    f"Output JSON example structure:\n{json.dumps(json_template, indent=2)}"
                )

                completion = self.client.chat.completions.create(
                    model=self.model,
                    temperature=temperature or self.temperature,
                    max_tokens=self.max_tokens,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "system", "content": schema_instruction},
                        {"role": "user", "content": user_prompt},
                    ],
                    response_format={"type": "json_object"}
                )

                content = completion.choices[0].message.content or "{}"
                usage = completion.usage
                tokens_used = (usage.total_tokens if usage else 0)
                
                # Parse and validate
                response_data = json.loads(content)
                validated_output = schema(**response_data)
                
                # Log successful interaction
                processing_time_ms = int((time.time() - start_time) * 1000)
                logging_service.log_ai_interaction(
                    module="ai_service",
                    prompt=user_prompt[:200],  # Truncate for logging
                    response=response_data,
                    tokens_used=tokens_used,
                    processing_time_ms=processing_time_ms
                )
                
                self.logger.info(
                    f"AI generation successful (attempt {attempt + 1}/{max_retries})",
                    extra={"data": {
                        "tokens": tokens_used,
                        "time_ms": processing_time_ms
                    }}
                )
                
                return validated_output
                
            except json.JSONDecodeError as e:
                last_error = f"Invalid JSON response: {str(e)}"
                self.logger.warning(f"Attempt {attempt + 1} failed: {last_error}")
                
            except Exception as e:
                last_error = str(e)
                self.logger.error(f"AI generation error (attempt {attempt + 1}): {last_error}")
                
                # Don't retry on authentication errors
                if "authentication" in str(e).lower():
                    raise
        
        # All retries failed
        processing_time_ms = int((time.time() - start_time) * 1000)
        logging_service.log_ai_interaction(
            module="ai_service",
            prompt=user_prompt[:200],
            response={},
            tokens_used=0,
            processing_time_ms=processing_time_ms,
            error=last_error
        )
        
        raise ValueError(f"Failed to generate valid output after {max_retries} attempts: {last_error}")
    
    async def generate_text(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None
    ) -> str:
        """
        Generate simple text response without structure validation.
        
        Args:
            system_prompt: System role and instructions
            user_prompt: User input
            temperature: Override default temperature
            
        Returns:
            AI-generated text response
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                temperature=temperature or self.temperature,
                max_tokens=self.max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
            )

            content = completion.choices[0].message.content or ""
            return content
            
        except Exception as e:
            self.logger.error(f"Text generation error: {str(e)}")
            raise
    
    def estimate_cost(self, tokens_used: int) -> float:
        """
        Estimate cost for token usage.
        
        Args:
            tokens_used: Number of tokens consumed
            
        Returns:
            Estimated cost in USD (Gemini pricing)
        """
        # Approximate pricing placeholder for Groq-hosted open models.
        # Keep at 0.0 for free-tier/dev tracking in this project.
        if self.provider == "groq":
            return 0.0

        cost_per_1m_input = 0.0
        cost_per_1m_output = 0.0
        
        # Estimate: split tokens 50/50 between input and output
        input_tokens = tokens_used // 2
        output_tokens = tokens_used - input_tokens
        
        input_cost = (input_tokens / 1000000) * cost_per_1m_input
        output_cost = (output_tokens / 1000000) * cost_per_1m_output
        
        return input_cost + output_cost


# Global AI service instance
ai_service = AIService()
