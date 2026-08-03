# PDF Data Extractor

Automação desenvolvida em Python para extrair informações estruturadas de conjuntos de documentos PDF e consolidá-las em uma planilha Excel.

O projeto foi criado para auxiliar uma atividade operacional que envolvia a consulta e organização manual de informações presentes em múltiplos documentos retirados do Sistema Nacional de Informações de Defesa do Consumidor integrado ao Procon-MPMG.

## Objetivo

Automatizar o processo de:

* localizar arquivos PDF em um diretório;
* extrair informações das tabelas e metadados dos documentos;
* consolidar os dados extraídos;
* gerar uma planilha Excel com os resultados.

### Fluxo

```text
PDFs
  │
  ▼
Extração de dados
  │
  ▼
Processamento em lote
  │
  ▼
Consolidação
  │
  ▼
Planilha Excel
```

## Tecnologias

* **Python**
* **pdfplumber** — extração de informações dos documentos PDF
* **Pandas** — estruturação e consolidação dos dados
* **OpenPyXL** — geração da planilha Excel

## Estrutura

```text
pdf-data-extractor/
├── src/
│   ├── main.py
│   │
│   ├── extraction/
│   │   ├── pdf_extractor.py
│   │   ├── extraction_config.py
│   │   └── extraction_error.py
│   │
│   ├── processing/
│   │   └── batch_processor.py
│   │
│   └── output/
│       └── excel_writer.py
│
├── data/
│   └── input/
│
├── output/
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Instalação

Clone o repositório:

```bash
git clone https://github.com/Alieinstein2008/pdf-data-extractor.git
cd pdf-data-extractor
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Utilização

Coloque os documentos PDF que deseja processar em:

```text
data/input/
```

Execute:

```bash
python src/main.py
```

Os dados extraídos serão consolidados em:

```text
output/tabela.xlsx
```

## Finalidade

Projeto desenvolvido como ferramenta de apoio ao trabalho, destinado à extração e organização de informações utilizadas em análises, estudos e pesquisas.

A ferramenta tem finalidade operacional e acadêmica, sendo voltada à automatização da organização dos dados e não à comercialização das informações processadas.

## Tratamento de erros

Documentos que não seguem a estrutura esperada são identificados durante o processamento e não interrompem a execução dos demais arquivos.

Exemplo:

```text
Processando: documento-01.pdf...
OK — 42 registros extraídos.

Processando: documento-02.pdf...
ERRO — documento-02.pdf: Metadado não encontrado: Guia Nº:

Processando: documento-03.pdf...
OK — 31 registros extraídos.
```

Dessa forma, arquivos válidos continuam sendo processados mesmo quando um documento apresenta problemas de estrutura.

## Observações

O extrator foi desenvolvido para documentos que seguem um formato específico. Alterações na estrutura, posicionamento ou nomenclatura dos campos dos PDFs podem exigir ajustes nas configurações de extração.

Os arquivos de entrada e planilhas geradas são mantidos fora do versionamento por meio do `.gitignore`.
