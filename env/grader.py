"""
Task-Specific Graders for OpenEnv
Each grader assigns a score between 0.0 and 1.0
"""


class EmailClassificationGrader:
    """Grades email classification accuracy and confidence with advanced scoring"""
    
    @staticmethod
    def grade(predicted_classification, predicted_confidence, correct_classification, confidence_hint=None):
        """
        Grade email classification with penalties, bonuses, and confidence calibration.
        
        Args:
            predicted_classification: Predicted class (important, spam, promotional)
            predicted_confidence: Confidence score (0.0-1.0)
            correct_classification: Ground truth classification
            confidence_hint: Optional expected confidence level for calibration
            
        Returns:
            dict with score, reasoning, and components breakdown
        """
        score = 0.0
        reasoning = []
        components = {}
        penalties = []
        bonuses = []
        
        # BASE SCORING: 60% for correct classification
        if predicted_classification == correct_classification:
            score += 0.6
            components["classification"] = 0.6
            reasoning.append("✓ Correct classification")
        else:
            components["classification"] = 0.0
            penalty = 0.25
            score -= penalty
            penalties.append(f"misclassification_penalty_{penalty}")
            reasoning.append(f"✗ Wrong classification: predicted {predicted_classification}, expected {correct_classification}")
        
        # CONFIDENCE CALIBRATION: 40% base + bonuses/penalties
        confidence_score = 0.0
        if predicted_classification == correct_classification:
            # Reward appropriate confidence for correct predictions
            if predicted_confidence >= 0.85:
                confidence_score = 0.4
                reasoning.append("✓ High confidence for correct prediction")
            elif predicted_confidence >= 0.65:
                confidence_score = 0.3
                reasoning.append("△ Moderate confidence for correct prediction")
            elif predicted_confidence >= 0.5:
                confidence_score = 0.15
                reasoning.append("✗ Low confidence in correct prediction (partial credit)")
            else:
                confidence_score = 0.0
                reasoning.append("✗ Very low confidence in correct prediction")
            
            # BONUS: Well-calibrated confidence
            if confidence_hint:
                calibration_diff = abs(predicted_confidence - confidence_hint)
                if calibration_diff <= 0.1:
                    bonus = 0.15
                    confidence_score += bonus
                    bonuses.append(f"calibration_bonus_{bonus}")
                    reasoning.append("🎯 Excellent confidence calibration (+15%)")
        else:
            # Penalize high confidence in wrong predictions
            if predicted_confidence >= 0.8:
                confidence_score = -0.2
                penalties.append("high_confidence_wrong_prediction")
                reasoning.append("✗ High confidence in wrong prediction (penalty)")
            elif predicted_confidence >= 0.5:
                confidence_score = -0.1
                penalties.append("moderate_confidence_wrong_prediction")
                reasoning.append("✗ Moderate confidence in wrong prediction")
            else:
                confidence_score = 0.0
                reasoning.append("✓ Low confidence saved from penalty")
        
        components["confidence_calibration"] = max(0, confidence_score)
        score += confidence_score
        
        final_score = max(0.0, min(1.0, score))
        
        return {
            "score": final_score,
            "reasoning": " | ".join(reasoning),
            "components": components,
            "penalties": penalties,
            "bonuses": bonuses
        }


