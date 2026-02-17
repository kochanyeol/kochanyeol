from marshmallow import Schema, fields


class BookSchema(Schema):
    # 변수명 제외 전부 Marshmallow 정의된 속성
    id = fields.Int(dump_only=True)
    # marshmallow에서 정수형 필드생성
    # dump_only=True는 get(출력)만 포함.
    title = fields.String(required=True)
    author = fields.String(required=True)
    # 처음에 생성하는 post나 기존에 있는 데이터를 수정하는 put을
    # 사용할 때 title, author가 없거나 필드가 문자열이 아닐 때 에러 발생