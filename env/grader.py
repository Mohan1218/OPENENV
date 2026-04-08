"""
Task-Specific Graders for OpenEnv
Each grader assigns a score between 0.0 and 1.0
"""


class EmailClassificationGrader:
    """Grades email classification accuracy and confidence"""
    
    @staticmethod
    def grade(predicted_classification, predicted_confidence, correct_classification):
        """
        Grade email classification.
        
        Args:
            predicted_classification: Predicted class (important, spam, promotional)
            predicted_confidence: Confidence score (0.0-1.0)
            correct_classification: Ground truth classification
            
        Returns:
            dict with score and reasoning
        """
        score = 0.0
        reasoning = []
        
        # 60% for correct classification
        if predicted_classification == correct_classification:
            score += 0.6
            reasoning.append("✓ Correct classification")
        else:
            reasoning.append(f"✗ Wrong classification: predicted {predicted_classification}, expected {correct_classification}")
        
        # 40% for confidence calibration
        if predicted_classification == correct_classification:
            if predicted_confidence >= 0.8:
                score += 0.4
                reasoning.append("✓ High confidence for correct prediction")
            elif predicted_confidence >= 0.6:
                score += 0.3
                reasoning.append("△ Moderate confidence for correct prediction")
            else:
                score += 0.1
                reasoning.append("✗ Low confidence in correct prediction")
        else:
            # Penalize high confidence in wrong prediction
            if predicted_confidence >= 0.8:
                score -= 0.2
                reasoning.append("✗ High confidence in wrong prediction (penalty)")
        
        return {
            "score": max(0.0, min(1.0, score)),
            "reasoning": " | ".join(reasoning)
        }


class CodeReviewGrader:
    """Grades code review quality"""
    
    @staticmethod
    def grade(predicted_issues, predicted_severity, correct_issues, correct_severity):
        """
        Grade code review.
        
        Args:
            predicted_issues: List of predicted issue types
            predicted_severity: Predicted severity level
            correct_issues: List of ground truth issues
            correct_severity: Ground truth severity
            
        Returns:
            dict with score and reasoning
        """
        score = 0.0
        reasoning = []
        
        # Convert to sets for comparison
        predicted_set = set(predicted_issues) if predicted_issues else set()
        correct_set = set(correct_issues) if correct_issues else set()
        
        # 50% for issue detection
        if predicted_set == correct_set:
            score += 0.5
            reasoning.append("✓ All issues correctly identified")
        else:
            # Partial credit for detecting some issues
            if predicted_set and correct_set:
                overlap = len(predicted_set & correct_set)
                total = len(predicted_set | correct_set)
                partial_score = (overlap / total) * 0.5
                score += partial_score
                reasoning.append(f"△ Detected {overlap}/{len(correct_set)} issues correctly")
            else:
                if not correct_set and not predicted_set:
                    score += 0.5
                    reasoning.append("✓ Correctly identified no issues")
                else:
                    reasoning.append(f"✗ Issue detection mismatch")
        
        # 50% for severity assessment
        if predicted_severity == correct_severity:
            score += 0.5
            reasoning.append("✓ Correct severity assessment")
        else:
            severity_levels = {"critical": 4, "major": 3, "minor": 2, "none": 1}
            pred_level = severity_levels.get(predicted_severity, 0)
            correct_level = severity_levels.get(correct_severity, 0)
            
            # Partial credit for being close
            diff = abs(pred_level - correct_level)
            if diff <= 1:
                score += 0.25
                reasoning.append(f"△ Severity off by 1 level: predicted {predicted_severity}")
            else:
                reasoning.append(f"✗ Severity mismatch: predicted {predicted_severity}, expected {correct_severity}")
        
        return {
            "score": max(0.0, min(1.0, score)),
            "reasoning": " | ".join(reasoning)
        }


class SupportRoutingGrader:
    """Grades support ticket routing decisions"""
    
    @staticmethod
    def grade(predicted_action, correct_action):
        """
        Grade support routing decision.
        
        Args:
            predicted_action: dict with department, priority, response_type, tone
            correct_action: dict with ground truth values
            
        Returns:
            dict with score and reasoning
        """
        score = 0.0
        reasoning = []
        
        # 35% for department routing
        if predicted_action.get("department") == correct_action.get("department"):
            score += 0.35
            reasoning.append("✓ Correct department")
        else:
            score -= 0.2
            reasoning.append(f"✗ Wrong department: {predicted_action.get('department')} vs {correct_action.get('department')}")
        
        # 25% for priority assessment
        if predicted_action.get("priority") == correct_action.get("priority"):
            score += 0.25
            reasoning.append("✓ Correct priority")
        else:
            # Partial credit for being close
            priority_levels = {"low": 1, "medium": 2, "high": 3, "urgent": 4}
            pred_level = priority_levels.get(predicted_action.get("priority"), 0)
            correct_level = priority_levels.get(correct_action.get("priority"), 0)
            
            diff = abs(pred_level - correct_level)
            if diff == 1:
                score += 0.125
                reasoning.append(f"△ Priority off by 1 level")
            else:
                score -= 0.15
                reasoning.append(f"✗ Wrong priority")
        
        # 20% for response type
        if predicted_action.get("response_type") == correct_action.get("response_type"):
            score += 0.2
            reasoning.append("✓ Correct response type")
        else:
            reasoning.append(f"✗ Wrong response type: {predicted_action.get('response_type')}")
        
        # 20% for tone appropriateness
        sentiment = predicted_action.get("sentiment", "neutral")
        customer_type = predicted_action.get("customer_type", "free")
        
        if predicted_action.get("tone") == correct_action.get("tone"):
            score += 0.2
            reasoning.append("✓ Appropriate tone")
        else:
            # Tone penalties based on context
            if sentiment in ["angry", "frustrated"] and predicted_action.get("tone") != "empathetic":
                score -= 0.15
                reasoning.append("✗ Should be empathetic for frustrated customer")
            elif customer_type == "premium" and predicted_action.get("tone") != "formal":
                score -= 0.1
                reasoning.append("△ Premium customers prefer formal tone")
            else:
                reasoning.append(f"✗ Tone mismatch: {predicted_action.get('tone')}")
        
        return {
            "score": max(0.0, min(1.0, score)),
            "reasoning": " | ".join(reasoning)
        }


def compute_score(data):
    """
    Generic scoring function for any task.
    
    Args:
        data: dict with task_id, predicted, and correct fields
        
    Returns:
        dict with score and reasoning
    """
    task_id = data.get("task_id")
    predicted = data.get("predicted", {})
    correct = data.get("correct", {})
    
    if task_id == "email_classification":
        return EmailClassificationGrader.grade(
            predicted.get("classification"),
            predicted.get("confidence", 0.5),
            correct.get("classification")
        )
    
    elif task_id == "code_review":
        return CodeReviewGrader.grade(
            predicted.get("issue_types", []),
            predicted.get("severity", "none"),
            correct.get("issue_types", []),
            correct.get("severity", "none")
        )
    
    elif task_id == "support_routing":
        # Pass additional context to grader
        predicted["sentiment"] = data.get("sentiment")
        predicted["customer_type"] = data.get("customer_type")
        return SupportRoutingGrader.grade(predicted, correct)
    
    else:
        return {
            "score": 0.0,
            "reasoning": f"Unknown task_id: {task_id}"
        }

