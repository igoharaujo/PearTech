import mercadopago

# Substituir pelas credencias de produção da minha conta
public_key = "APP_USR-0a01dcf2-b4e6-4607-87ba-2737c2f6e7d8"
token = "APP_USR-1334559273165883-102215-1455f11605edd8a620d4291f0a7de751-2050496847"

def criar_pagamento(itens_pedido, link):
	sdk = mercadopago.SDK(token)

	# Precisam ser passados em request:
	# - Itens que serão comprados no formato de dicionário
	itens = []
	for item in itens_pedido:
		quantidade = int(item.quantidade)
		nome_produto = item.item_estoque.produto.nome
		preco_unitario = float(item.item_estoque.produto.preco)
		itens.append({
			"title": nome_produto,
			"quantity": quantidade,
			"unit_price": preco_unitario,
		})

	# - Valor total

	request = {
		"items": itens,
		"back_urls": {
			"success": "http://test.com/success",
			"failure": "http://test.com/failure",
			"pending": "http://test.com/pending",
		},
	}

	resposta = sdk.preference().create(request)
	link_pagamento = resposta["response"]["init_point"]
	id_pagamento = resposta["response"]["id"]
	return link_pagamento, id_pagamento