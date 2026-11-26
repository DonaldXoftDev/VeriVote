import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate


@pytest.fixture
def user_details() -> dict[str, str]:
    return {
        'org_name': 'Test_Org',
        'email': 'Test@gmail.com',
        'password': 'TestPassword123'
    }

def test_usercreate_schema_succeeds(user_details):
    record = UserCreate(**user_details)

    assert record.email == user_details['email']
    assert record.password == user_details['password']
    assert record.org_name == user_details['org_name']

def test_invalid_email_format_fails(user_details):
    with pytest.raises(ValidationError):
        UserCreate(
            email='james@',
            password=user_details['password'],
            org_name=user_details['org_name']
        )

def test_short_password_fails(user_details):
      with pytest.raises(ValidationError):
        UserCreate(
            email=user_details['email'],
            password='james',
            org_name=user_details['org_name'],
        )


def test_blank_org_name_during_user_creation_fails(user_details):
        with pytest.raises(ValidationError):
            UserCreate(
                email=user_details['email'],
                password='james',
                org_name='',
            )

def test_userresponse_model_omit_password_hash(user_details):
    record = UserCreate(**user_details)

    assert 'password_hash' not in record.model_dump()
