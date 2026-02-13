from flask import json, render_template, jsonify, request
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
                "tags": ["NLP", "Classification", "Scikit-Learn"],
            },
            {
                "title": "Image Classifier",
                "description": "CNN-based image recognition",
                "demo_url": "/demo/image",
                "github_url": "#",
                "tags": ["CNN", "Computer Vision", "PyTorch"],
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
                    "description": "Trained on custon dataset",
                    "accuracy": "N/A",  # Load from metadata if available
                }
            )
        return render_template("gallery.html", models_info=models_info)

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

    # ===== API ENDPOINTS FOR PREDICTION =====
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

    # ===== AGENTS =====

    @app.route("/demo/agent/<agent_name>")
    def agent_demo(agent_name):
        """Interactive agent demo page"""
        agent = AGENTS.get(agent_name)
        if not agent:
            return "Agent not found", 404

        return render_template(
            "demos/agent_demo.html", agent=agent, title=f"{agent.name} Demo"
        )

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
                    "history": agent.conversation_history[-5:],  # last 5 messages
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
