"""
LENLU Learning System - User Training & Knowledge Persistence
Allows LENLU to learn from user interactions and improve over time
"""

import json
import os
from pathlib import Path
from datetime import datetime

class LENLULearner:
    """AI-like learning system that builds knowledge from user interactions"""
    
    def __init__(self, learned_kb_file="user_learned_knowledge.json", 
                 conversation_log="conversation_log.json"):
        self.learned_kb_file = learned_kb_file
        self.conversation_log_file = conversation_log
        self.learned_knowledge = self._load_learned_knowledge()
        self.conversation_history = self._load_conversations()
        self.learning_enabled = True
        
    def _load_learned_knowledge(self):
        """Load previously learned knowledge"""
        if Path(self.learned_kb_file).exists():
            with open(self.learned_kb_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "user_defined_topics": {},
            "improved_answers": {},
            "common_questions": {},
            "user_corrections": {},
            "learning_stats": {
                "total_interactions": 0,
                "topics_learned": 0,
                "corrections_applied": 0
            }
        }
    
    def _load_conversations(self):
        """Load conversation history for learning"""
        if Path(self.conversation_log_file).exists():
            with open(self.conversation_log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "conversations": [],
            "session_count": 0,
            "total_messages": 0
        }
    
    def save_learned_knowledge(self):
        """Persist learned knowledge to file"""
        with open(self.learned_kb_file, 'w', encoding='utf-8') as f:
            json.dump(self.learned_knowledge, f, indent=2, ensure_ascii=False)
    
    def save_conversations(self):
        """Persist conversation history"""
        with open(self.conversation_log_file, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
    
    def learn_from_interaction(self, question, answer, user_feedback=None, is_correct=True):
        """Learn from Q&A pair - AI improves itself"""
        if not self.learning_enabled:
            return
        
        # Store the interaction
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "feedback": user_feedback,
            "marked_correct": is_correct
        }
        
        # Add to conversation history
        self.conversation_history["conversations"].append(interaction)
        self.conversation_history["total_messages"] += 1
        
        # Extract topic
        topic = self._extract_topic(question)
        
        # Build knowledge from similarity
        question_hash = self._get_hash(question)
        
        if question_hash not in self.learned_knowledge["common_questions"]:
            self.learned_knowledge["common_questions"][question_hash] = {
                "question": question,
                "count": 0,
                "best_answer": answer,
                "variations": []
            }
        
        self.learned_knowledge["common_questions"][question_hash]["count"] += 1
        
        # Store topic knowledge
        if topic not in self.learned_knowledge["user_defined_topics"]:
            self.learned_knowledge["user_defined_topics"][topic] = {
                "created": datetime.now().isoformat(),
                "q_and_a": [],
                "confidence": 0.5
            }
        
        self.learned_knowledge["user_defined_topics"][topic]["q_and_a"].append({
            "question": question,
            "answer": answer,
            "is_verified": is_correct
        })
        
        # Increase confidence if marked correct
        if is_correct:
            current_conf = self.learned_knowledge["user_defined_topics"][topic]["confidence"]
            self.learned_knowledge["user_defined_topics"][topic]["confidence"] = min(1.0, current_conf + 0.1)
        
        # Update stats
        self.learned_knowledge["learning_stats"]["total_interactions"] += 1
        self.learned_knowledge["learning_stats"]["topics_learned"] = len(
            self.learned_knowledge["user_defined_topics"]
        )
        
        self.save_learned_knowledge()
        self.save_conversations()
    
    def add_user_correction(self, question, wrong_answer, corrected_answer):
        """User corrects LENLU - AI learns the correction"""
        correction = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "was": wrong_answer,
            "should_be": corrected_answer,
            "applied": False
        }
        
        topic = self._extract_topic(question)
        
        if topic not in self.learned_knowledge["user_corrections"]:
            self.learned_knowledge["user_corrections"][topic] = []
        
        self.learned_knowledge["user_corrections"][topic].append(correction)
        
        # Apply correction immediately
        question_hash = self._get_hash(question)
        if question_hash in self.learned_knowledge["common_questions"]:
            self.learned_knowledge["common_questions"][question_hash]["best_answer"] = corrected_answer
        
        self.learned_knowledge["learning_stats"]["corrections_applied"] += 1
        
        self.save_learned_knowledge()
    
    def get_improved_answer(self, question):
        """Retrieve improved answer learned from user"""
        question_hash = self._get_hash(question)
        
        if question_hash in self.learned_knowledge["common_questions"]:
            return self.learned_knowledge["common_questions"][question_hash]["best_answer"]
        
        # Try topic-based retrieval
        topic = self._extract_topic(question)
        if topic in self.learned_knowledge["user_defined_topics"]:
            answers = self.learned_knowledge["user_defined_topics"][topic]["q_and_a"]
            if answers:
                return answers[-1]["answer"]  # Return most recent
        
        return None
    
    def add_user_topic(self, topic_name, description, content):
        """User adds custom topic for LENLU to learn"""
        self.learned_knowledge["user_defined_topics"][topic_name] = {
            "created": datetime.now().isoformat(),
            "description": description,
            "content": content,
            "q_and_a": [],
            "confidence": 0.8
        }
        
        self.learned_knowledge["learning_stats"]["topics_learned"] = len(
            self.learned_knowledge["user_defined_topics"]
        )
        
        self.save_learned_knowledge()
    
    def get_learning_stats(self):
        """Get AI learning progress statistics"""
        return {
            "total_interactions": self.learned_knowledge["learning_stats"]["total_interactions"],
            "topics_learned": self.learned_knowledge["learning_stats"]["topics_learned"],
            "corrections_applied": self.learned_knowledge["learning_stats"]["corrections_applied"],
            "user_topics": list(self.learned_knowledge["user_defined_topics"].keys()),
            "confidence_level": self._calculate_overall_confidence()
        }
    
    def _calculate_overall_confidence(self):
        """Calculate overall AI knowledge confidence"""
        if not self.learned_knowledge["user_defined_topics"]:
            return 0.5
        
        confidences = [
            topic.get("confidence", 0.5) 
            for topic in self.learned_knowledge["user_defined_topics"].values()
        ]
        return sum(confidences) / len(confidences) if confidences else 0.5
    
    def _extract_topic(self, question):
        """Extract topic from question"""
        key_topics = {
            "machine learning": ["ml", "machine learning", "neural", "deep learning", "model", "training"],
            "system_design": ["system", "design", "scale", "database", "load", "cache"],
            "devops": ["docker", "kubernetes", "ci/cd", "deployment", "devops", "container"],
            "web_development": ["web", "frontend", "backend", "react", "javascript", "api"],
            "dsa": ["algorithm", "data structure", "array", "tree", "graph", "sorting", "complexity"],
            "database": ["sql", "database", "query", "nosql", "mongodb", "postgres"],
            "cloud": ["cloud", "aws", "gcp", "azure", "lambda", "ec2"]
        }
        
        q_lower = question.lower()
        for topic, keywords in key_topics.items():
            if any(kw in q_lower for kw in keywords):
                return topic
        
        return "general"
    
    def _get_hash(self, text):
        """Simple hash for question similarity"""
        # Remove common words and get signature
        words = text.lower().split()
        filtered = [w for w in words if len(w) > 3]
        return "_".join(sorted(filtered)[:5])  # Hash of top 5 words


