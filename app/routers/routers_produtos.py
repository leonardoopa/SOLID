from typing import List, Dict
from fastapi import APIRouter, HTTPException
from app.models.models_produtos import (
    Produto,
    CriarProduto,
    HistoricoCompras,
    Preferencias,
)
from .routers_usuarios import usuarios


router = APIRouter()

produtos: List[Produto] = []
contador_produto: int = 1
# Histórico de compras em memória
historico_de_compras: Dict[int, List[int]] = {}


@router.post("/produtos/", response_model=Produto)
def criar_produto(produto: CriarProduto) -> Produto:
    """Cria um novo produto com o nome, categoria e tags fornecidos."""
    global contador_produto
    novo_produto = Produto(id=contador_produto, **produto.model_dump())
    produtos.append(novo_produto)
    contador_produto += 1
    return novo_produto


@router.get("/produtos/", response_model=List[Produto])
def listar_produtos() -> List[Produto]:
    """Retorna uma lista de produtos cadastrados."""
    return produtos


@router.post("/historico_compras/{usuario_id}")
def adicionar_historico_compras(
    usuario_id: int, compras: HistoricoCompras
) -> Dict[str, str]:
    """Adiciona um histórico de compras para um usuário."""
    if usuario_id not in [usuario.id for usuario in usuarios]:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    historico_de_compras[usuario_id] = compras.produtos_ids
    return {"mensagem": "Histórico de compras atualizado"}


@router.post("/recomendacoes/{usuario_id}", response_model=List[Produto])
def recomendar_produtos(usuario_id: int, preferencias: Preferencias) -> List[Produto]:
    """Recomenda produtos com base no histórico de compras e preferências do usuário."""
    if usuario_id not in historico_de_compras:
        raise HTTPException(
            status_code=404, detail="Histórico de compras não encontrado"
        )

    produtos_recomendados = []

    # Buscar produtos com base no histórico de compras do usuário

    produtos_recomendados = [
        produto
        for produto_id in historico_de_compras[usuario_id]
        for produto in produtos
        if produto.id == produto_id
    ]

    # Filtrar as recomendações com base nas preferências
    produtos_recomendados = [
        p for p in produtos_recomendados if p.categoria in preferencias.categorias
    ]  # Preferencias de categorias
    produtos_recomendados = [
        p
        for p in produtos_recomendados
        if any(tag in preferencias.tags for tag in p.tags)
    ]  # Preferencias de tags

    return produtos_recomendados
