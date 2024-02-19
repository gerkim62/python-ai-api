import asyncio

from flask import Flask, abort, render_template
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

from constants import SUPPORTED_MODELS

from chatbots.bing_web import ask_bing_web
from chatbots.gemini_api import ask_gemini_api
from chatbots.gemini_web import ask_gemini_web
# from chatbots.chatgpt_web import ask_chatgpt_web
# from chatbots.claude_web import ask_claude_web

app = Flask(__name__)
CORS(app)
api = Api(app)


def validate_cookies(cookies):
    print(cookies)
    if not isinstance(cookies, list):
        raise ValueError("Cookies must be provided as a list")

    for cookie in cookies:
        if not isinstance(cookie, dict) or "name" not in cookie or "value" not in cookie:
            raise ValueError("Each cookie must be a dictionary with 'name' and 'value' keys")

    return cookies


ask_args = reqparse.RequestParser()
ask_args.add_argument("question", required=True, type=str, help="question string is required")
ask_args.add_argument("cookies", required=False, location="json", type=validate_cookies)  # Making cookies optional


class Ask(Resource):
    def post(self, model):
        args = ask_args.parse_args()
        print(args["question"])

        if model not in SUPPORTED_MODELS:
            abort(400, "Model not supported")

        if model == "bing_web":
            answer_coroutine = ask_bing_web(cookies=args["cookies"], question=args["question"])
            answer = asyncio.run(answer_coroutine)

            print(answer)
            return {
                "answer": answer,
                "model": model
            }
        elif model == "gemini_web":
            # For gemini_web, cookies are still required, so checking if cookies are provided
            if args["cookies"] is None:
                abort(400, "Cookies are required for this model")
            answer_coroutine = ask_gemini_web(question=args["question"], cookies=args['cookies'])
            answer = asyncio.run(answer_coroutine)
            return {
                "answer": answer,
                "model": model
            }

        elif model == "gemini_api":
            # For gemini_api, cookies are not required, so it can proceed without checking
            answer = ask_gemini_api(question=args["question"])
            return {
                "answer": answer,
                "model": model
            }


class SupportedModels(Resource):
    def get(self):
        return {"supported_models": SUPPORTED_MODELS}


api.add_resource(Ask, "/ask/<string:model>")
api.add_resource(SupportedModels, "/supported_models")

# Route to serve the homepage
@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
