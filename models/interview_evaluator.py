import google.generativeai as genai
from config.settings import Config

class InterviewEvaluator:
    """Model for structured interview evaluation using Gemini API"""
    
    def __init__(self):
        # Configure Gemini API
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def evaluate(self, video_bytes, mime_type):
        """
        Evaluate interview video with structured metrics
        
        Args:
            video_bytes: Binary video data
            mime_type: MIME type of the video
            
        Returns:
            str: Structured evaluation result from Gemini
        """
        try:
            prompt = self._get_interview_evaluation_prompt()
            
            # Create content with video and evaluation prompt
            response = self.model.generate_content([
                {
                    "mime_type": mime_type,
                    "data": video_bytes
                },
                prompt
            ])
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Error evaluating interview: {str(e)}")
    
    def _get_interview_evaluation_prompt(self):
        """Get the detailed interview evaluation prompt"""
        return """You are an AI interview evaluation assistant.

You will be provided with the transcript of a recorded interview. Your job is to assess the candidate's performance across 10 specific evaluation metrics.

For **each metric**, you must:
1. Assign a **score out of 10** (e.g., "7/10").
2. Provide a **concise and clear reasoning** for the assigned score based solely on the transcript.
3. Output the results in a **structured JSON format** with three fields:
   - "metric": the name of the evaluation metric
   - "score": score out of 10 (e.g., "7/10")
   - "reasoning": a brief explanation of why that score was given

The final output should be a **JSON array containing exactly 10 objects**, each representing one metric.

---

Below are the **10 metrics with detailed evaluation guidelines**. Evaluate each metric strictly according to the instructions.

---

1. **Communication Skills**  
_Assess how clearly and effectively the candidate expresses ideas._

Evaluate based on:
- Clarity and ease of understanding
- Logical structure in responses
- Minimal use of filler words
- Consistent and appropriate pace
- Rich and context-appropriate vocabulary

Scoring:
- 9–10: Fluent and articulate with minimal filler words
- 6–8: Understandable but occasional filler words or pacing issues
- 1–5: Disjointed, unclear, poor structure or vocabulary

---

2. **Confidence**  
_Assess self-assurance and composure._

Evaluate based on:
- Steady tone and assured delivery
- Lack of hesitation or second-guessing
- Assertiveness without arrogance
- Comfortable elaboration on topics
- Inferred cues of composure from transcript

Scoring:
- 9–10: Very confident and calm
- 6–8: Moderate confidence with minor hesitation
- 1–5: Hesitant, unsure, or nervous tone

---

3. **Presentation Skills**  
_Assess organization and delivery of responses._

Evaluate based on:
- Structured answers (e.g., intro → body → conclusion)
- Smooth transitions between ideas
- Use of examples or illustrations
- Clarity and relevance of content

Scoring:
- 9–10: Clear, organized, well-explained responses
- 6–8: Some structure but lacks flow or transitions
- 1–5: Disorganized or incoherent delivery

---

4. **Body Language**  
_Assess non-verbal cues inferred from transcript._

Evaluate based on:
- Descriptions or implications of posture, gestures
- Inferred confidence or nervousness (e.g., frequent "um", hesitation)
- Consistency between verbal and non-verbal tone

Scoring:
- 9–10: Confident and expressive (if video cues are available)
- 6–8: Mild nervousness or stiffness inferred
- 1–5: Excessive nervous signals or lack of expression

Note: If visual cues are unavailable, use language indicators only.

---

5. **Technical Knowledge**  
_Assess understanding of relevant technical topics._

Evaluate based on:
- Accuracy and completeness of responses
- Correct use of technical terminology
- Ability to explain reasoning
- Depth of both theoretical and applied knowledge

Scoring:
- 9–10: In-depth, correct, and confident technical responses
- 6–8: Mostly correct with minor gaps
- 1–5: Vague, incorrect, or shallow technical answers

---

6. **Problem Solving / Critical Thinking**  
_Assess logical thinking and structured reasoning._

Evaluate based on:
- Ability to break down problems step-by-step
- Clear articulation of assumptions and reasoning
- Consideration of alternatives
- Logical flow and creativity in solutions

Scoring:
- 9–10: Well-reasoned, structured, and insightful approach
- 6–8: Logical but lacks creativity or depth
- 1–5: Poorly structured or flawed reasoning

---

7. **Listening Skills**  
_Assess attentiveness and relevance of responses._

Evaluate based on:
- Direct and relevant answers
- Acknowledgment of the question
- Clarifying when needed
- Adjusting based on follow-ups
- Avoiding interruptions (if visible)

Scoring:
- 9–10: Highly responsive and accurate
- 6–8: Generally attentive but occasionally off-target
- 1–5: Often off-topic or misinterprets questions

---

8. **Language Proficiency**  
_Assess command over language and grammar._

Evaluate based on:
- Correct grammar and sentence structure
- Fluent use of appropriate vocabulary
- Minimal grammatical or usage errors
- Professional tone and language

Scoring:
- 9–10: Fluent and grammatically correct
- 6–8: Minor issues but understandable
- 1–5: Frequent grammar or vocabulary errors

---

9. **Cultural / Behavioral Fit**  
_Assess alignment with workplace values and attitude._

Evaluate based on:
- Openness to learning and feedback
- Enthusiasm for the role
- Evidence of teamwork, adaptability, or leadership
- Avoids red flags (blaming others, entitlement)

Scoring:
- 9–10: Strong alignment and positive attitude
- 6–8: Acceptable fit but lacks strong evidence
- 1–5: Red flags or poor cultural alignment

---

10. **Time Management / Conciseness**  
_Assess ability to communicate efficiently._

Evaluate based on:
- Focused and concise responses
- Avoidance of unnecessary repetition
- Effective use of time in explanations
- Prioritization of key points

Scoring:
- 9–10: Crisp, relevant, and efficient communication
- 6–8: Some digressions but mostly focused
- 1–5: Frequently verbose or disorganized

---

Only return a **structured JSON array** of 10 metric evaluations in the format below:

```json
[
  {
    "metric": "Communication Skills",
    "score": "7/10",
    "reasoning": "The candidate spoke clearly and had good vocabulary, but used some filler words and occasionally lost structure in responses."
  },
  {
    "metric": "Confidence",
    "score": "8/10",
    "reasoning": "Answered questions assertively with minimal hesitation. Spoke in a composed tone throughout."
  }
]
```

Please analyze the interview video and provide the evaluation in the exact JSON format specified above."""