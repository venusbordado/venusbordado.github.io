# Como atualizar a página de links

Endereço: **https://venusbordado.github.io**
Pasta no computador: `Área de Trabalho\Venus\venus-links`
Repositório: https://github.com/venusbordado/venusbordado.github.io

## Jeito mais fácil
Mande o link de afiliado para o Claude ("acrescenta esse produto na página: https://meli.la/...").
Ele confere o anúncio, coloca a foto e publica.

## Sozinha, com o script
1. Gere o link no painel de afiliados do Mercado Livre (nunca monte o link na mão).
2. Abra o terminal na pasta `venus-links` (clique com o botão direito na pasta → "Abrir no Terminal").
3. Rode:
   ```
   C:\Users\Carol\.venvs\edicao\Scripts\python.exe adicionar.py https://meli.la/SEU-LINK "Linhas"
   ```
   (se quiser escolher o nome que aparece, acrescente no fim entre aspas: `"Kit de linhas que eu uso"`)
4. Ele mostra o título do anúncio e a foto que vai entrar. **Confira se é o produto certo** e digite `s` para publicar.
5. Em 1 ou 2 minutos aparece no site.

## Na mão (se o script falhar)
1. Coloque a foto em `img/` (quadrada, até 600 px, de preferência `.webp`).
2. Abra `dados.json` e copie um bloco de produto, trocando `nome`, `foto`, `link`, `categoria` e `data`.
3. No terminal da pasta: `git add -A`, depois `git commit -m "novo produto"`, depois `git push`.

## Regras (não quebrar)
- Nome, foto e link têm que ser do MESMO produto.
- Não escrever preço, nota, "mais vendido" ou promoção que não esteja no anúncio.
- Só link de afiliado do seu painel.
- Mais de 6 produtos: os filtros por categoria aparecem sozinhos.

## Trocar botões do topo (lojas e redes)
Ficam no `index.html`, entre `<nav class="redes">` e `</nav>`. Peça ao Claude.