class CodeReviewGrader:
    """Grades code review quality with advanced scoring"""
    
    @staticmethod
    def grade(predicted_issues, predicted_severity, correct_issues, correct_severity):
        """
        Grade code review with penalties for missed critical issues and bonuses for completeness.
        
        Args:
            predicted_issues: List of predicted issue types
            predicted_severity: Predicted severity level
            correct_issues: List of ground truth issues
            correct_severity: Ground truth severity
            
        Returns:
            dict with score, reasoning, and components
        """
        score = 0.0
        reasoning = []
        components = {}
        penalties = []
        bonuses = []
        
        # Convert to sets for comparison
        predicted_set = set(predicted_issues) if predicted_issues else set()
        correct_set = set(correct_issues) if correct_issues else set()
        
        # ISSUE DETECTION: 50% base + penalties/bonuses
        issue_score = 0.0
        if predicted_set == correct_set:
            issue_score = 0.5
            components["issue_detection"] = 0.5
            reasoning.append("✓ All issues correctly identified")
            
            # BONUS: Perfect detection
            if len(correct_set) >= 2:
                bonus = 0.1
                issue_score += bonus
                bonuses.append(f"perfect_detection_bonus_{bonus}")
                reasoning.append("🎯 Perfect detection of multiple issues (+10%)")
        else:
            # Calculate partial credit
            if predicted_set and correct_set:
                overlap = len(predicted_set & correct_set)
                false_positives = len(predicted_set - correct_set)
                missed = len(correct_set - predicted_set)
                total = len(predicted_set | correct_set)
                
                # Partial credit: 50% * (overlap / total)
                partial_score = (overlap / total) * 0.5
                issue_score += partial_score
                
                # PENALTIES
                if missed > 0 and "security" in correct_set and "security" not in predicted_set:
                    penalty = 0.15
                    issue_score -= penalty
                    penalties.append(f"missed_security_penalty_{penalty}")
                    reasoning.append(f"✗ Missed critical SECURITY issue (-15%)")
                
                if false_positives > 0:
                    false_positive_penalty = min(0.1, false_positives * 0.05)
                    issue_score -= false_positive_penalty
                    penalties.append(f"false_positives_penalty_{false_positive_penalty}")
                    reasoning.append(f"✗ {false_positives} false positive(s) reported")
                
                components["issue_detection"] = max(0, partial_score)
                reasoning.append(f"△ Detected {overlap}/{len(correct_set)} issues correctly")
            else:
                if not correct_set and not predicted_set:
                    issue_score = 0.5
                    components["issue_detection"] = 0.5
                    reasoning.append("✓ Correctly identified no issues")
                else:
                    components["issue_detection"] = 0.0
                    if len(correct_set) > 0:
                        penalty = 0.2
                        issue_score -= penalty
                        penalties.append(f"missed_all_issues_penalty_{penalty}")
                        reasoning.append(f"✗ Missed all {len(correct_set)} issues")
        
        score += issue_score
        
        # SEVERITY ASSESSMENT: 50% base + penalties/bonuses
        severity_score = 0.0
        severity_levels = {"critical": 4, "major": 3, "minor": 2, "none": 1}
        pred_level = severity_levels.get(predicted_severity, 0)
        correct_level = severity_levels.get(correct_severity, 0)
        
        if predicted_severity == correct_severity:
            severity_score = 0.5
            components["severity"] = 0.5
            reasoning.append("✓ Correct severity assessment")
            
            # BONUS: Correct critical severity
            if correct_severity == "critical":
                bonus = 0.1
                severity_score += bonus
                bonuses.append(f"critical_severity_bonus_{bonus}")
                reasoning.append("🎯 Correctly identified CRITICAL severity (+10%)")
        else:
            diff = abs(pred_level - correct_level)
            if diff <= 1:
                severity_score = 0.25
                components["severity"] = 0.25
                reasoning.append(f"△ Severity off by 1 level: predicted {predicted_severity}")
            else:
                penalty = 0.2
                severity_score = -penalty
                components["severity"] = 0.0
                penalties.append(f"wrong_severity_penalty_{penalty}")
                reasoning.append(f"✗ Severity mismatch: predicted {predicted_severity}, expected {correct_severity}")
        
        score += severity_score
        
        final_score = max(0.0, min(1.0, score))
        
        return {
            "score": final_score,
            "reasoning": " | ".join(reasoning),
            "components": components,
            "penalties": penalties,
            "bonuses": bonuses
        }


