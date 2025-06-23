

def test_register_and_authenticate():
    service = UserService()
    username = "juanito"
    email = "juanito@example.com"
    password = "claveSegura123"
    full_name = "Juanito Prueba"

    print("🧪 Registrando usuario...")
    user = service.register_user(username, email, password, full_name)
    assert user["id"] is not None
    print(f"✅ Usuario registrado con ID {user['id']}")

    print("🔐 Autenticando con contraseña válida...")
    authenticated_user = service.authenticate(username, password)
    assert authenticated_user is not None
    print("✅ Autenticación exitosa")

    print("🔐 Autenticando con contraseña inválida...")
    invalid_login = service.authenticate(username, "contraseñaIncorrecta")
    assert invalid_login is None
    print("✅ Autenticación fallida como se esperaba")

def test_user_queries():
    service = UserService()

    print("🔍 Buscando usuario por username...")
    user = service.get_user("juanito")
    assert user is not Nonefrom services.user_service import UserService

    print(f"✅ Usuario encontrado: {user['username']}")

    print("📋 Listando todos los usuarios...")
    users = service.list_users()
    assert isinstance(users, list)
    print(f"👥 Total de usuarios: {len(users)}")

def test_deactivate_user():
    service = UserService()
    user = service.get_user("juanito")
    if user:
        print("🛑 Desactivando usuario...")
        result = service.deactivate(user["id"])
        assert result["is_active"] is False
        print("✅ Usuario desactivado correctamente")

if __name__ == "__main__":
    test_register_and_authenticate()
    test_user_queries()
    test_deactivate_user()
