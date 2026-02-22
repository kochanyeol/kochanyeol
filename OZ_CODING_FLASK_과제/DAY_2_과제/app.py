from flask import Flask
from flask_smorest import Api
from api import book_blp

app = Flask(__name__)

app.config('API_TITLE') = 'Book API'
# 문서의 타이틀(제목)
app.config('API VERSION') = 'v1'
# API 문서의 버전
app.config('OPENAPI_VERSION') = '3.0.2'
# https://swagger.io/specification/ 최신스펙 확인 가능
# 추가로 flask_smorest는 openapi 3.0.~ 버전을 안정적으로 지원한다고 합니다.
app.config('OPENAPI_URL_PREFIX') = '/'
app.config('OPENAPI_SWAGGER_UI_PATH') = '/swagger-ui'
# swagger UI에 접속 할 경로
app.config('OPENAPI_SWAGGER_UI_URL') = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
# swagger UI의 역할은 문서 형태로 내려온 openapi의 문서를 html,js로 화면에 렌더링하는 역할

api = Api(app)
api.register_blueprint(book_blp)


if __name__ == '__main__':
    app.run(debug=True)