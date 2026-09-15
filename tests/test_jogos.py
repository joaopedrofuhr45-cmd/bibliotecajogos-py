def test_web_listar_jogos_vazio(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Nenhum jogo cadastrado" in response.text

def test_web_fluxo_completo(client):
    # 1. Adicionar jogo via form
    response = client.post("/jogos", data={"titulo": "Super Mario Odyssey", "plataforma": "Nintendo Switch"})
    assert response.status_code == 200
    assert "Super Mario Odyssey" in response.text
    assert "Jogando" in response.text

    # 2. Alternar para Zerado
    response_concluir = client.post("/jogos/1/concluir")
    assert response_concluir.status_code == 200
    assert "Zerado" in response_concluir.text

    # 3. Apagar jogo
    response_apagar = client.post("/jogos/1/apagar")
    assert response_apagar.status_code == 200
    assert "Super Mario Odyssey" not in response_apagar.text

def test_api_rest_completa(client):
    # 1. Listar vazio
    resp = client.get("/api/jogos")
    assert resp.status_code == 200
    assert resp.json() == []

    # 2. Criar via POST JSON
    post_resp = client.post("/api/jogos", json={"titulo": "God of War Ragnarok", "plataforma": "PS5", "concluido": False})
    assert post_resp.status_code == 201
    jogo_id = post_resp.json()["id"]

    # 3. Buscar por ID
    get_resp = client.get(f"/api/jogos/{jogo_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["titulo"] == "God of War Ragnarok"

    # 4. Atualizar via PUT
    put_resp = client.put(f"/api/jogos/{jogo_id}", json={"titulo": "God of War (2018)", "plataforma": "PC", "concluido": True})
    assert put_resp.status_code == 200
    assert put_resp.json()["titulo"] == "God of War (2018)"

    # 5. Alternar status via PATCH
    patch_resp = client.patch(f"/api/jogos/{jogo_id}/concluir")
    assert patch_resp.status_code == 200
    assert patch_resp.json()["concluido"] is False

    # 6. Deletar via DELETE
    del_resp = client.delete(f"/api/jogos/{jogo_id}")
    assert del_resp.status_code == 204

    # 7. Buscar deletado (404)
    resp_404 = client.get(f"/api/jogos/{jogo_id}")
    assert resp_404.status_code == 404