from pydantic import BaseModel, Field, SecretStr 

# jsonExample = {
#     "User":{
#         "name": "김태영",
#         "nickname": "버블",
#         "id": "kty0904kty",
#         "password": "qwer1234"
#     }
# }
# Field(...)은 꼭 필요한 값임을 나타냄.
# <Class'ellipsis'>
# 사용자 스키마

class UserSchema(BaseModel):
    name: str = Field(..., description="사용자의 이름")
    nickname: str = Field(..., description="사용자의 닉네임")
    id: str = Field(..., description="사용자의 ID")
    password: SecretStr = Field(..., description="사용자의 비밀번호")


class RequestUserSchema(BaseModel):
    User: UserSchema = Field(..., description="사용자 정보")

# jsonExample = {
#     "Manager":{
#         "company": "삼둘샵",
#         "name": "김태영",
#         "phone": "010-1234-5678"
#         "id": "kty0904kty",
#         "password": "qwer1234"
#     }
# }

# 기업회원 스키마
class ManagerSchema(BaseModel):
    company: str = Field(..., description="기업의 이름")
    name: str = Field(..., description="담당자의 이름")
    phone: SecretStr = Field(..., description="담당자의 번호")
    id: str = Field(..., description="기업회원의 ID")
    password: SecretStr = Field(..., description="기업회원의 비밀번호")


class RequestManagerSchema(BaseModel):
    Manager: ManagerSchema = Field(..., description="기업회원 정보")