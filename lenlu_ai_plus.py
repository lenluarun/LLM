"""
LENLU AI+ - Advanced LLM with User Training & Extended 4GB Knowledge
Integrates learning system with massive knowledge base
"""

import torch
import json
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from difflib import SequenceMatcher

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.text import Text
    from rich.align import Align
    from rich.table import Table
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from user_training_system import LENLULearner, UserTrainer

if HAS_RICH:
    console = Console()

class AIEnhancedLENLU:
    """LENLU with AI-like learning capabilities and 4GB+ knowledge"""
    
    def __init__(self, model_name="t5-base", use_learning=True):
        if HAS_RICH:
            banner = Panel(
                Text("🤖 LENLU LLM Edition 🤖\n", style="bold magenta") +
                Text("Advanced LLM with User Training\n", style="dim magenta") +
                Text("4GB+ Knowledge Base • LLM Learning System", style="cyan"),
                border_style="magenta"
            )
            console.print(banner)
        else:
            print("\n🤖 Initializing LENLU LLM...\n")
        
        # Load model
        if HAS_RICH:
            with Progress(SpinnerColumn(), TextColumn("[cyan]Loading model...[/cyan]"), transient=True) as progress:
                progress.add_task("model", total=None)
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            console.print("[green]✓[/green] [bold green]Model loaded![/bold green]")
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            print("✓ Model loaded")
        
        # Load knowledge bases
        if HAS_RICH:
            with Progress(SpinnerColumn(), TextColumn("[cyan]Loading knowledge bases...[/cyan]"), transient=True) as progress:
                progress.add_task("kb", total=None)
                self.extended_kb = self._load_extended_knowledge()
            console.print("[green]✓[/green] [bold green]Knowledge loaded![/bold green]")
        else:
            self.extended_kb = self._load_extended_knowledge()
            print("✓ Knowledge bases loaded")
        
        # Initialize learning system
        if use_learning:
            if HAS_RICH:
                with Progress(SpinnerColumn(), TextColumn("[cyan]Initializing learning system...[/cyan]"), transient=True) as progress:
                    progress.add_task("learn", total=None)
                    self.learner = LENLULearner()
                    self.trainer = UserTrainer(self.learner)
                console.print("[green]✓[/green] [bold green]Learning system ready![/bold green]")
            else:
                self.learner = LENLULearner()
                self.trainer = UserTrainer(self.learner)
                print("✓ Learning system initialized")
        else:
            self.learner = None
            self.trainer = None
        
        self.conversation_history = []
        self.max_history = 10
        
        # Load training data for similarity matching
        try:
            with open("training_data_expanded.json", 'r', encoding='utf-8') as f:
                self.training_data = json.load(f)
        except:
            try:
                with open("training_data.json", 'r', encoding='utf-8') as f:
                    self.training_data = json.load(f)
            except:
                self.training_data = []
        
        if HAS_RICH:
            ready_text = Text("✨ LENLU LLM Ready! Ask anything! ✨", style="bold cyan")
            console.print(Align.center(ready_text))
            console.print()
    
    def _load_extended_knowledge(self):
        """Load comprehensive knowledge base"""
        try:
            with open("knowledge_base_comprehensive.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _get_similarity_score(self, s1, s2):
        """Calculate similarity between two strings - keyword-based"""
        s1_lower = s1.lower()
        s2_lower = s2.lower()
        
        # Remove common question words
        stop_words = {'what', 'explain', 'describe', 'how', 'tell', 'show', 'define', 'is', 'are'}
        for word in stop_words:
            s1_lower = s1_lower.replace(word, '')
            s2_lower = s2_lower.replace(word, '')
        
        s1_lower = ' '.join(s1_lower.split())
        s2_lower = ' '.join(s2_lower.split())
        
        # Extract significant words (>2 chars)
        s1_words = set(w for w in s1_lower.split() if len(w) > 2)
        s2_words = set(w for w in s2_lower.split() if len(w) > 2)
        
        if not s1_words or not s2_words:
            return SequenceMatcher(None, s1_lower, s2_lower).ratio()
        
        # Jaccard similarity
        intersection = len(s1_words & s2_words)
        union = len(s1_words | s2_words)
        jaccard = intersection / union if union > 0 else 0
        
        # Character-level similarity as secondary metric
        char_sim = SequenceMatcher(None, s1_lower, s2_lower).ratio()
        
        # Weighted combination: 75% keyword, 25% character
        return (jaccard * 0.75) + (char_sim * 0.25)
    
    def _find_similar_qa(self, query, threshold=0.6):
        """Find similar Q&A from training data"""
        if not self.training_data:
            return None
        
        best_match = None
        best_score = threshold
        query_lower = query.lower()
        
        for qa in self.training_data:
            input_text = qa.get("input", "").lower()
            score = self._get_similarity_score(query_lower, input_text)
            
            if score > best_score:
                best_score = score
                best_match = qa
        
        return best_match
    
    def _extract_knowledge(self, query):
        """Extract knowledge from comprehensive knowledge base"""
        query_lower = query.lower()
        results = []
        
        for category, content in self.extended_kb.items():
            if isinstance(content, dict):
                for key, value in content.items():
                    if isinstance(value, str):
                        # Check if keywords match
                        keywords = query_lower.split()
                        if any(keyword in key.replace('_', ' ').lower() or 
                               keyword in value.lower() for keyword in keywords[:3]):
                            results.append(f"[{category.upper()}] {value[:150]}")
        
        return results[:3]
    
    def retrieve_intelligent_context(self, query):
        """Retrieve context using multi-source AI-enhanced retrieval"""
        context_parts = []
        query_lower = query.lower()
        
        # Priority 1: Check learned knowledge
        if self.learner:
            learned_answer = self.learner.get_improved_answer(query)
            if learned_answer:
                context_parts.append(f"[LEARNED] {learned_answer[:150]}")
        
        # Priority 2: Search training data
        similar_qa = self._find_similar_qa(query, threshold=0.5)
        if similar_qa:
            context_parts.append(f"[TRAINING] {similar_qa['target'][:150]}")
        
        # Priority 3: Extract from knowledge base
        kb_results = self._extract_knowledge(query)
        context_parts.extend(kb_results[:2])
        
        return "\n".join(context_parts[:4])
    
    def generate_response(self, prompt):
        """Generate response with learning integration"""
        if HAS_RICH:
            with Progress(SpinnerColumn(), TextColumn("[yellow]🧠 Generating...[/yellow]"), transient=True) as progress:
                progress.add_task("generate", total=None)
                response = self._compute_response(prompt)
        else:
            response = self._compute_response(prompt)
        
        # Learn from this interaction
        if self.learner:
            self.learner.learn_from_interaction(prompt, response, is_correct=True)
        
        # Store in history
        self.conversation_history.append((prompt, response))
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
        
        return response
    
    def _compute_response(self, prompt):
        """Compute response with 4-strategy hybrid approach"""
        # Strategy 1: Search training data (best quality)
        similar_qa = self._find_similar_qa(prompt, threshold=0.45)
        if similar_qa and self._get_similarity_score(prompt.lower(), similar_qa['input'].lower()) > 0.50:
            return similar_qa['target']
        
        # Strategy 2: Extract from knowledge base
        kb_answers = self._extract_knowledge(prompt)
        if kb_answers and len(kb_answers[0]) > 50:
            return kb_answers[0]
        
        # Strategy 3: Generate with T5
        context = self.retrieve_intelligent_context(prompt)
        enhanced_prompt = f"Q: {prompt}\nContext: {context}\nA:"
        
        try:
            inputs = self.tokenizer.encode(enhanced_prompt, return_tensors="pt", max_length=512, truncation=True)
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=200,
                    num_beams=3,
                    early_stopping=True,
                    temperature=0.5,
                    top_p=0.85,
                    do_sample=True,
                    no_repeat_ngram_size=3,
                    length_penalty=0.4
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
            if response and len(response) > 20:
                return response
        except:
            pass
        
        # Strategy 4: Category-based fallback
        query_category = self._categorize_query(prompt)
        return self._generate_fallback_response(prompt, query_category)
    
    def _categorize_query(self, query):
        """Categorize query by topic"""
        query_lower = query.lower()
        
        categories = {
            'dsa': ['algorithm', 'sort', 'binary', 'tree', 'graph', 'linked', 'heap', 'queue', 'stack', 'complexity'],
            'web': ['react', 'html', 'css', 'javascript', 'rest', 'api', 'frontend', 'websocket', 'node', 'express'],
            'database': ['sql', 'database', 'query', 'index', 'table', 'schema', 'nosql', 'mongodb', 'mysql', 'postgresql'],
            'devops': ['docker', 'kubernetes', 'ci/cd', 'jenkins', 'deployment', 'pipeline', 'git', 'terraform'],
            'ml': ['machine learning', 'neural', 'tensorflow', 'pytorch', 'model', 'training', 'dataset', 'algorithm'],
            'cloud': ['aws', 'gcp', 'azure', 'ec2', 's3', 'lambda', 'cloud', 'serverless'],
            'security': ['security', 'encryption', 'auth', 'jwt', 'ssl', 'xss', 'csrf', 'sql injection', 'vulnerable'],
            'programming': ['python', 'java', 'c++', 'javascript', 'code', 'function', 'class', 'variable', 'syntax'],
            'system': ['system', 'scale', 'performance', 'load', 'cache', 'distributed', 'design', 'architecture']
        }
        
        for category, keywords in categories.items():
            if any(keyword in query_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def _generate_fallback_response(self, query, category):
        """Generate fallback response based on category"""
        fallback_responses = {
            'dsa': f"For DSA question about '{query}': This typically involves algorithm analysis, time/space complexity, and implementation details. Please provide more specific context (e.g., problem name, constraint). Key areas: arrays, linked lists, trees, graphs, sorting, dynamic programming.",
            'web': f"For web development question '{query}': This relates to front-end or back-end technologies. Common topics: HTML/CSS, JavaScript, React/Vue, REST APIs, authentication. What specific technology are you asking about?",
            'database': f"For database question '{query}': This involves SQL, schema design, or query optimization. Consider: normalization levels, indexing strategy, query execution plan. Which database system are you using?",
            'devops': f"For DevOps question '{query}': This covers containerization, orchestration, CI/CD pipelines. Tools: Docker, Kubernetes, Jenkins. Let me know which tool or process you need help with.",
            'ml': f"For machine learning question '{query}': This involves model training, data preprocessing, or algorithms. Consider: supervised/unsupervised learning, overfitting prevention, performance metrics.",
            'cloud': f"For cloud question '{query}': Major platforms: AWS (EC2, S3, Lambda), GCP (Compute Engine, BigQuery), Azure. What service or use case?",
            'security': f"For security question '{query}': Key areas: authentication, encryption, injection attacks, API security. Best practice: defense in depth, principle of least privilege.",
            'programming': f"For programming question '{query}': Language-specific details needed. General concepts: OOP, functional programming, design patterns, testing, performance.",
            'system': f"For system design question '{query}': Consider: scalability, availability, consistency (CAP theorem), load balancing, caching, databases. Trade-offs matter.",
            'general': f"Question: {query}\n\nI have extensive knowledge about: DSA, Web Development, Databases, DevOps, Machine Learning, Cloud Platforms, Security, and System Design. Please refine your question or specify the topic!"
        }
        
        return fallback_responses.get(category, fallback_responses['general'])
    
    def display_welcome(self):
        """Show welcome with learning stats"""
        if HAS_RICH:
            import rich.box as box
            welcome_text = Text("Welcome to LENLU AI+\n", style="bold magenta")
            welcome_text.append("4GB+ Knowledge Base • AI Learning\n\n", style="dim magenta")
            welcome_text.append("@lenlu_arun & @lenluarun", style="bold cyan")
            
            panel = Panel(welcome_text, border_style="magenta", box=box.ROUNDED, padding=(1, 2))
            console.print(panel)
            
            # Show stats
            if self.learner:
                stats = self.learner.get_learning_stats()
                stats_text = f"📚 Learned Topics: {stats['topics_learned']} | 🔧 Corrections: {stats['corrections_applied']} | 💪 Confidence: {stats['confidence_level']:.0%}"
                console.print(f"\n[yellow]{stats_text}[/yellow]")
            
            commands = Text("\n💡 Commands:\n", style="bold cyan")
            commands.append("  • Ask any coding question\n", style="white")
            commands.append("  • 'train' - Enter training mode\n", style="cyan")
            commands.append("  • 'stats' - View learning stats\n", style="cyan")
            commands.append("  • 'history' - Conversation history\n", style="cyan")
            commands.append("  • 'quit' - Exit\n", style="red")
            console.print(commands)
        else:
            print("="*50)
            print("LENLU AI+ - Advanced Coding Assistant")
            print("4GB+ Knowledge Base • AI Learning System")
            print("="*50)
            print("\nPowered by @lenlu_arun & @lenluarun\n")
    
    def display_response(self, response):
        """Display formatted response"""
        if HAS_RICH:
            response_panel = Panel(
                Text(response, style="white"),
                title="[bold magenta]🤖 LENLU LLM[/bold magenta]",
                border_style="magenta",
                padding=(1, 2)
            )
            console.print(response_panel)
        else:
            print(f"\nLENLU: {response}\n")
    
    def show_stats(self):
        """Display learning statistics"""
        if not self.learner:
            if HAS_RICH:
                console.print("[yellow]Learning system not available[/yellow]")
            return
        
        stats = self.learner.get_learning_stats()
        
        if HAS_RICH:
            console.print("\n[bold magenta]📊 LENLU AI+ Learning Statistics:[/bold magenta]")
            console.print("━" * 60)
            console.print(f"  [cyan]Total Interactions:[/cyan] {stats['total_interactions']}")
            console.print(f"  [cyan]Topics Learned:[/cyan] {stats['topics_learned']}")
            console.print(f"  [cyan]Corrections Applied:[/cyan] {stats['corrections_applied']}")
            console.print(f"  [cyan]Overall Confidence:[/cyan] {stats['confidence_level']:.1%}")
            if stats['user_topics']:
                console.print(f"  [cyan]Custom Topics:[/cyan] {', '.join(stats['user_topics'][:5])}")
            console.print("━" * 60 + "\n")
        else:
            print(f"\nLENLU Learning Stats:")
            print(f"  Interactions: {stats['total_interactions']}")
            print(f"  Topics: {stats['topics_learned']}")
            print(f"  Confidence: {stats['confidence_level']:.1%}\n")
    
    def enter_training_mode(self):
        """Enter interactive training mode"""
        if not self.trainer:
            if HAS_RICH:
                console.print("[red]Training system not available[/red]")
            return
        
        self.trainer.enable_training_mode()
        self.trainer.show_stats()


def main():
    """Main interactive LENLU AI+ loop"""
    try:
        lenlu = AIEnhancedLENLU(model_name="t5-base", use_learning=True)
        lenlu.display_welcome()
        
        while True:
            try:
                if HAS_RICH:
                    user_input = console.input("[bold magenta]LENLU >>> [/bold magenta]").strip()
                else:
                    user_input = input("LENLU >>> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == "quit":
                    break
                elif user_input.lower() == "train":
                    lenlu.enter_training_mode()
                elif user_input.lower() == "stats":
                    lenlu.show_stats()
                elif user_input.lower() == "history":
                    if lenlu.conversation_history:
                        if HAS_RICH:
                            console.print("\n[cyan bold]📚 Conversation History:[/cyan bold]\n")
                            for i, (q, a) in enumerate(lenlu.conversation_history, 1):
                                console.print(f"[yellow]{i}. Q:[/yellow] {q}")
                                console.print(f"[magenta]   A:[/magenta] {a[:80]}...\n")
                        else:
                            for i, (q, a) in enumerate(lenlu.conversation_history, 1):
                                print(f"{i}. Q: {q}")
                                print(f"   A: {a[:80]}...")
                    else:
                        if HAS_RICH:
                            console.print("[yellow]No history yet[/yellow]")
                        else:
                            print("No history")
                else:
                    response = lenlu.generate_response(user_input)
                    lenlu.display_response(response)
            
            except KeyboardInterrupt:
                print("\n")
                break
    
    except Exception as e:
        if HAS_RICH:
            console.print(f"[bold red]❌ Error: {str(e)}[/bold red]")
        else:
            print(f"Error: {str(e)}")
    
    finally:
        if HAS_RICH:
            closing = Text("\n✨ LENLU LLM - Powered by @lenlu_arun & @lenluarun ✨\n", style="bold magenta")
            console.print(Align.center(closing))
        else:
            print("\n✨ LENLU LLM - Powered by @lenlu_arun & @lenluarun ✨\n")


if __name__ == "__main__":
    main()
