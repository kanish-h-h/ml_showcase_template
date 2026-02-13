from flask import render_template, jsonify, request
from .models.model_loader import SentimentClassifier, ModelManager
from .agents.agent_system import AGENTS


def init_app(app):
    # ===== PORTFOLIO PAGES =====
    @app.route("/")
    def index():
        """Homepage - showcase all projects"""
        projects = [
            {
                "title": "Sentiment Analysis",
                "description": "Classifies text sentiment with 92% accuracy",
                "demo_url": "/demo/sentiment",
                "github_url": "#",
                "tags": ["NLP", "Classification", "Scikit-learn"],
            },
            {
                "title": "Image Classifier",
                "description": "CNN-based image recognition",
                "demo_url": "/demo/image",
                "github_url": "#",
                "tags": ["Computer Vision", "CNN", "PyTorch"],
            },
        ]
        return render_template("index.html", projects=projects)

    @app.route("/gallery")
    def gallery():
        """Visual showcase of all models"""
        models_info = []
        for model_name in ModelManager.list_available_models():
            models_info.append(
                {
                    "name": model_name,
                    "description": "Trained on custom dataset",
                    "accuracy": "N/A",
                }
            )
        return render_template("gallery.html", models=models_info)

    # ===== NEW: API Documentation Page =====
    @app.route("/api_docs")
    def api_docs_page():  # Route name must match url_for()
        """API documentation page"""
        return render_template("api_docs.html")

    # ===== ML DEMO PAGES =====
    @app.route("/demo/sentiment")
    def sentiment_demo():
        """Interactive sentiment analysis demo"""
        return render_template(
            "demos/sentiment_demo.html", title="Sentiment Analysis Demo"
        )

    @app.route("/demo/image")
    def image_demo():
        """Image classification demo"""
        return render_template("demos/image_demo.html", title="Image Classifier Demo")

    # ===== AGENT DEMO PAGES =====
    @app.route("/demo/agent/<agent_name>")
    def agent_demo(agent_name):
        """Interactive agent demo page"""
        agent = AGENTS.get(agent_name)
        if not agent:
            return "Agent not found", 404

        return render_template(
            "demos/agent_demo.html", agent=agent, title=f"{agent.name} Demo"
        )

    # ===== API ENDPOINTS FOR PREDICTIONS =====
    @app.route("/api/predict/sentiment", methods=["POST"])
    def predict_sentiment():
        """API endpoint for sentiment prediction"""
        try:
            data = request.get_json()
            text = data.get("text", "")

            if not text:
                return jsonify({"error": "No text provided"}), 400

            # Load model and predict
            classifier = SentimentClassifier()
            result = classifier.predict(text)

            return jsonify({"success": True, "prediction": result})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/models")
    def list_models():
        """List all available models"""
        return jsonify({"models": ModelManager.list_available_models()})

    # ===== AGENT API ENDPOINTS =====
    @app.route("/api/agent/<agent_name>/chat", methods=["POST"])
    def agent_chat(agent_name):
        """API endpoint for agent interaction"""
        agent = AGENTS.get(agent_name)
        if not agent:
            return jsonify({"error": "Agent not found"}), 404

        try:
            data = request.get_json()
            user_message = data.get("message", "")

            if not user_message:
                return jsonify({"error": "No message provided"}), 400

            # Process with agent
            response = agent.process(user_message)

            return jsonify(
                {
                    "success": True,
                    "response": response,
                    "history": agent.conversation_history[-5:],  # Last 5 messages
                }
            )

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/agents")
    def list_agents():
        """List all available agents"""
        return jsonify(
            {
                "agents": [
                    {
                        "id": agent_id,
                        "name": agent.name,
                        "description": agent.description,
                    }
                    for agent_id, agent in AGENTS.items()
                ]
            }
        )
