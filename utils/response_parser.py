import json

class ResponseParser:
    """Utility class for parsing AI responses"""
    
    @staticmethod
    def parse_evaluation_response(response_text):
        """
        Parse the AI response to extract JSON evaluation data
        
        Args:
            response_text (str): Raw response from AI model
            
        Returns:
            list: Parsed evaluation data
            
        Raises:
            ValueError: If parsing fails or data is invalid
        """
        try:
            # Try to find JSON content in the response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON array found in response")
            
            json_str = response_text[start_idx:end_idx]
            evaluation_data = json.loads(json_str)
            
            # Validate that we have exactly 10 metrics
            if len(evaluation_data) != 10:
                raise ValueError(f"Expected 10 metrics, got {len(evaluation_data)}")
            
            # Validate structure of each metric
            required_fields = ['metric', 'score', 'reasoning']
            for item in evaluation_data:
                if not all(field in item for field in required_fields):
                    raise ValueError(f"Missing required fields in metric: {item}")
            
            return evaluation_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error parsing evaluation response: {str(e)}")