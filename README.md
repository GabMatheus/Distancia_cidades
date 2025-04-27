# Distância entre Cidades

Este projeto calcula a distância entre uma cidade de origem e todas as cidades do Brasil utilizando a API do Google Maps. O cálculo pode ser feito entre uma cidade de origem e uma cidade de destino específica ou entre a cidade de origem e todas as cidades, gerando um arquivo CSV com as distâncias.

Foi desenvolvido em Python e pode ser transformado em um executável para ser usado em máquinas que não possuem Python instalado.

## Como usar

1. Instale as dependências necessárias:
      ```
      requests
      PyQt5
      unidecode
      ```

2. Para gerar o executável, rode o seguinte comando no diretório que os arquivos estarão:
    - `pyinstaller --onefile --add-data "cidades.db;cidades.db" ler_cid.py`

   Isso criará um executável na pasta `dist/`. Lembre-se de colocar o arquivo `cidades.db` junto à pasta `dist/` para que o banco de dados seja acessado corretamente.

3. O código pode ser usado por empresas de transportes de cargas ou vendas de produtos, ajudando na logística para calcular a distância entre a cidade de origem e a cidade de destino específica ou entre a cidade de origem e todas as cidades do Brasil.

4. **Importante**: É necessário obter uma chave da API do Google Maps para o projeto funcionar. Substitua no código onde está comentado com a sua chave da API.

## Observações

- Ao executar o programa, você pode calcular a distância entre a cidade de origem e a cidade de destino informada, ou calcular as distâncias para todas as cidades do Brasil, gerando um arquivo CSV com as distâncias.
- Não forneci a chave da API no código por questões de segurança, então é necessário configurá-la individualmente para o funcionamento adequado do programa.

## Contribuições

Caso queira contribuir com melhorias ou correções, fique à vontade para abrir uma issue ou enviar um pull request.

## Feito por:

Gabriel Matheus Oliveira - gab_matheus@hotmail.com