class SupportRoutingGrader:
    """Grades support ticket routing decisions with advanced scoring"""
    
    @staticmethod
    def grade(predicted_action, correct_action):
        """
        Grade support routing decision with penalties for misrouting and bonuses for context awareness.
        
        Args:
            predicted_action: dict with department, priority, response_type, tone, etc.
            correct_action: dict with ground truth values
            
        Returns:
            dict with score, reasoning, and components
        """
        score = 0.0
        reasoning = []
        components = {}
        penalties = []
        bonuses = []
        
        is_vip = predicted_action.get("is_vip", False)
        sentiment = predicted_action.get("sentiment", "neutral")
        customer_type = predicted_action.get("customer_type", "standard")
        urgency = predicted_action.get("urgency", "normal")
        
        # DEPARTMENT ROUTING: 38% base (adjusted from 35 to accommodate bonuses)
        dept_score = 0.0
        if predicted_action.get("department") == correct_action.get("department"):
            dept_score = 0.38
            components["department"] = 0.38
            reasoning.append("✓ Correct department")
            
            # BONUS: Correct escalation for VIP
            if is_vip and predicted_action.get("department") == "escalation":
                bonus = 0.08
                dept_score += bonus
                bonuses.append(f"vip_escalation_bonus_{bonus}")
                reasoning.append("🎯 VIP correctly escalated (+8%)")
        else:
            # PENALTY: Wrong department routing
            penalty = 0.25
            dept_score -= penalty
            components["department"] = 0.0
            penalties.append(f"wrong_department_penalty_{penalty}")
            reasoning.append(f"✗ Wrong department: {predicted_action.get('department')} vs {correct_action.get('department')}")
            
            # SEVERE PENALTY: Wrong escalation
            if correct_action.get("department") == "escalation" and predicted_action.get("department") != "escalation":
                severe_penalty = 0.15
                dept_score -= severe_penalty
                penalties.append(f"missed_escalation_severe_penalty_{severe_penalty}")
                reasoning.append(f"✗ CRITICAL: Missed escalation case (-15%)")
        
        score += dept_score
        
        # PRIORITY ASSESSMENT: 22% base (adjusted from 25%)
        priority_score = 0.0
        priority_levels = {"low": 1, "medium": 2, "high": 3, "urgent": 4}
        pred_level = priority_levels.get(predicted_action.get("priority"), 0)
        correct_level = priority_levels.get(correct_action.get("priority"), 0)
        
        if predicted_action.get("priority") == correct_action.get("priority"):
            priority_score = 0.22
            components["priority"] = 0.22
            reasoning.append("✓ Correct priority")
            
            # BONUS: Correct urgency handling
            if urgency == "critical" and predicted_action.get("priority") == "urgent":
                bonus = 0.08
                priority_score += bonus
                bonuses.append(f"critical_priority_bonus_{bonus}")
                reasoning.append("🎯 Critical issue prioritized correctly (+8%)")
        else:
            diff = abs(pred_level - correct_level)
            if diff == 1:
                priority_score = 0.11
                components["priority"] = 0.11
                reasoning.append(f"△ Priority off by 1 level")
            else:
                penalty = 0.15
                priority_score = -penalty
                components["priority"] = 0.0
                penalties.append(f"wrong_priority_penalty_{penalty}")
                reasoning.append(f"✗ Wrong priority")
        
        score += priority_score
        
        # RESPONSE TYPE: 22% base (adjusted from 20%)
        response_score = 0.0
        if predicted_action.get("response_type") == correct_action.get("response_type"):
            response_score = 0.22
            components["response_type"] = 0.22
            reason_type = predicted_action.get("response_type")
            if reason_type == "escalate":
                reasoning.append("✓ Correct response type (escalation)")
            else:
                reasoning.append("✓ Correct response type")
        else:
            penalty = 0.12
            response_score = -penalty
            components["response_type"] = 0.0
            penalties.append(f"wrong_response_type_penalty_{penalty}")
            reasoning.append(f"✗ Wrong response type: {predicted_action.get('response_type')}")
        
        score += response_score
        
        # TONE APPROPRIATENESS: 18% base (adjusted from 20%)
        tone_score = 0.0
        if predicted_action.get("tone") == correct_action.get("tone"):
            tone_score = 0.18
            components["tone"] = 0.18
            reasoning.append("✓ Appropriate tone")
            
            # BONUS: Empathetic tone for frustrated customers
            if sentiment in ["angry", "frustrated"] and predicted_action.get("tone") == "empathetic":
                bonus = 0.1
                tone_score += bonus
                bonuses.append(f"empathetic_for_frustrated_bonus_{bonus}")
                reasoning.append("🎯 Excellent empathy for frustrated customer (+10%)")
        else:
            # Context-aware tone penalties
            penalty = 0.0
            if sentiment in ["angry", "frustrated"] and predicted_action.get("tone") != "empathetic":
                penalty = 0.15
                penalties.append("empathy_gap_penalty")
                reasoning.append("✗ Should be empathetic for frustrated customer (-15%)")
            elif customer_type == "premium" and is_vip:
                if predicted_action.get("tone") not in ["formal", "urgent"]:
                    penalty = 0.12
                    penalties.append("vip_tone_penalty")
                    reasoning.append("✗ VIP premium customers need formal/urgent tone (-12%)")
            else:
                penalty = 0.1
                penalties.append("tone_mismatch_penalty")
                reasoning.append(f"✗ Tone mismatch: {predicted_action.get('tone')}")
            
            tone_score = -penalty
            components["tone"] = 0.0
        
        score += tone_score
        
        final_score = max(0.0, min(1.0, score))
        
        return {
            "score": final_score,
            "reasoning": " | ".join(reasoning),
            "components": components,
            "penalties": penalties,
            "bonuses": bonuses
        }


def compute_score(data):
    """
    Generic scoring function for any task with full context passed.
    
    Args:
        data: dict with task_id, predicted, correct, and optional context fields
        
    Returns:
        dict with score, reasoning, components, penalties, and bonuses
    """
    task_id = data.get("task_id")
    predicted = data.get("predicted", {})
    correct = data.get("correct", {})
    
    if task_id == "email_classification":
        return EmailClassificationGrader.grade(
            predicted.get("classification"),
            predicted.get("confidence", 0.5),
            correct.get("classification"),
            confidence_hint=correct.get("confidence_hint")
        )
    
    elif task_id == "code_review":
        return CodeReviewGrader.grade(
            predicted.get("issue_types", []),
            predicted.get("severity", "none"),
            correct.get("issue_types", []),
            correct.get("severity", "none")
        )
    
    elif task_id == "support_routing":
        # Pass full context to grader
        predicted["sentiment"] = data.get("sentiment", "neutral")
        predicted["customer_type"] = data.get("customer_type", "standard")
        predicted["is_vip"] = data.get("is_vip", False)
        predicted["urgency"] = data.get("urgency", "normal")
        return SupportRoutingGrader.grade(predicted, correct)
    
    else:
        return {
            "score": 0.0,
            "reasoning": f"Unknown task_id: {task_id}",
            "components": {},
            "penalties": [],
            "bonuses": []
        }

