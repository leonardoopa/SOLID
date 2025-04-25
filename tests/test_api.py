import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "mensagem": "Bem-vindo à API de Recomendação de Produtos"
    }

def test_criar_produto():
    response = client.post(
        "/produtos/",
        json={
            "nome": "iphone",
            "categoria": "eletrônico",
            "tags": ["smartphone", "apple"],
        },
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "iphone"

def test_listar_produtos():
    response = client.get("/produtos/")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_criar_usuario():
    response = client.post("/usuarios/", params={"nome": "John Doe"})    
    assert response.status_code == 200
    usuario_data = response.json()
    assert usuario_data["nome"] == "John Doe"

def test_listar_usuarios():
    response = client.get("/usuarios/")
    assert response.status_code == 200
    assert len(response.json()) == 1    

def test_historico_compras():
    response = client.post(
        "/historico_compras/1",
        json={
            "produtos_ids": [1, 2, 3],
        },
    )    
    assert response.status_code == 200
    assert response.json()["mensagem"] == "Histórico de compras atualizado"


def test_recomendacoes():
    response = client.post(
        "/recomendacoes/1",
        json={
            "preferencias": {
                "categorias": ["eletrônico", "smartphone"],
                "tags": ["apple", "smartphone"],
            },
        },
    )    
    assert response.status_code == 500
    assert len(response.json()) == 1

