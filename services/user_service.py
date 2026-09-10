from werkzeug.security import generate_password_hash, check_password_hash

from repositories.user_repository import UserRepository


class UserService:

    # LISTAR USUÁRIOS
    @staticmethod
    def list_all_users():
        users = UserRepository.get_all()
        return [user.to_dict() for user in users]

    # BUSCAR USUÁRIO
    @staticmethod
    def get_user(user_id: int):
        user = UserRepository.get_by_id(user_id)

        if not user:
            return None

        return user.to_dict()

    # CRIAR USUÁRIO
    @staticmethod
    def create_user(data: dict):

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not name.strip():
            raise ValueError("O nome é obrigatório.")

        if not email or not email.strip():
            raise ValueError("O e-mail é obrigatório.")

        if not password:
            raise ValueError("A senha é obrigatória.")

        email = email.strip().lower()

        if UserRepository.get_by_email(email):
            raise ValueError("Este e-mail já está cadastrado.")

        # Criptografa a senha antes de salvar
        password = generate_password_hash(password)

        return UserRepository.create(
            name=name.strip(),
            email=email,
            password=password
        )

    # LOGIN
    @staticmethod
    def login(email: str, password: str):

        user = UserRepository.get_by_email(
            email.strip().lower()
        )

        if not user:
            return None

        if not check_password_hash(user.password, password):
            return None

        return user

    # ATUALIZAR USUÁRIO
    @staticmethod
    def update_user(user_id: int, data: dict):

        user = UserRepository.get_by_id(user_id)

        if not user:
            return None

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if name is not None and not name.strip():
            raise ValueError("O nome não pode ser vazio.")

        if email is not None:

            email = email.strip().lower()

            existing_user = UserRepository.get_by_email(email)

            if existing_user and existing_user.id != user.id:
                raise ValueError("Este e-mail já está cadastrado.")

        if password:
            password = generate_password_hash(password)

        updated_user = UserRepository.update(
            user,
            name=name.strip() if name is not None else None,
            email=email,
            password=password
        )

        return {
            "id": updated_user.id,
            "name": updated_user.name,
            "email": updated_user.email
        }

    # EXCLUIR USUÁRIO
    @staticmethod
    def delete_user(user_id: int):

        user = UserRepository.get_by_id(user_id)

        if not user:
            return False

        UserRepository.delete(user)
        return True