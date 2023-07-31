from flask import jsonify, request

from app import app
from app.auth.jwt_auth import token_required_fact
from app.env import *
from app.llm import LLMSession


@app.route('/chatbot-inference', methods=['POST'])
@token_required_fact(FRONTEND_TOKEN_SECRET_KEY, FRONTEND_TOKEN_SECRET)
def chatbot_inference():
    request_data = request.get_json()
    message = request_data['message']
    session_id = request_data['session_id']

    llm_session = LLMSession(session_id)
    result = llm_session.query(message)

    return (
        jsonify(
            {'chatbot_response': result['answer'], 'source_urls': result['source_urls']}
        ),
        201,
    )


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'message': 'Up and running!'}), 200