class UserTrainer:
    """Allows users to actively train LENLU"""
    
    def __init__(self, learner=None):
        self.learner = learner or LENLULearner()
        self.training_mode = False
    
    def enable_training_mode(self):
        """Enable interactive training mode"""
        self.training_mode = True
        print("\n🎓 LENLU Training Mode Activated!")
        print("━" * 50)
        print("You can now teach LENLU:")
        print("  • 'add_topic <name>' - Add new topic")
        print("  • 'add_qa' - Add question & answer")
        print("  • 'correct' - Correct last answer")
        print("  • 'review' - See what LENLU learned")
        print("  • 'stats' - View learning statistics")
        print("  • 'exit_training' - Exit training mode")
        print("━" * 50 + "\n")
    
    def add_qa_pair(self, question, answer):
        """User adds Q&A pair"""
        self.learner.learn_from_interaction(question, answer, is_correct=True)
        print(f"✓ Added to LENLU's knowledge!")
    
    def add_topic(self, topic_name, description, content):
        """User adds new topic to LENLU"""
        self.learner.add_user_topic(topic_name, description, content)
        print(f"✓ Topic '{topic_name}' added to LENLU!")
    
    def correct_answer(self, question, wrong_answer, correct_answer):
        """User corrects LENLU"""
        self.learner.add_user_correction(question, wrong_answer, correct_answer)
        print(f"✓ Correction saved! LENLU will improve next time.")
    
    def show_stats(self):
        """Display learning statistics"""
        stats = self.learner.get_learning_stats()
        print("\n📊 LENLU Learning Statistics:")
        print("━" * 50)
        print(f"  Total Interactions: {stats['total_interactions']}")
        print(f"  Topics Learned: {stats['topics_learned']}")
        print(f"  Corrections Applied: {stats['corrections_applied']}")
        print(f"  Overall Confidence: {stats['confidence_level']:.1%}")
        if stats['user_topics']:
            print(f"  Custom Topics: {', '.join(stats['user_topics'][:5])}")
        print("━" * 50 + "\n")
    
    def export_learned_knowledge(self, filename="lenlu_learned_export.json"):
        """Export learned knowledge for backup"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.learner.learned_knowledge, f, indent=2, ensure_ascii=False)
        print(f"✓ Knowledge exported to {filename}")


def create_training_interface():
    """Create interactive training interface"""
    learner = LENLULearner()
    trainer = UserTrainer(learner)
    
    print("\n" + "="*60)
    print("🤖 LENLU AI Learning System Initialized")
    print("="*60)
    print("\n✨ Features:")
    print("  • Learn from user corrections")
    print("  • Build custom topics")
    print("  • Add Q&A pairs")
    print("  • Track learning progress")
    print("  • Persist knowledge across sessions")
    print("="*60 + "\n")
    
    return learner, trainer


if __name__ == "__main__":
    learner, trainer = create_training_interface()
    
    # Example: Teaching LENLU
    print("📚 Example Learning Session:")
    print("-" * 60)
    
    learner.learn_from_interaction(
        "What is a bloom filter?",
        "A bloom filter is a probabilistic data structure for efficient membership testing.",
        is_correct=True
    )
    
    learner.add_user_topic(
        "Bloom Filters",
        "Probabilistic data structures",
        "Bloom filters use multiple hash functions to check if element is in set..."
    )
    
    stats = learner.get_learning_stats()
    print(f"\n✓ Learning Stats: {stats}")
    print(f"✓ Topics Known: {stats['topics_learned']}")
    print(f"✓ Confidence: {stats['confidence_level']:.1%}")
